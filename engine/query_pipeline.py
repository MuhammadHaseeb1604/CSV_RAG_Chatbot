import streamlit as st
from llama_index.core.settings import Settings
from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent,
)
from llama_index.experimental.query_engine.pandas import PandasInstructionParser

from engine import promptTemplates as pt

@st.cache_resource
def get_query_pipeline(df):
    pandas_prompt = pt.pandas_prompt_tmplt.partial_format(
        instruction_str=pt.instruction_str, df_str=df.head(5), df_info_str=pt.df_info_str
    )
    pandas_output_parser = PandasInstructionParser(df)
    response_synthesis_prompt = pt.response_synthesis_prompt_tmplt

    qp = QP(
        modules={
            "input": InputComponent(),
            "pandas_prompt": pandas_prompt,
            "llm1": Settings.llm,
            "pandas_output_parser": pandas_output_parser,
            "response_synthesis_prompt": response_synthesis_prompt,
            "llm2": Settings.llm,
        },
        verbose=False,
    )

    qp.add_chain(["input", "pandas_prompt", "llm1", "pandas_output_parser"])

    qp.add_links(
        [
            Link("input", "response_synthesis_prompt", dest_key="query_str"),
            Link(
                "llm1", "response_synthesis_prompt", dest_key="pandas_instructions"
            ),
            Link(
                "pandas_output_parser",
                "response_synthesis_prompt",
                dest_key="pandas_output",
            ),
        ]
    )

    qp.add_link("response_synthesis_prompt", "llm2")

    return qp
