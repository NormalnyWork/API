import logging
import logging.config
import os.path

from pydantic import Extra
from pydantic_settings import BaseSettings


class MyFormatter(logging.Formatter):
    err_fmt = '[%(asctime)s][%(filename)s.%(funcName)s(%(lineno)d)][%(levelname)s] - %(message)s'
    dbg_fmt = '[%(asctime)s][%(filename)s.%(funcName)s(%(lineno)d)][%(levelname)s] - %(message)s'
    info_fmt = '[%(asctime)s][%(levelname)s] - %(message)s'

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt='%Y-%m-%d %H:%M:%S', style='%')

    def format(self, record):
        format_orig = self._style._fmt

        if record.levelno == logging.DEBUG:
            self._style._fmt = MyFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._style._fmt = MyFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = MyFormatter.err_fmt

        result = logging.Formatter.format(self, record)
        self._style._fmt = format_orig
        return result


class Settings(BaseSettings, extra=Extra.ignore):
    host: str = '0.0.0.0'
    port: int = 8000
    app_name: str = 'blomup'
    pg_host: str = ''
    pg_user: str = ''
    pg_password: str = ''
    pg_port: str = ''
    pg_database: str = ''
    aws_access_key_id: str = ''
    aws_secret_access_key: str = ''
    firebase_credentials_path: str = ''

    class Config:
        env_file = '../.env'

    @property
    def database_url(self):
        if self.pg_host:
            # return f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}"
            return f'postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}'
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3').replace('\\', '/')
        return f"sqlite:///{path}"


def get_settings():
    return Settings()


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'info_format': {
            '()': MyFormatter
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'info_format',
        },
        # 'info_rotating_file_handler': {
        #     'level': 'INFO',
        #     'formatter': 'info_format',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': 'main.log',
        #     'mode': 'a',
        #     'maxBytes': 1048576,
        #     'backupCount': 10
        # },
    },

    'loggers': {
        '__main__': {
            'handlers': ['stream_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'database': {
            'handlers': ['stream_handler'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)