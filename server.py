# -*- coding: UTF-8 -*-
from app import create_app
from config import Config
import logging.config
from app import logging_config

logging.config.dictConfig(logging_config.DEV)
app = create_app()
app.run(host=Config.HOST_NAME, port=Config.SERVER_PORT, use_reloader=False)
