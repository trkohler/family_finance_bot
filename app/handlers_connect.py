from telegram.ext import MessageHandler, Filters

from app.bot_handlers import how_many_remain, make_notion_card, show_all_type_of_spends
from app.filters import FilterShowCategories, filter_remain, filter_spend

remain_handler = MessageHandler(filter_remain & Filters.chat_type.channel, how_many_remain)
notion_handler = MessageHandler(filter_spend & Filters.chat_type.channel, make_notion_card)
categories_handler = MessageHandler(FilterShowCategories & Filters.chat_type.channel, show_all_type_of_spends)
