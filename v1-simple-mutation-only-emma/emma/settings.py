from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    max_nodes: int = Field(10, env='MAX_NODES')
    openai_api_key: str = Field(..., env='OPENAI_API_KEY')
    max_tokens: int = Field(1500, env='MAX_TOKENS')
    temperature: float = Field(0.5, env='TEMPERATURE')
    ai_model_name: str = Field('gpt-3.5-turbo', env='AI_MODEL_NAME')
    max_parallel_tasks: int = Field(1, env='MAX_PARALLEL_TASKS')

    class Config:
        env_file = '.env'
        protected_namespaces = ('model_',)
        extra = 'allow'

settings = Settings()