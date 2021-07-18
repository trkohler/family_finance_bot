import logging
import re
from datetime import datetime, timedelta
from difflib import SequenceMatcher

from telegram import Update
from telegram.ext import CallbackContext

from constants import (
    our_home_chat_id, 
    test_chat_id, 
    types_of_spends,
)
from notion import (
    check_if_card_exist,
    notion_page_builder,
    get_remain_from_res,
    prepare_query_kwargs, notion,
)


CHAT_ID=test_chat_id


def make_notion_card(
        content: str,
        channel_post
):
    tokens = content.split("\n")
    sum_of_spend = 0.0

    for token in tokens[1:]:
        price = re.findall(r"[-+]?\d*\.\d+|\d+", token)
        if len(price) < 1:
            print("there is no price in the future card")
            return
        sum_of_spend += float(price[0])

    for type_of_spend in types_of_spends.values():
        if SequenceMatcher(None, tokens[0], type_of_spend["title"]).ratio() > 0.6:
            title = type_of_spend["title"]

            res = notion.databases.query(
                **prepare_query_kwargs(title)
            )
            remain_value, remain_flag = get_remain_from_res(res)
            remain_flag = type_of_spend["remain"] and remain_flag

            notion_page = notion_page_builder(
                title,
                type_of_spend["id"],
                int(round(sum_of_spend)),
                remain_value,
                tokens[1:],
                remain_flag
            )
            notion.pages.create(**notion_page)
            channel_post.delete()
            return
    print("don't find anything interesting")


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
            if remain:
                message += (
                    f"По категории {type_of_spend['title']} "
                    f"осталось {remain} "
                    f"гривен \n"
                )
    if message:
        context.bot.send_message(chat_id=CHAT_ID, text=message)


def cleanup_notion(context: CallbackContext):
    pass


def notion_card_creater(update: Update, context):
    if hasattr(update, "channel_post"):
        chat_id = update.channel_post.chat_id
        if chat_id == CHAT_ID:
            content = update.channel_post.text
            make_notion_card(content, update.channel_post)

# TODO: remove this or do something with it
def new_period(context: CallbackContext):
    ekonomy_tag = list(filter(lambda item: item["economy_flag"], types_of_spends))[0]
    result = []
    ekonomy = 0
    for type_of_spend in types_of_spends:
        if type_of_spend.get("period_map"):
            keys = type_of_spend["period_map"].keys()
            for key in keys:
                if datetime.today().day == key:
                    logging.info("found new period")
                    res = notion.databases.query(
                        **prepare_query_kwargs(type_of_spend["title"])
                    )
                    remain = get_remain_from_res(res)
                    ekonomy += remain
                    notion_page = notion_page_builder(
                        f"Экономия по категории {type_of_spend['title']}",
                        ekonomy_tag["id"],
                        remain,
                        0,
                        bullets=None,
                        spend=False
                    )
                    notion.pages.create(**notion_page)
                    notion_page = notion_page_builder(
                        type_of_spend["title"],
                        type_of_spend["id"],
                        type_of_spend["period_map"][key],
                        0,
                        bullets=None,
                        spend=False
                    )
                    notion.pages.create(**notion_page)
                    result.append(type_of_spend["title"])
    if result:
        context.bot.send_message(
            CHAT_ID,
            f"Новый период начался по таким категориям: {str(result)}\n"
            f"Экономия должна быть: {ekonomy} гривен"
        )
