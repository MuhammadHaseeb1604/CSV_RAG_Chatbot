import os
from dotenv import load_dotenv
from llama_index.llms.together import TogetherLLM
from llama_index.core.settings import Settings

def init_llm():
    load_dotenv()

    llm = TogetherLLM(
        model="meta-llama/Llama-3-70b-chat-hf", api_key=os.getenv('TOGETHER_API_KEY')
    )

    Settings.llm = llm