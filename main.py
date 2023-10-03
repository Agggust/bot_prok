import telebot
from telebot.types import KeyboardButton

import config

from db import *
from telebot import types
from newsapi import NewsApiClient
bot = telebot.TeleBot(config.token)
newsapi = NewsApiClient(api_key=config.api)

#приветствие
@bot.message_handler(commands=['start'])
def welcome(message):
  text = 'Вы уже зарегистрированы'
  user_id = message.chat.id
  user = getUser(user_id)
  print(user)

  if getUser(user_id) == None:
    insertUser(user_id)
    text = f"{message.from_user.first_name}, вы зарегистрированы\n Что нужно?"

  sti = open('static/dog_with_burger.webp', 'rb')

  #keybords
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

  itemNews = types.KeyboardButton('Новости 📰')
  itemSubs = types.KeyboardButton('Мои подписки 📬')
  itemCats = types.KeyboardButton('Категории 🧧')

  markup.add(itemCats, itemNews, itemSubs)

  bot.send_sticker(message.chat.id, sti)
  bot.reply_to(message, text,  reply_markup=markup)

# def makeButtons( arrObj, text = ''):
#   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#   for i in arrObj:
#     markup.add(types.KeyboardButton(f"{text} {i[0]}"))
#
#   return markup

@bot.message_handler(content_types=['text'])
def work_bot(message):
  if message.chat.type == 'private':

    user_id = message.chat.id
    subs_user = getSubUser(user_id)
    categs = []
    for i in subs_user:
      categs.append(i[0])
    print(categs)
    # for i in subs_user:
    #   print(i)
    if message.text == 'Категории 🧧':
      cats = getCategories()
      menu = types.KeyboardButton('Основное меню')
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.add(menu)
      for i in cats:
        print(type(i[0]))
        markup.add(types.KeyboardButton(f"Подписаться на {i[0]}"))

      bot.reply_to(message, 'вот все категории',  reply_markup=markup)

    if message.text.startswith('Подписаться на'):
      cat = message.text[15:]
      cat_id = getIdCat(cat)[0]

#проверка что еще не подписан пока нет
      if isSub(user_id, cat_id) == None:
        insertSub(user_id,cat_id)
        text = f"Вы успешно подписаны на {cat}"
      else:
        text = f"Вы уже подписаны на {cat}"

      bot.reply_to(message, text)

    if message.text == 'Основное меню':
      # keybords
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

      itemNews = types.KeyboardButton('Новости 📰')
      itemSubs = types.KeyboardButton('Мои подписки 📬')
      itemCats = types.KeyboardButton('Категории 🧧')

      markup.add(itemCats, itemNews, itemSubs)

      bot.reply_to(message, "Что нужно?", reply_markup=markup)
    #мои подписки
    if message.text == 'Мои подписки 📬':

      subs = getSubUser(user_id)
      menu = types.KeyboardButton('Основное меню')
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.add(menu)
      for i in subs:
        print(type(i[0]))
        markup.add(types.KeyboardButton(f"Отписаться от {i[0]}"))

      bot.reply_to(message, 'вот все подписки', reply_markup=markup)

    if message.text.startswith('Отписаться от'):
      sub = message.text[14:]
      cat_id = getIdCat(sub)
      print(cat_id)
      if isSub(user_id, cat_id) == None:
        text = f"Вы еще не подписаны на {sub}"
        bot.reply_to(message, text)
      else:
        delSub(user_id, cat_id)
        subs = getSubUser(user_id)
        menu = types.KeyboardButton('Основное меню')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(menu)
        for i in subs:
          print(type(i[0]))
          markup.add(types.KeyboardButton(f"Отписаться от {i[0]}"))
        bot.reply_to(message, f"Вы успешно отписаны от {sub}", reply_markup=markup)

    if message.text == 'Новости 📰':

      for a in categs:
        print(a)
        top_headlines = newsapi.get_top_headlines(category=f'{a}', language='ru', country='ru', page=1, page_size=3)
        print(top_headlines)
        i = 0
        while i<len(top_headlines):
          bot.send_message(message.chat.id,f'Категория:{a}\n {top_headlines["articles"][i]["title"]}\n {top_headlines["articles"][i]["url"]}')
          i=i+1


# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#   bot.reply_to(message, "Howdy, how are you doing?",)
#
#
# @bot.message_handler(commands=['help'])
# def send_welcome(message):
#   bot.reply_to(message,  message.from_user.first_name + " " + message.from_user.first_name + ", тебе нужна помощь",)
#
#
bot.infinity_polling()