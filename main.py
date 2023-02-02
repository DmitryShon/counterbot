from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from utils import check_acc_valid
from checker import *
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from sqlighter import SQLighter

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = SQLighter('db.db')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(f'Привет {message.from_user["first_name"]}! \nДобро пожаловать в моего кривого бота по подсчету транзакций\nЧтобы ознакомиться с функциями напиши /help')
    if not db.check_user_in_db(message.from_user['id']):
        db.add_user(message.from_user['id'])
        await message.reply( f'Вы были добавлены в базу данных')

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Принцип работы бота: он проходит по транзакциям, начиная с самой последней пока не встретит особую. "
                        "Под особой понимается транзакция отправки монет на мой кошелек _dimees.near_ или конкретный TXid(hash) транзакции."
                        "То есть бот не будет работать *не* на моем акке, если вы явно не указали ему ДО КУДА ему считать, отправив номер транзакции. \n\n"
                        "Чтоб запустить его в обычном режиме, просто напиши ник аккаунта, который хочешь считать. Пример: _dimees.near_.\n"
                        "Если не сработало, попробуй в режиме остановки по транзакции:\n _dimees.near_ Номертранзакции (через 1 пробел)", parse_mode="Markdown")

@dp.message_handler(commands=['my_accounts'])
async def process_accounts_command(msg: types.Message):
    # await message.reply('Прив',reply_markup=keyboard)
    keyboard = ReplyKeyboardMarkup()
    button_list = [KeyboardButton(text=x, callback_data=x) for x in db.show_accounts(msg.from_user['id'])]
    keyboard.add(*button_list)
    await bot.send_message(msg.from_user.id,'Введи аккаунт', reply_markup=keyboard)

@dp.message_handler(commands=['add'])
async def add_account(msg: types.Message):
    accs = msg.text.split()[1:]
    valid_accs = []
    for acc in accs:
        if await check_acc_valid(acc):
            if db.add_account(acc, msg.from_user['id']):
                valid_accs.append(acc)
    if len(valid_accs)>0:
        await bot.send_message(msg.from_user.id, 'Добавлены аккаунты\n'+ '\n'.join(valid_accs))
    else:
        await bot.send_message(msg.from_user.id, 'Ни один из введенных аккаунтов не оказался существующим или уже был добавлен.')


@dp.message_handler(commands=['del'])
async def del_account(msg: types.Message):
    accs = msg.text.split()[1:]
    valid_accs = []
    for acc in accs:
        if await check_acc_valid(acc):
            db.del_account(acc, msg.from_user['id'])
            valid_accs.append(acc)
    if len(valid_accs)>0:
        await bot.send_message(msg.from_user.id, 'Удалены аккаунты\n'+ '\n'.join(valid_accs))
    else:
        await bot.send_message(msg.from_user.id, 'Вы ввели несуществующий аккаунт')

@dp.message_handler()
async def echo_message(msg: types.Message):
    data = msg.text.split()
    if await check_acc_valid(data[0]):
        await bot.send_message(msg.from_user.id, await get_result(data), parse_mode="html")
    else:
        await bot.send_message(msg.from_user.id, 'Такой аккаунт не найден. Попробуй еще раз')


if __name__ == '__main__':
    executor.start_polling(dp)