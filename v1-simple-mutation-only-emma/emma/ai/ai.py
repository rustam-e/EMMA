from langchain_openai import ChatOpenAI 
from langchain.schema import HumanMessage
from utils.logger import logger

from settings import settings

class LangchainClient:
    def __init__(self):
        self.chat_model = ChatOpenAI(
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            model_name=settings.ai_model_name,
            openai_api_key=settings.openai_api_key
        )

    def complete(self, prompt: str) -> str:
        logger.info(f"Sending request with prompt: {prompt[:100]}...")
        messages = [HumanMessage(content=prompt)]
        response = self.chat_model.invoke(messages)
        result = response.content
        logger.info(f"Received response: {result[:100]}...")
        return result
