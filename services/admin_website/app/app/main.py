import logging
import sys

from app.admin import App

logging.basicConfig(stream=sys.stderr)

app = App()
