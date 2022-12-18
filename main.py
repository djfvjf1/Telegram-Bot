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
            await bot.send_message(message.from_user.id, "Введите имя")
            await bot.send_message(message.from_user.id, "Введите email")
        else:
            await bot.send_message(message.from_user.id, "Вы уже зарегестрированы", reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Профиль':
            pass
        else:
            if db.get_signup(message.from_user.id) == "setname":
                if(len(message.text) > 50):
                    await bot.send_message(message.from_user.id, "Имя не может превышать 50 символов")
                else:
                    db.set_name(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "done", "Вы успешно зарегистрировались")


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