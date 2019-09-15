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

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import ephem
import datetime


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO,
                    filename='bot.log'
                    )


PLANETS = {
    'mercury' : 'Меркурий',
    'venus' : 'Венера',
    'mars' : 'Марс',
    'jupiter' : 'Юпитер',
    'saturn' : 'Сатурн',
    'uranus' : 'Уран',
    'neptune' : 'Нептун',
    'pluto' : 'Плутон',
}


def print_start_text(bot, update):
    text = (
        'Вызван /start\n'
        'Наберите /planet и название планеты на английском для того, чтобы узнать в каком созвездии находится планета\n'
        'Наберите /help чтобы узнать названия планет на Английском\n'
    )   
    update.message.reply_text(text)


def print_planets_list(bot, update):
    text = '\n'.join([f'{name} - {eng_name.capitalize()}' for eng_name, name in PLANETS.items()])
    update.message.reply_text(text)


def show_planet_constellation(bot, update):
    query_params = update.message.text.split()
    try:
        selected_planet = query_params[1].lower()
        if PLANETS.get(selected_planet):
            date = datetime.date.today()

            f = getattr(ephem, selected_planet.capitalize())
            constellation_name = ephem.constellation( f(date) )

            text = (
                f'Вы выбрали планету - {PLANETS.get(selected_planet)}\n'
                f'На сегодняшнюю дату ({date}) планета находится в созвездии: {constellation_name}'
            )
        else:
            text = (
                'Планета не выбрана или указана несуществующая планета\n'
                'Пожалуйста, воспользуйтесь коммендой /help для просмотра списка поддерживаемых планет'
            )          
    except AttributeError:
        text = (
            'Нет данных по выбраной планете\n'
            'Пожалуйста, воспользуйтесь коммендой /help для просмотра списка поддерживаемых планет'
        )
    except IndexError:
        text = (
            'Вы вызвали комманду /planet без параметров\n'
            'Пожалуйста, воспользуйтесь коммендой /help для просмотра списка поддерживаемых планет'
        )

    update.message.reply_text(text)


def talk_to_me(bot, update):
    user_text = f"Привет, {update.message.chat.first_name}! Ты написал: " + update.message.text
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                     update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)


def main(): 
    mybot = Updater (settings.API_KEY, request_kwargs=settings.PROXY )

    logging.info('Бот запускается')
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", print_start_text))
    dp.add_handler(CommandHandler("help", print_planets_list))
    dp.add_handler(CommandHandler("planet", show_planet_constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


main()
