"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход 
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите 
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите 
  бота отвечать, в каком созвездии сегодня находится планета.

"""

from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO,
                    filename='bot.log'
                    )


def print_start_text(bot, update, user_data):
    emo = get_user_emo(user_data)
    text = (
        f'Вызван /start\n {user_data["emo"]}'
    )
    update.message.reply_text(text, reply_markup=get_keyboard())


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    random_cat = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(random_cat, 'rb'), reply_markup=get_keyboard())


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    text = (
        f'Новая аватарка\n {user_data["emo"]}'
    )
    update.message.reply_text(text, reply_markup=get_keyboard())
    

def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = f"Привет, {update.message.chat.first_name}! {emo} Ты написал: " + update.message.text
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                     update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def get_contact(bot, update, user_data):
    print(update.message.contact)
    user_text = f"Спасибо, {update.message.chat.first_name}! {get_user_emo(user_data)}"
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    print(update.message.location)
    user_text = f"Спасибо, {update.message.chat.first_name}! {get_user_emo(user_data)}"
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать локацию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup(  [
                                            ['Прислать котика', 'Изменить аватарку'],
                                            [contact_button, location_button],
                                        ] 
                                    )
    return my_keyboard

 
def main(): 
    mybot = Updater (settings.API_KEY, request_kwargs=settings.PROXY )

    logging.info('Бот запускается')
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", print_start_text, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))

    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Изменить аватарку)$', change_avatar, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
