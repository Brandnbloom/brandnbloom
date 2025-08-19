import os, smtplib, ssl, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mailer")

# SMTP Config from environment
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
SMTP_FROM = os.environ.get("SMTP_FROM", "Brand N Bloom <noreply@example.com>")

# Restrict all attachments to this directory
UPLOAD_DIR = os.path.abspath("uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def send_email(to_email: str, subject: str, html: str, attachments: list[str] | None = None):
    """
    Send an email with optional attachments using secure TLS.
    All attachments must exist inside the UPLOAD_DIR folder.
    """
    try:
        # Build email
        msg = MIMEMultipart()
        msg["From"] = SMTP_FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html, "html"))

        # Attachments (if any)
        attachments = attachments or []
        for path in attachments:
            try:
                # Normalize & enforce restriction
                safe_name = os.path.basename(path)  # strip directory traversal
                abs_path = os.path.abspath(os.path.join(UPLOAD_DIR, safe_name))

                if not abs_path.startswith(UPLOAD_DIR):
                    raise ValueError("Invalid attachment path")

                if not os.path.isfile(abs_path):
                    raise FileNotFoundError(f"File not found: {safe_name}")

                with open(abs_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=safe_name)
                    part["Content-Disposition"] = f'attachment; filename="{safe_name}"'
                    msg.attach(part)

            except Exception as e:
                logger.warning(f"⚠️ Skipped attachment {path}: {e}")

        # Secure TLS context
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1

        # Connect & send
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            if SMTP_USER and SMTP_PASS:
                server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_FROM, [to_email], msg.as_string())

        logger.info(f"✅ Email sent to {to_email} with subject '{subject}'")

    except Exception as e:
        logger.error(f"❌ Failed to send email to {to_email}: {e}")
