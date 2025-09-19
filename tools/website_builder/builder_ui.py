import streamlit as st
import streamlit.components.v1 as components
from .page_store import PageStore

def show_builder():
    st.title("Website & Landing Page Builder (Drag & Drop)")
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("Save page"):
            html = st.session_state.get("gjs_html", "")
            css = st.session_state.get("gjs_css", "")
            name = st.text_input("Page name", value="landing-page")
            if name:
                PageStore.save_page(name, html, css)
                st.success("Saved!")
        st.write("Saved pages")
        pages = PageStore.list_pages()
        page = st.selectbox("Open saved page", [""]+pages)
        if page:
            p = PageStore.load_page(page)
            st.code("Preview: open in new tab by saving as static HTML.", language="html")

    # GrapesJS HTML bootstrap (simple)
    grapes_html = """
    <link href="https://unpkg.com/grapesjs/dist/css/grapes.min.css" rel="stylesheet"/>
    <div id="gjs" style="height:600px; border:1px solid #ccc;"></div>
    <script src="https://unpkg.com/grapesjs"></script>
    <script>
      const editor = grapesjs.init({ container: '#gjs', fromElement: false, storageManager: false});
      editor.setComponents('<div class="my-page"><h1>Hello</h1><p>Drag and edit...</p></div>');
      editor.on('change:changesCount', () => {
        const html = editor.getHtml();
        const css = editor.getCss();
        // send to Streamlit via window.sessionStorage (workaround)
        window.sessionStorage.setItem('gjs_html', html);
        window.sessionStorage.setItem('gjs_css', css);
      });
    </script>
    """
    components.html(grapes_html, height=700)

    # load values from sessionStorage via a JS injection trick (polling)
    components.html("""
    <script>
    setInterval(()=> {
      const h = window.sessionStorage.getItem('gjs_html') || '';
      const c = window.sessionStorage.getItem('gjs_css') || '';
      if (window.parent) {
        const msg = {html: h, css: c};
        window.parent.postMessage(msg, "*");
      }
    }, 1000);
    </script>
    """, height=1)

    # client side to python via st.experimental_get_query_params is limited;
    # as a simple approach, let user copy HTML from editor to a textarea when saving.
    st.info("If Save button doesn't capture the HTML, copy the page HTML/CSS and paste into the save form below.")
    html_input = st.text_area("Paste page HTML (if needed)")
    css_input = st.text_area("Paste page CSS (if needed)")
    if st.button("Save pasted page"):
        name = st.text_input("Page name for paste")
        PageStore.save_page(name or "page-from-paste", html_input, css_input)
        st.success("Saved pasted page")
