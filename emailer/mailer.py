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

# Safe uploads directory
SAFE_UPLOAD_DIR = os.path.abspath("uploads")
os.makedirs(SAFE_UPLOAD_DIR, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """
    Prevent path traversal by returning only the basename.
    Example: '../../etc/passwd' -> 'passwd'
    """
    return os.path.basename(filename)


def send_email(to_email: str, subject: str, html: str, attachments: list[str] | None = None):
    """
    Send an email with optional attachments securely.
    """
    try:
        # Build email
        msg = MIMEMultipart()
        msg["From"] = SMTP_FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html, "html"))

        # Attachments (safe)
        attachments = attachments or []
        for path in attachments:
            try:
                safe_name = sanitize_filename(path)
                abs_path = os.path.join(SAFE_UPLOAD_DIR, safe_name)

                if not os.path.isfile(abs_path):
                    raise FileNotFoundError(f"File not found: {safe_name}")

                with open(abs_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=safe_name)
                    part["Content-Disposition"] = f'attachment; filename="{safe_name}"'
                    msg.attach(part)

            except Exception as e:
                logger.warning(f"⚠️ Could not attach {path}: {e}")

        # Secure TLS context
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1

        # Send
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
