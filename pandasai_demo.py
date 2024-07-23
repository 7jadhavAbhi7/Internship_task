# import streamlit as st
# import os
# from pandasai.connectors.yahoo_finance import YahooFinanceConnector
# from pandasai import SmartDataframe
# from pandasai.llm.openai import OpenAI

# # Set the OpenAI API key
# api_key = os.getenv('OPENAI_API_KEY')

# # Initialize the OpenAI LLM
# llm = OpenAI(api_token=api_key)

# # Streamlit app
# st.title("Stock Information")

# # User input
# prompt = st.text_input("Enter your query:")

# if prompt:
#     yahoo_connector = YahooFinanceConnector("TSLA")
#     df = SmartDataframe(yahoo_connector)
#     response = df.chat(prompt, llm=llm)
#     st.write(response)

# # Run the app with: streamlit run your_script.py
import os

import streamlit as st
from pandasai import SmartDataframe
from pandasai.callbacks import BaseCallback
from pandasai.llm import OpenAI
from pandasai.responses.response_parser import ResponseParser
import pandas as pd
import plotly.express as px
from langchain import PromptTemplate
class StreamlitCallback(BaseCallback):
    def __init__(self, container) -> None:
        """Initialize callback handler."""
        self.container = container

    def on_code(self, response: str):
        self.container.code(response)


class StreamlitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result["value"])
        return

    def format_plot(self, result):
        st.image(result["value"])
        return

    def format_other(self, result):
        st.write(result["value"])
        return


st.write("# Chat with Credit Card Fraud Dataset 🦙")

df = pd.read_csv('msft_stock_data.csv')

with st.expander("🔎 Dataframe Preview"):
    st.write(df.tail(3))

query = st.text_area("🗣️ Chat with Dataframe")
container = st.container()
demo_template='''I want you to act as a plotting bot who plots graph using plotly'''
# prompt=PromptTemplate(
#     input_variables=['financial_concept'],
#     template=demo_template
#     )
if query:
    llm = OpenAI(api_token='')
    query_engine = SmartDataframe(
        df,
        config={
            "llm": llm,
            "response_parser": StreamlitResponse,
            "callback": StreamlitCallback(container),
            "custom_instructions":demo_template
        },
    )

    answer = query_engine.chat(query)