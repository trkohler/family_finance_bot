import http
import logging
import os

from flask import (
    Flask,
    request,
    make_response,
)
from telegram import (
    Bot,
    Update,
)
from telegram.ext import (
    Updater,
)
from werkzeug.wrappers import Response

from app.handlers_connect import remain_handler, notion_handler, categories_handler
from constants import telegram_token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

updater = Updater(token=telegram_token)
bot = Bot(token=telegram_token)
dispatcher = updater.dispatcher
dispatcher.add_handler(remain_handler)
dispatcher.add_handler(notion_handler)
dispatcher.add_handler(categories_handler)
logger = logging.getLogger(__name__)
app = Flask(__name__)
port = int(os.environ.get('PORT', 8080))


@app.route("/", methods=["POST"])
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return make_response("", http.HTTPStatus.NO_CONTENT)


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=port)
