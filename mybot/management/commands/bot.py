from django.core.management.base import BaseCommand, CommandError
import os
import telebot
import traceback
from django.utils import timezone
from telebot import types

from mybot.models import TelegramUser

bot = telebot.TeleBot(os.getenv('TELEGRAMKEY'))


@bot.message_handler(commands=['start'])
def start_command(message):

    try:
        TelegramUser.objects.create(first_name=message.json['from'].get('first_name', '-'),
                                    last_name=message.json['from'].get('last_name', '-'),
                                    chat_id=message.from_user.chat_id,
                                    last_message=timezone.now()
                                    )
    except:
        print(traceback.format_exc())
        
    bot.send_message(message.chat.id, 'Доброго дня, я бот програми Weld Calculator', reply_markup=main_key)


main_key = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
main_key.add(types.KeyboardButton(text='Про програму'), types.KeyboardButton(text='Контакти'), types.KeyboardButton(text='Розвиток проекта'))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == 'Про програму':
        info_prog(message.chat.id)
    elif message.text == 'Контакти':
        info_prog_2(message.chat.id)
    elif message.text == 'Розвиток проекта':
        info_prog_3(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Оберіть варіанти')


def info_prog(chatid):
    kbd = types.InlineKeyboardMarkup()
    kbd.add(types.InlineKeyboardButton(text='Інфо', callback_data='1'))
    kbd.add(types.InlineKeyboardButton(text='Завантажити', callback_data='2'))
    kbd.add(types.InlineKeyboardButton(text='Версія', callback_data='3'))
    bot.send_message(chatid,'''Оберіть пункт''', reply_markup=kbd)

def info_prog_2(chatid):
    kbd = types.InlineKeyboardMarkup()
    kbd.add(types.InlineKeyboardButton(text='Електронна скринька', callback_data='4'))
    kbd.add(types.InlineKeyboardButton(text='Телефон', callback_data='5'))
    kbd.add(types.InlineKeyboardButton(text='Адреса', callback_data='6'))
    bot.send_message(chatid,'''Оберіть пункт''', reply_markup=kbd)

def info_prog_3(chatid):
        kbd = types.InlineKeyboardMarkup()
        kbd.add(types.InlineKeyboardButton(text='Долучитися до проекту', callback_data='7'))
        kbd.add(types.InlineKeyboardButton(text='Підтримка проекта', callback_data='8'))
        bot.send_message(chatid, '''Оберіть пункт''', reply_markup=kbd)

@bot.callback_query_handler(func=lambda m: True)
def info_answer(message):
    print(message.data)
    if message.data == '1':
        bot.send_message(message.from_user.id, 'Дана програма створена для полегшення вибору розмірів зварки в залежності від товщини зварювальної пластини.')
    elif message.data == '2':
        bot.send_message(message.from_user.id, 'Посилання')
    elif message.data == '3':
        bot.send_message(message.from_user.id, 'Версія 1.0')
    elif message.data == '4':
            bot.send_message(message.from_user.id, 'filatov.f@ukr.net')
    elif message.data == '5':
            bot.send_message(message.from_user.id, '0676303828')
    elif message.data == '6':
            bot.send_message(message.from_user.id, 'м.Львів вул.Городоцька 13')
    elif message.data == '7':
        bot.send_message(message.from_user.id, 'Ви можете прийняти участь у розробці чи в тестуванні даного проекта. Для цього напишіть нам на пошту або зателефонуйте')
    elif message.data == '8':
        bot.send_message(message.from_user.id, 'Ви також можете фінансово підтримати проект. Номер карти 999999999')






class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print('i comand')
        bot.infinity_polling()
