import logging
import re
from datetime import datetime, timedelta
from difflib import SequenceMatcher

from telegram import Update
from telegram.ext import CallbackContext

from app.bot import logger
from constants import (
    types_of_spends,
)
from notion import (
    check_if_card_exist,
    notion_page_builder,
    get_remain_from_res,
    prepare_query_kwargs, notion,
)


def make_notion_card(
    update: Update,
    *args,
    **kwargs,
):
    content = update.channel_post.text
    channel_post = update.channel_post
    tokens = content.split("\n")
    title = tokens[0]
    type_of_spend: dict = filter(
        lambda item:
            SequenceMatcher(
                None, item.get("title"), title
            ).ratio() > 0.6,
        types_of_spends.values()
    ).__next__()
    sum_of_spend = 0.0

    for token in tokens[1:]:
        price = re.findall(r"[-+]?\d*\.\d+|\d+", token)
        if len(price) < 1:
            logger.error("there is no price in the future card")
            return
        sum_of_spend += float(price[0])

    res = notion.databases.query(
        **prepare_query_kwargs(title)
    )
    remain_value = get_remain_from_res(res)
    remain_flag = type_of_spend["remain"]

    notion_page = notion_page_builder(
        title,
        type_of_spend["id"],
        int(round(sum_of_spend)),
        remain_value=remain_value,
        bullets=tokens[1:],
        remain_flag=remain_flag
    )
    notion.pages.create(**notion_page)
    channel_post.delete()


def how_many_remain(
        update: Update,
        context: CallbackContext
):
    message = ""
    for type_of_spend in types_of_spends.values():
        last_month = (
                datetime
                .today()
                - timedelta(30)
        )
        last_card_month = check_if_card_exist(type_of_spend["title"], last_month)
        if last_card_month:
            logging.info("the card exist!")
            remain = last_card_month['properties']['Remain']['formula'].get('number')
            remain_flag = type_of_spend["remain"]
            if remain and remain_flag:
                message += (
                    f"По категории {type_of_spend['title']} "
                    f"осталось {remain} "
                    f"гривен \n"
                )
            elif remain and not remain_flag:
                message += (
                    f"По категории {type_of_spend['title']} "
                    f"в этом месяце потрачено {-remain} "
                    f"гривен \n"
                )
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

