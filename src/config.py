from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    llm_provider: str = "ollama"

    openai_api_key: str | None= None
    mistral_api_key: str | None= None

    ollama_base_url: str #= "http://localhost:11434"
    ollama_model: str #= "llama3:8b"

    elasticsearch_url: str = "http://localhost:9200"
    elasticsearch_index: str = "acme_knowledge"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()