'''
if "svg_height" not in st.session_state:
    st.session_state["svg_height"] = 200

if "previous_mermaid" not in st.session_state:
    st.session_state["previous_mermaid"] = ""

def mermaid(code: str) -> None:
    html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height = st.session_state["svg_height"] + 50,
    )

code = """
    graph TD
        A[Step 1] -->B[Step 2]
        B --> C[Step 3]
    """

mermaid(code)

if code != st.session_state["previous_mermaid"]:
    st.session_state["previous_mermaid"] = code
    sleep(1)
    streamlit_js_eval(
        js_expressions='parent.document.getElementsByTagName("iframe")[0].contentDocument.getElementsByClassName("mermaid")[0].getElementsByTagName("svg")[0].getBBox().height',
        key="svg_height",
    )
'''