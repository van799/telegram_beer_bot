from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    logger: str = Field('INFO', env='LOGGER')
    debug: str = Field('True', env='DEBUG')

    bot_token: str = Field('INFO', env='BOT_TOKEN')
    admin_pass: str = Field('1234567', env='ADMIN_PASS')


app_settings = AppSettings()
