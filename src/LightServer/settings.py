from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = 9434

    database_url: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600

    max_message_length = 65535
    max_title_length = 24

    blog_post_title_length = 40
    blog_post_text_length = 10000


    class Config:
        env_file = '.env'


settings = Settings()
