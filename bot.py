import sqlite3
import sys
import time
import telepot
import feedparser
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def on_chat_message(msg):
    conn=sqlite3.connect('feed.db')

    content_type, chat_type, chat_id = telepot.glance(msg)

    noticia = feedparser.parse('http://www.criptomoedasfacil.com/feed/')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Clique aqui para mais', callback_data='press')],
               ])

    bot.sendMessage(chat_id, 'Novas notícias',reply_markup=keyboard )
    for post in range(3):
      bot.sendMessage(chat_id, noticia.entries[post].title + ": " + noticia.entries[post].link + "")


    params =  (noticia['feed']['title'],noticia.entries[0].title, noticia['feed']['link'], chat_id, 0)
    sql = ''' INSERT INTO feed(titulo,descricao,link,user, is_first_post)
              VALUES(?,?,?,?,?)'''
    curs = conn.cursor()
    curs.execute(sql,params)
    conn.commit()
    conn.close()

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='chat')
    print('Callback Query:', query_id, from_id, query_data)

    noticia = feedparser.parse('http://www.criptomoedasfacil.com/feed/')
    print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text=noticia['feed']['title'])
    
    
TOKEN = ''  # get token from command-line

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')



while 1:
    time.sleep(10)
