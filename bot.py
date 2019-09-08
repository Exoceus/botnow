import sys
import os
import logging
import asyncio

from pykeybasebot import Bot
import pykeybasebot.types.chat1 as chat1

from scraper import *

logging.basicConfig(level=logging.DEBUG)

if "win32" in sys.platform:
    # Windows specific event-loop policy
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


class Handler:
    async def __call__(self, bot, event):
        # define trigger, other vars
        trigger = event.msg.content.text.body[:5]
        query = event.msg.content.text.body[6:]
        channel = event.msg.channel

        if event.msg.content.type_name != chat1.MessageTypeStrings.TEXT.value:
            return

        elif trigger == "/wiki":

            summary, URL = scrape(query)

            if summary == " ":
                output = '*Error*: the query you entered was either mis spelled or does not exists on wikipedia. Please try again with a valid query.'

            else:
                output = summary + "\n Learn more at: " + URL

            await bot.chat.send(channel, output)

        elif trigger == "/priv":
            if query == "what\'s new?":
                output = 'Good morning!\n:warning: There was a security break at Facebook.\nWould you like to know what personal data is at risk?'

            elif query == "sure":
                output = 'Facebook knows the following about you:\n1. Full name\n2. Email\n3. Birthday\n4. Location\n5. Friends list\n\nWould you like to know how this may affect you?'

            elif query == "yep":
                output = ':speech_balloon:'

            elif query == "who knows my real name?":
                output = 'There are *28* services that know your full name, and *72* that know only your first name.\nWhich would you like to know more about?'

            elif query == "full name":
                output = 'Okay, here are the top 3 services that know your full name:\n1. Facebook\n2. Google\n3. Amazon\nWhat can I help you with?'

            elif query == "delete my amazon account":
                output = ':white_check_mark:It has been deleted.'

            elif query == "thanks":
                output = ':innocent:No worries. Have a good day!'

            else:
                output = 'Hi there! I am your fully autonomous digital assistant. Type /priv "message" to get started. Ask me "what\'s new?"'

            await bot.chat.send(channel, output)


listen_options = {
    "local": True,
    "wallet": True,
    "dev": True,
    "hide-exploding": False,
    "filter_channel": None,
    "filter_channels": None,
}

key_file = open("paperkey.txt", "r+")

bot = Bot(
    username="botnow", paperkey=key_file.read(), handler=Handler()
)

asyncio.run(bot.start(listen_options))

# Improvments:
# -format for the 'most commonly refers to:'
# - get rid of the [1], etc
