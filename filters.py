from difflib import SequenceMatcher

from telegram.ext import MessageFilter


class FilterRemain(MessageFilter):
    def filter(self, message):
        if SequenceMatcher(None, message.text, "cкок осталось").ratio() > 0.6:
            return True
        return False


filter_remain = FilterRemain()
