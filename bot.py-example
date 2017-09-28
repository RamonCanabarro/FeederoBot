import sys
import time
import telepot
import feedparser
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    noticia = feedparser.parse('http://www.criptomoedasfacil.com/feed/')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Clique aquipara mais', callback_data='press')],
               ])

    bot.sendMessage(chat_id, 'Novas notícias',reply_markup=keyboard )
   

def on_callback_query(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    noticia = feedparser.parse('http://www.criptomoedasfacil.com/feed/')
      
    for post in range(3):
      bot.sendMessage(chat_id, noticia.entries[post].title + ": " + noticia.entries[post].link + "")

    
TOKEN = TOOOOKEN  # get token from command-line

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')



while 1:
    time.sleep(10)
