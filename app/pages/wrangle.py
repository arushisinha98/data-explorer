import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
from streamlit_js_eval import streamlit_js_eval
import random

from PipelineClass import Pipeline


if __name__ == "__main__":

    st.set_page_config(
        page_title = "Transform"
    )

    st.title("Transform")
    master_df = st.session_state["MASTER DATA"]
    pipeline = Pipeline(master_df)
    
    edited_df = st.data_editor(pd.DataFrame(columns = ["S/N", "Step"]),
                               key = "user_input",
                               num_rows = "dynamic",
                               hide_index = False)
    
    st.subheader("Pre-process Methodology")
    st.write(edited_df)

    st.subheader("User Inputs")
    edited_rows = st.session_state["user_input"].get("edited_rows")
    st.write(edited_rows)
    
    consolidated_df = pd.DataFrame(
        {
            "Column": list(master_df.columns),
            "Steps": [random.sample(pipeline.listFunctions, n = random.uniform(0, len(pipeline.listFunctions)))
                      for col in master_df.columns]
        }
    )

    st.dataframe(consolidated_df)
    
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