import logging
from aiogram import Bot, Dispatcher, executor, types
from db import Database
import markups as nav

logging.basicConfig(level=logging.INFO)

bot = Bot(token="5902092559:AAEwLnFd-eRbZZU0Etcw_zHbl-dUDx6TU6E")
dp = Dispatcher(bot)
db = Database('database.db')

@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    if message.chat.type == "private":
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, "Вы успешно зарегестрировались")
        else:
            await bot.send_message(message.from_user.id, "Вы уже зарегестрированы, ждите рассылки от вашего любимейшего университета )")





@dp.message_handler(commands = ['sendall'])
async def start(message: types.Message):
    if message.chat.type == "private":
        if message.from_user.id == 975225841:
            text = message.text[9:]

            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)

                await bot.send_message(message.from_user.id, "Успешная рассылка")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)