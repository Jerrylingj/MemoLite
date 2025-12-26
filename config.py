# 全局 llm 配置
from langchain_siliconflow import ChatSiliconFlow, SiliconFlowEmbeddings
from dataclasses import dataclass
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_BASE_URL = os.getenv("SILICONFLOW_BASE_URL")
SILICONFLOW_EMBED_MODEL = os.getenv("SILICONFLOW_EMBED_MODEL")
SILICONFLOW_CHAT_MODEL = os.getenv("SILICONFLOW_CHAT_MODEL")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.0))

# 配置类, 全局单例
@dataclass
class Config:
    """全局配置类"""
    api_key: str = SILICONFLOW_API_KEY
    base_url: str = SILICONFLOW_BASE_URL
    embed_model = SILICONFLOW_EMBED_MODEL
    chat_model = SILICONFLOW_CHAT_MODEL
    temperature = TEMPERATURE
config = Config()

embeddings = SiliconFlowEmbeddings(model=config.embed_model)
llm = ChatSiliconFlow(
    model=config.chat_model,
    temperature=config.temperature
)