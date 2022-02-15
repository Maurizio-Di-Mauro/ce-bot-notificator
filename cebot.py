import os, logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import account_reader
import utils


bot = Bot(token=os.environ['TOKEN'])
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    print('The bot is online')
    await log_to_admin('The bot is online')

async def log_to_admin(text: str):
    await bot.send_message(os.environ['ADMIN_ID'], text, disable_notification=False)

async def send_message(user_id: int, text: str, disable_notification: bool = False):
    bots_msg = await bot.send_message(user_id, text, disable_notification=disable_notification)
    await bots_msg.chat.pin_message(bots_msg.message_id)

async def send_money_collected(chat_id: int):
    money_collected, money_needed = account_reader.scrap_from_web(os.environ['CE_CLUB_URL'])
    message_creator = utils.MessageCreator(money_collected, money_needed)
    if message_creator.should_notify():
        await send_message(chat_id, message_creator.create_message())
    else:
        await log_to_admin(f"Money collected: {money_collected}\nMoney needed: {money_needed}")
        await log_to_admin(f"Days left: {message_creator.days_left}")

executor.start(dp, send_money_collected(os.environ['CHAT_ID']), skip_updates=True, on_startup=on_startup)