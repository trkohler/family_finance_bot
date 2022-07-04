from difflib import SequenceMatcher
from typing import Optional, Union

from telegram import Message
from telegram.ext import MessageFilter
from telegram.ext.filters import DataDict

from constants import types_of_spends


class FilterRemain(MessageFilter):
    def filter(self, message):
        if SequenceMatcher(None, message.text, "cкок осталось").ratio() > 0.6:
            return True
        return False


class FilterSpend(MessageFilter):
    def filter(self, message: Message) -> Optional[Union[bool, DataDict]]:
        content = message.text
        tokens = content.split("\n")
        for type_of_spend in types_of_spends.values():
            if SequenceMatcher(None, tokens[0], type_of_spend["title"]).ratio() > 0.6:
                return True
        return False

class FilterShowCategories(MessageFilter):
    
    def filter(self, message: Message) -> Optional[Union[bool, DataDict]]:
        content = message.text
        if content == "Показать категории":
            return True
        return False

filter_remain = FilterRemain()
filter_spend = FilterSpend()
filter_show_categories = FilterShowCategories()
