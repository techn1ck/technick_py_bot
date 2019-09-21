"""
Домашнее задание

Научите бота играть в города. 

Правила такие - внутри бота есть список городов, 
пользователь пишет /cities Москва и если в списке такой город есть, 
бот отвечает городом на букву "а" - "Альметьевск, ваш ход". 
 
Оба города должны удаляться из списка.

Помните, с ботом могут играть несколько пользователей одновременно

"""

from glob import glob
import logging
from random import choice, randint

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO,
                    filename='bot.log'
                    )

        
def print_start_text(bot, update, user_data):
    get_user_emo(user_data)
    
    user_data['cities'] = get_cities_list()
    user_data['used_cities'] = []
    user_data['current_bot_city'] = ''
    
    text = (
        f'Игра в города, {user_data["emo"]}\n'
        f'Напишите любой город России: \n'
        f'если город оканчивается на мягкий знак, то берется предпоследняя буква \n'
    )

    update.message.reply_text(text, reply_markup=get_keyboard())

    

def name_the_city(bot, update, user_data):
    city = update.message.text.strip().title()
    
    if not user_data['cities']:
        user_data['cities'] = get_cities_list()

    if city in user_data['cities']:
        user_data['cities'].remove(city)
        user_data['used_cities'].append(city)
        last_letter = city.replace('ь', '')[-1].upper()
        try:
            cities = [x for x in user_data['cities'] if x.startswith(last_letter)]
            user_data['current_bot_city'] = cities[ randint(0, len(cities)-1) ]
            user_data['cities'].remove( user_data['current_bot_city'] )
            user_data['used_cities'].append( user_data['current_bot_city'] )
            text = f"{user_data['current_bot_city']}, ваш ход"
        except ValueError:
            text = (
                f'Больше нет городов на букву "{last_letter}"\n'
                f'Начинаем игру заново\n'
                f'Введите город:\n'
            )
            user_data['cities'] = get_cities_list()
            user_data['used_cities'] = []
            user_data['current_bot_city'] = ''
    elif city in user_data['used_cities']:
        text = f'Город "{city}" уже использовался'
    else:
        text = f'Нет такого города "{city}", введите другой'

    update.message.reply_text(text, reply_markup=get_keyboard())

    

def let_bot_name_the_city(bot, update, user_data):
    if not user_data['cities']:
        user_data['cities'] = get_cities_list()

    if user_data['current_bot_city']:
        last_letter = user_data['current_bot_city'].replace('ь', '')[-1].upper()
        try:
            cities = [x for x in user_data['cities'] if x.startswith(last_letter)]
            user_data['current_bot_city'] = cities[ randint(0, len(cities)-1) ]
            user_data['cities'].remove( user_data['current_bot_city'] )
            user_data['used_cities'].append( user_data['current_bot_city'] )
            text = f"{user_data['current_bot_city']}, ваш ход"
        except ValueError:
            text = (
                f'Больше нет городов на букву "{last_letter}"\n'
                f'Начинаем с начала\n'
                f'Введите город:\n'
            )
            user_data['cities'] = get_cities_list()
            user_data['used_cities'] = []
            user_data['current_bot_city'] = ''
    else:
        user_data['current_bot_city'] = choice(user_data['cities'])
        user_data['cities'].remove( user_data['current_bot_city'] )
        user_data['used_cities'].append( user_data['current_bot_city'] )
        text = f"{user_data['current_bot_city']}, ваш ход"
    
    update.message.reply_text(text, reply_markup=get_keyboard())



def get_cities_list():
    with open('cities.txt', 'r', encoding='utf-8') as f:
        return [x.strip() for x in f]

        

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']



def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup(  [
                                            ['Начать сначала', 'Пусть бот придумает город'],
                                        ], resize_keyboard=True
                                    )
    return my_keyboard


 
def main(): 
    mybot = Updater (settings.API_KEY, request_kwargs=settings.PROXY )

    logging.info('Бот запускается')
   
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", print_start_text, pass_user_data=True))

    dp.add_handler(RegexHandler('^(Начать сначала)$', print_start_text, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Пусть бот придумает город)$', let_bot_name_the_city, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, name_the_city, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()



if __name__ == '__main__':
    main()
