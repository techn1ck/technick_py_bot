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


planets = {
    'mercury' : 'Меркурий',
    'venus' : 'Венера',
    'mars' : 'Марс',
    'jupiter' : 'Юпитер',
    'saturn' : 'Сатурн',
    'uranus' : 'Уран',
    'neptune' : 'Нептун',
    'pluto' : 'Плутон',
}

# start command
def greet_user(bot, update):
    text = 'Вызван /start \n' 
    text += 'Наберите /planet и название планеты на английском для того, чтобы узнать в каком созвездии находится планета\n'
    text += 'Наберите /help чтобы узнать названия планет на Английском\n'
#   logging.info(text)
    update.message.reply_text(text)


# help command
def help_user(bot, update):
    text = str()
    for eng_name, name in planets.items():
        text += f'{name} - {eng_name.capitalize()}\n'
    update.message.reply_text(text)


# planet command
def show_planet_constellation(bot, update):
    planet = update.message.text.split()
    try:         
        if planets.get(planet[1].lower()):
            date = datetime.date.today()

            f = getattr(ephem, planet[1].lower().capitalize())
            constellation_name = ephem.constellation( f(date) )

            text = f'Вы выбрали планету - {planets.get(planet[1].lower())}\n'
            text += f'На сегодняшнюю дату ({date}) планета находится в созвездии: {constellation_name}'
        else:
            text = 'Планета не выбрана или указана несуществующая планета\n'
            text += 'Пожалуйста, воспользуйтесь коммендой /help для просмотра списка поддерживаемых планет'
    except AttributeError:
        text = 'Нет данных по выбраной планете\n'
        text += 'Пожалуйста, воспользуйтесь коммендой /help для просмотра списка поддерживаемых планет'
    except IndexError:
        text = 'Вы вызвали комманду /planet без параметров\n'
        text += 'Пожалуйста, воспользуйтесь коммендой /help для просмотра списка поддерживаемых планет'

    update.message.reply_text(text)


# message handler
def talk_to_me(bot, update):
    user_text = f"Привет, {update.message.chat.first_name}! Ты написал: " + update.message.text
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                     update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)


# сonnection
def main(): 
    mybot = Updater (settings.API_KEY, request_kwargs=settings.PROXY )

    logging.info('Бот запускается')
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("help", help_user))
    dp.add_handler(CommandHandler("planet", show_planet_constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


# run
main()
