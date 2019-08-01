#!/usr/bin/env python

"""
Magic 8 Ball Bot will predict you future as real magic 8 ball.

Say ``/start`` and go!
"""

import telebot
import time
import random
import os
# from telebot import apihelper

# define metadata
__version__     = "1.0.0"
__author__      = "Vladimir Saltykov"
__copyright__   = "Copyright 2019, %s" % __author__
__email__       = "vowatchka@mail.ru"
__license__     = "MIT"
__date__        = "2019-08-01"

# proxy settings
# apihelper.proxy = {
	# "https": "https://46.20.9.187:181"
# }

# bot settings
lang = None
LANG_RU = "ru"
LANG_EN = "en"

# phrases
# ball answers were be kepped from https://ru.wikipedia.org/wiki/Magic_8_ball
PHRASES = {
	"welcome": "Hi! I'm Magic 8 Ball. Select you lang, please...", 
	"unknown_lang": "Sorry. I don't know this language", 
	"selected_lang": {
		"ru": "Отлично! Ты выбрал русский язык", 
		"en": "All right! You language is English", 
	}, 
	"offer_to_ask": {
		"ru": "А теперь я предскажу твое будущее. Спрашивай о чем хочешь...", 
		"en": "Now I will predict you future. You can ask me about everything...", 
	}, 
	"positive": {
		"ru": ["Бесспорно", "Предрешено", "Никаких сомнений", "Определённо да", "Можешь быть уверен в этом"], 
		"en": ["It is certain", "It is decidedly so", "Without a doubt", "Yes — definitely", "You may rely on it"], 
	}, 
	"hesitantly_positive": {
		"ru": ["Мне кажется — «да»", "Вероятнее всего", "Хорошие перспективы", "Знаки говорят — «да»", "Да"], 
		"en": ["As I see it, yes", "Most likely", "Outlook good", "Signs point to yes", "Yes"], 
	}, 
	"neutral": {
		"ru": ["Пока не ясно, попробуй снова", "Спроси позже", "Лучше не рассказывать", "Сейчас нельзя предсказать", "Сконцентрируйся и спроси опять"], 
		"en": ["Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again"], 
	},
	"negative": {
		"ru": ["Даже не думай", "Мой ответ — «нет»", "По моим данным — «нет»", "Перспективы не очень хорошие", "Весьма сомнительно"], 
		"en": ["Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"], 
	}, 
}

# phrase types
PHRASE_TYPES = ["positive", "hesitantly_positive", "neutral", "negative"]

# get token
TG_TOKEN = os.environ["TOKEN"]

# bot
magic8ballbot = telebot.TeleBot(TG_TOKEN)

def create_lang_keyboard():
	# create keyboard
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
	
	# create keyboard buttons
	ru_btn = telebot.types.KeyboardButton(text="Русский")
	en_btn = telebot.types.KeyboardButton(text="English")
	
	# add buttons to keyboard
	keyboard.add(ru_btn, en_btn)
	
	return keyboard

def drop_bot_settings():
	global lang
	lang = None
	
def select_lang(message):
	global lang
	if message.text.lower() == "русский":
		lang = LANG_RU
	elif message.text.lower() == "english":
		lang = LANG_EN
	else:
		magic8ballbot.send_message(message.from_user.id, PHRASES["unknown_lang"], reply_markup=keyboard)
		return
	
	# reply and hide keyboard
	magic8ballbot.send_message(message.from_user.id, PHRASES["selected_lang"][lang], reply_markup=telebot.types.ReplyKeyboardRemove())
	magic8ballbot.send_message(message.from_user.id, PHRASES["offer_to_ask"][lang])
	
def predict_future(message):
	phrase_type = PHRASE_TYPES[random.randint(0, len(PHRASE_TYPES)-1)]
	predective_phrases = PHRASES[phrase_type][lang]
	magic8ballbot.send_message(message.from_user.id, predective_phrases[random.randint(0, len(predective_phrases)-1)])
	
@magic8ballbot.message_handler(commands=["start"])
def start_bot(message):
	drop_bot_settings()
	# show keyboard
	magic8ballbot.send_message(message.from_user.id, PHRASES["welcome"], reply_markup=keyboard)
	
@magic8ballbot.message_handler()
def get_message(message):
	if not lang:
		select_lang(message)
	else:
		predict_future(message)
	
keyboard = create_lang_keyboard()
try:
	magic8ballbot.polling(none_stop=True, interval=0)
except Exception as ex:
	time.sleep(5)
	print("Internet error!")
	print(ex)