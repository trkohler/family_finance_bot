import logging
import re
import requests
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CallbackContext

from constants import (
    MONOBANK_API_URL,
    types_of_spends,
)
from app.notion import (
    check_if_card_exist,
    notion_page_builder,
    get_remain_from_res,
    prepare_query_kwargs,
    notion,
)

logger = logging.getLogger(__name__)

cache = dict()

def identify_type_of_spend(title: str) -> dict:
    type_of_spend = next(filter(
        lambda item: item.get('title') == title,
        types_of_spends.values()
    ))
    return type_of_spend

def get_converted_sum(sum: float) -> float:
    rate_sell = cache.get("rate_sell")
    
    if not rate_sell:
        request_url = MONOBANK_API_URL
        response = requests.request(
            "GET",
            request_url,
        )
        all_currencies = response.json()
        
        euro_to_uah = next(filter(
            lambda item: item["currencyCodeA"] == 978 and item["currencyCodeB"] == 980,
            all_currencies
        ))
        
        rate_sell = euro_to_uah["rateSell"]
        cache["rate_sell"] = rate_sell
    
    amount = sum * rate_sell

    return amount

def get_converted_remain(sum: float) -> float:
    rate_sell = cache.get("rate_sell")
    
    if not rate_sell:
        request_url = MONOBANK_API_URL
        response = requests.request(
            "GET",
            request_url,
        )
        all_currencies = response.json()
        
        euro_to_uah = next(filter(
            lambda item: item["currencyCodeA"] == 978 and item["currencyCodeB"] == 980,
            all_currencies
        ))
        
        rate_sell = euro_to_uah["rateSell"]
        cache["rate_sell"] = rate_sell
    
    amount = sum / rate_sell

    return amount


def make_notion_card(
    update: Update,
    context: CallbackContext,
    *args,
    **kwargs,
):
    content = update.channel_post.text
    channel_post = update.channel_post
    tokens = content.split("\n")
    title = tokens[0]
    
    try:
        type_of_spend = identify_type_of_spend(title)
    except StopIteration:
        logger.error("the title is not found")
        message = "Не найдена категория. Проверьте правильность написания названия категории"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return
    
    sum_of_spend = 0.0

    for token in tokens[1:]:
        price = re.findall(r"[-+]?\d*\.\d+|\d+", token)
        
        if len(price) < 1:
            logger.error("there is no price in the future card")
            message = "Не найдена сумма. Проверьте правильность написания суммы"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            return
        
        sum_of_spend += float(price[0])
    
    converted_from_euro = 0.0
    try:
        converted_from_euro = get_converted_sum(sum_of_spend)
    except ValueError:
        logger.error("api returns some bullshit.")
        message = "конвертер валют вернул какой-то мусор. Конвертация в евро провалилась. Придется завести вручную :("
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return

    res = notion.databases.query(
        **prepare_query_kwargs(title)
    )
    remain_value = get_remain_from_res(res)
    remain_flag = type_of_spend["remain"]

    notion_page = notion_page_builder(
        title,
        type_of_spend["id"],
        int(round(converted_from_euro)),
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
            logger.info("the card exist!")
            remain = last_card_month['properties']['Remain']['formula'].get('number')
            
            try:
                remain_converted = get_converted_remain(remain)
            except (ValueError, KeyError):
                logger.error("api returns some bullshit.")
                message = "конвертер валют вернул какой-то мусор. Конвертация в евро провалилась. :("
                context.bot.send_message(chat_id=update.effective_chat.id, text=message)
                return
            
            remain_flag = type_of_spend["remain"]
            if remain_converted and remain_flag:
                message += (
                    f"По категории {type_of_spend['title']} "
                    f"осталось {remain_converted} "
                    f"euro \n"
                )
            elif remain_converted and not remain_flag:
                message += (
                    f"По категории {type_of_spend['title']} "
                    f"в этом месяце потрачено {-remain_converted} "
                    f"euro \n"
                )
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def show_all_type_of_spends(
    update: Update,
    context: CallbackContext
):
    types_of_spends = list(map(lambda item: item["title"], types_of_spends.values()))
    
    message = "Все категории: \n"
    
    for type_of_spend in types_of_spends:
        message += f"- {type_of_spend} \n"
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)