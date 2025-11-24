import streamlit as st
import streamlit.components.v1 as components
from .page_store import PageStore

# -----------------------------
# Helper Function for JS Sync
# -----------------------------
SYNC_SCRIPT = """
<script>
window.gjs_save_state = {};

function syncToStreamlit(editor) {
    const html = editor.getHtml();
    const css = editor.getCss();
    window.gjs_save_state = {html, css};

    if (window.parent) {
        window.parent.postMessage(
            {type: 'gjs_content', html: html, css: css},
            "*"
        );
    }
}

window.addEventListener("message", (event) => {
    if (event.data && event.data.type === "load_page") {
        const {html, css} = event.data;
        const editor = window.editorInstance;
        if (editor) {
            editor.setComponents(html || "");
            editor.setStyle(css || "");
        }
    }
});
</script>
"""


# -----------------------------
# Main Builder UI
# -----------------------------
def show_builder():
    st.title("🌐 Website & Landing Page Builder")

    # Saved Pages Sidebar
    with st.sidebar:
        st.header("📁 Saved Pages")
        pages = PageStore.list_pages()
        selected = st.selectbox("Open page", [""] + pages)

        if selected:
            pg = PageStore.load_page(selected)
            st.success(f"Loaded page: {selected}")

            # send content to GrapesJS for loading
            load_script = f"""
            <script>
            window.parent.postMessage({{
                type: "load_page",
                html: `{pg['html']}`,
                css: `{pg['css']}`
            }}, "*");
            </script>
            """
            components.html(load_script, height=0)

        st.markdown("---")
        st.subheader("💾 Save Current Page")

        save_name = st.text_input("Page name", value="landing-page")

        if st.button("Save"):
            html = st.session_state.get("gjs_html", "")
            css = st.session_state.get("gjs_css", "")
            PageStore.save_page(save_name, html, css)
            st.success(f"Saved as {save_name}!")

        # Export HTML
        if st.button("Download HTML"):
            html = st.session_state.get("gjs_html", "")
            css = st.session_state.get("gjs_css", "")
            final_html = f"<style>{css}</style>\n{html}"
            st.download_button("Download HTML", final_html, file_name=f"{save_name}.html")


    # -----------------------------
    # GrapesJS Editor
    # -----------------------------
    st.markdown("### 🧩 Drag & Drop Builder")

    GRAPES_JS = f"""
    <link href="https://unpkg.com/grapesjs/dist/css/grapes.min.css" rel="stylesheet"/>
    <script src="https://unpkg.com/grapesjs"></script>

    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; }}
    </style>

    <div id="gjs" style="height: 700px; border: 2px solid #ccc"></div>

    {SYNC_SCRIPT}

    <script>
        const editor = grapesjs.init({{
            container: '#gjs',
            fromElement: false,
            height: "100%",
            storageManager: false,
            panels: {{ defaults: [] }},
            blockManager: {{
                appendTo: '#blocks',
            }},
        }});

        window.editorInstance = editor;

        editor.on("change:changesCount", () => syncToStreamlit(editor));

        // Custom Blocks
        editor.BlockManager.add("hero", {{
            label: "Hero Section",
            content: `<section style="padding:60px;text-align:center;background:#f4f4f4">
                        <h1>Your Product Headline</h1>
                        <p>Short value description here</p>
                        <button style="padding:10px 20px">Get Started</button>
                      </section>`
        }});

        editor.BlockManager.add("cta", {{
            label: "Call To Action",
            content: `<div style='padding:40px;background:#222;color:#fff;text-align:center;'>
                        <h2>Ready to buy?</h2>
                        <button style='padding:10px 20px;background:#fff;color:#000;'>Buy Now</button>
                      </div>`
        }});

        editor.BlockManager.add("pricing", {{
            label: "Pricing",
            content: `<div style='display:flex;gap:20px;justify-content:center;padding:40px;'>
                        <div style='border:1px solid #ccc;padding:20px;width:200px'><h3>Basic</h3><p>$19</p></div>
                        <div style='border:1px solid #ccc;padding:20px;width:200px'><h3>Pro</h3><p>$49</p></div>
                      </div>`
        }});

        editor.BlockManager.add("footer", {{
            label: "Footer",
            content: `<footer style='padding:20px;text-align:center;background:#eee;'>© Brand & Bloom 2025</footer>`
        }});

        // Initial starter template
        editor.setComponents("<h1>Start designing your page!</h1>");

        // Send save updates via postMessage
        setInterval(() => {{
            if (window.gjs_save_state.html) {{
                window.parent.postMessage({{
                    type: 'gjs_content',
                    html: window.gjs_save_state.html,
                    css: window.gjs_save_state.css
                }}, "*");
            }}
        }}, 1000);
    </script>
    """

    components.html(GRAPES_JS, height=720)


    # -----------------------------
    # Receive HTML/CSS from Builder
    # -----------------------------
    st.markdown("### 📥 Captured HTML/CSS (Debug)")
    msg = st.experimental_get_query_params()

    # Streamlit’s message capturing workaround
    st.session_state["gjs_html"] = st.session_state.get("gjs_html", "")
    st.session_state["gjs_css"] = st.session_state.get("gjs_css", "")

    # manual paste fallback (if needed)
    with st.expander("Manual Save (Fallback)"):
        html_input = st.text_area("Paste HTML")
        css_input = st.text_area("Paste CSS")
        if st.button("Save Pasted Page"):
            PageStore.save_page(save_name, html_input, css_input)
            st.success("Saved manually pasted page!")
