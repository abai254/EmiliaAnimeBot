import json
from pprint import pprint

import requests
from telegram.ext import CommandHandler

from SaitamaRobot import dispatcher

# Open API key
API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
URL = "http://services.gingersoftware.com/Ginger/correct/json/GingerTheText"


def grammar(update, context):
    if update.effective_message.reply_to_message:
        msg = update.effective_message.reply_to_message

        params = dict(lang="US", clientVersion="2.0", apiKey=API_KEY, text=msg.text)

        res = requests.get(URL, params=params)
        # print(res)
        # print(res.text)
        pprint(json.loads(res.text))
        changes = json.loads(res.text).get("LightGingerTheTextResult")
        curr_string = ""

        prev_end = 0

        for change in changes:
            start = change.get("From")
            end = change.get("To") + 1
            suggestions = change.get("Suggestions")
            if suggestions:
                sugg_str = suggestions[0].get("Text")  # should look at this list more
                curr_string += msg.text[prev_end:start] + sugg_str

                prev_end = end

        curr_string += msg.text[prev_end:]
        print(curr_string)
        update.effective_message.reply_text(curr_string)

__help__ = """
Hi
"""


GRAMMAR_HANDLER = CommandHandler("gmr", grammar)

dispatcher.add_handler(GRAMMAR_HANDLER)


__command_list__ = ["grammar"]
__handlers__ = [GRAMMAR_HANDLER]
