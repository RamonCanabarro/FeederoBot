import sqlite3
import json
import sys
import time
import telepot
import feedparser
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


 
def on_list_command(msg):   
        conn=sqlite3.connect('feed.db')
        text, chat_type, chat_id = telepot.glance(msg)
        bot = telepot.Bot(TOKEN)

        sql = 'SELECT link FROM feed WHERE user = ?'
        curs = conn.cursor()
        id = (chat_id,)
        curs.execute(sql,id)

        exist = (curs.fetchall())

        if(not exist):
            bot.sendMessage('Não há registros.')
        else:
            cont = 0
            for post in exist:
                cont+=1            
                bot.sendMessage(chat_id,  (str(cont)+ " ---- " + json.dumps(post)))


def on_delete_command(msg):
    conn = sqlite3.connect('feed.db')
    text, chat_type, chat_id = telepot.glance(msg)
    bot = telepot.Bot(TOKEN)
    bot.sendMessage(chat_id, 'Selecione o feed enviando o número a ser removido.')
    on_list_command(msg)
    link = bot.getUpdates()

    while (not link):
        link = bot.getUpdates()

    rmo =  (int(link[0]['message']['text'])-1)
    sql = 'SELECT link FROM feed WHERE user = ?'

    curs = conn.cursor()
    id = (chat_id,)
    curs.execute(sql, id)
    exist = (curs.fetchall())    

    curs = conn.cursor()
    sql= 'DELETE FROM feed WHERE user = ? AND link = ?'
    params  = (chat_id,exist[rmo][0])
    print (str(exist[rmo]))
    print (params)
    curs.execute(sql, params)
    conn.commit()
    conn.close()

def on_chat_message(msg):
    conn=sqlite3.connect('feed.db')
    text, chat_type, chat_id = telepot.glance(msg)
    bot = telepot.Bot(TOKEN)
    link = bot.getUpdates()
    feed =  (link[0]['message']['text'])

    # READS AND REDIRECTS ALL COMMANDS GIVEN --------------------------------------------------------
    if ('/' in  feed):
        mensagem = (feed[1:8])        
        if(mensagem == 'listar'):
            on_list_command(msg)
        elif(mensagem == 'remover'):    
            on_delete_command(msg)    

    noticia = feedparser.parse(feed)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Clique aqui para mais', callback_data='press')],
               ])
    sql = 'SELECT user,link FROM feed WHERE user = ?'
    curs = conn.cursor()
    id = (chat_id,)
    curs.execute(sql, id)
    exist = (curs.fetchone()) #Futuramente receber array de resultados

    if ((not exist) or ((exist[0] == str(chat_id)) and (exist[1] != feed) )):
      for post in range(3):
        bot.sendMessage(chat_id, noticia.entries[post].title + ": " + noticia.href + "")    
      sql = ''' INSERT INTO feed(titulo,descricao,link,user) VALUES(?,?,?,?)'''
    else:
        
        bot.sendMessage(chat_id, noticia.entries[0].title + ": " + noticia.entries[0].link + "")
        sql='''UPDATE feed set titulo=?, descricao=?, link=? where user=?'''
    
    print ('--------------------------------------------------------------------------------------')
    print (noticia['href'])
    params =  (noticia['href'],noticia.entries[0].title, noticia['href'], chat_id)   



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
    
    
TOKEN = 'TOKEN'  # get token from command-line

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')



while 1:
    time.sleep(10)