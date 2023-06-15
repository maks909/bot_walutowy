import telebot
import requests
from telebot import types
import time
import json

with open("mowa_botu.json", "r", encoding="utf-8") as p:
    mowa_botu = json.load(p)
p.close()

#Spetial thank's for flaticon.com for it's icons

plik = open("TOKEN.ini")
TOKEN = plik.read()
plik.close()

bot = telebot.TeleBot(TOKEN)
OPENEXCHANGE_API_KEY = "9c157b50feae410d85148894079c06ca"

currencies = ("USD", "EUR", "PLN", "RUB", "BYN", "GBP", "CNY", "CHF", "UAH", "JPY")

currensy_pictures = {"USD":"https://telegra.ph/file/229e7bc4ef6f23d127cc3.png", "EUR":"https://telegra.ph/file/abd077de4d9ab557c77b8.png", "PLN":"https://telegra.ph/file/45d7c30e714afa69f8e36.png", "RUB":"https://telegra.ph/file/564592554d733e6e29724.png", "BYN":"https://telegra.ph/file/93a67e8a5a62a18354b3e.png", "GBP":"https://telegra.ph/file/6e99f7dcf172b7b802ffb.png", "CNY":"https://telegra.ph/file/ed8cec61f2943bcfb9f5a.png", "CHF":"https://telegra.ph/file/e672f46428eb3612c8311.png", "UAH":"https://telegra.ph/file/20d4d140fa6cc5b7deb1f.png", "JPY":"https://telegra.ph/file/0ed34d05c60533bc85eb2.png"}

number_pictures = {1:"https://telegra.ph/file/31f2b3d588e89638e5c20.png", 5:"https://telegra.ph/file/8e5155ea17c4eef7c0f11.png", 10:"https://telegra.ph/file/3f3b2e0d83d82dd1b69a2.png", 20:"https://telegra.ph/file/2f43f402eb5054de068b9.png", 50:"https://telegra.ph/file/864c79280630d1e6837ae.png", 100:"https://telegra.ph/file/7b284263ea92b9ca95cef.png"}

@bot.message_handler(commands=["start"])#" Jestem botem do pomocy w napisaniu walut. \n Możesz mnie zawołać w każdym czacie z pomocą @currency_rate_help_bot I nazw walut. \n Dowiesz się więcej jeżeli napiszesz /help.")
def początek(m):
    bot.send_message(m.chat.id, mowa_botu["chat"]["start"])

@bot.message_handler(commands=["help"])
def pomoc(m):
    bot.send_message(chat_id=m.chat.id, text=mowa_botu["chat"]["help"]["początek"])
    bot.send_message(chat_id=m.chat.id, text=mowa_botu["chat"]["help"]["opowiadanie"])
    bot.send_message(chat_id=m.chat.id, text=mowa_botu["chat"]["help"]["przykłady"])

import random

gra_działa=False
@bot.message_handler(commands=["game"])
def game(m):
    global gra_działa
    gra_działa = True
    bot.send_message(chat_id=m.chat.id, text="Zagrajmy w grę \"odgadnij kurs waluty\". \n Musisz odgadnąć kurs dowolnej pary walut.")
    any_walutes_function("USD", "EUR")
    global pierwsza_waluta
    global druga_waluta
    pierwsza_waluta = random.choice(lista_walut)
    druga_waluta = random.choice(lista_walut)
    bot.send_message(chat_id=m.chat.id, text=f"Ogadnij kurs walut {pierwsza_waluta} i {druga_waluta}")

@bot.message_handler(content_types=["text"])
def zapis_liczby(m):
    global gra_działa
    if gra_działa:
        global user_hint
        user_hint = float(m.text)
        prawdziwy_kurs = round(any_walutes_function(pierwsza_waluta, druga_waluta), 2)
        if abs(user_hint - prawdziwy_kurs) < 0.5:
            bot.send_message(chat_id=m.chat.id, text=f"Dobrze odgadnełeś, gratulacje!!\nPrawdziwy kurs to: {prawdziwy_kurs}")
        else:
            bot.send_message(chat_id=m.chat.id, text=f"Trochę się nie udało!\nPrawdziwy kurs to: {prawdziwy_kurs}.")

@bot.inline_handler(lambda query: query.query)
def query_text(query):
    # Dzielimy otrzymane w żądaniu informacje
    req = query.query.upper().split()
    if len(req) == 1:
        scr = req[0]
        if not scr in currencies:
            komunikat_o_błędzie(query)
            return
        one_curency(scr, query)
    elif len(req) == 2 and isnumeric(req[0]):
        number, scr = req
        if not scr in currencies:
            komunikat_o_błędzie(query)
            return
        one_curency_with_number(scr, float(number), query)
    elif len(req) == 2 and isnumeric(req[1]):
        scr, number = req
        if not scr in currencies:
            komunikat_o_błędzie(query)
            return
        one_curency_with_number(scr, float(number), query)
    elif len(req) == 2:
        scr, tgt = req
        if not scr in currencies or not tgt in currencies:
            komunikat_o_błędzie(query)
            return
        two_curencies(scr, tgt, query)
    elif len(req) == 3 and isnumeric(req[2]):
        scr, tgt, number = req
        if not scr in currencies or not tgt in currencies:
            komunikat_o_błędzie(query)
            return
        two_curencies_with_number(scr, tgt, float(number), query)
    else:
        komunikat_o_błędzie(query)
        return


    # Zapisujemy adres żądania do API
    #url = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGE_API_KEY}&base={scr}&symbols={tgt}"
    # Wysłanie żądania GET do API
    #response = requests.get(url)
    # Parsing (rozszyfrowanie) otrzymanej odpowiedzi
    #rate = response.json()['rates'][tgt]
    #bot.answer_inline_query(query.id, [article_1, article_5, article_10, article_20, article_50, article_100])

@bot.inline_handler(lambda query: len(query.query) == 0)
def empty_query(query):
    hint = mowa_botu["inline"]["hint"]["text"]
    try:
        r = types.InlineQueryResultArticle(
                id="12",
                title=mowa_botu["inline"]["hint"]["title"],
                description=hint,
                input_message_content=types.InputTextMessageContent(
                message_text=mowa_botu["inline"]["hint"]["no_tekst_messege"],
                parse_mode="Markdown")
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)

# def any_walutes_function(cur1, cur2):
#     url2 = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGE_API_KEY}&base=USD&symbols={cur2}"

#     response = requests.get(url2)

#     rate2 = response.json()['rates'][cur2]
#     if cur1 == "USD":
#         return rate2
#     else:
#         url = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGE_API_KEY}&base=USD&symbols={cur1}"

#         response = requests.get(url)

#         rate1 = response.json()['rates'][cur1]
#         rate = rate2/rate1
#         return rate

last_time = time.time() - 3600
currency_rates={}
 
def any_walutes_function(cur1, cur2):
    global last_time
    global currency_rates
    global lista_walut
    if time.time() - last_time >= 3600:
        url = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGE_API_KEY}&base=USD&symbols="

        response = requests.get(url)
        currency_rates = response.json()['rates']
        lista_walut = list(dict.keys(currency_rates))

    if cur1 == "USD":
            return currency_rates[cur2]
    else:
        rate = currency_rates[cur2]/currency_rates[cur1]
        return rate

def one_curency(cur1, query):
    results = []
    articles = []
    i = 0
    for cur2 in currencies:
        if cur1 != cur2:
            rate = any_walutes_function(cur1, cur2)
            result = f"1 {cur1} = {round(rate, 4)} {cur2}"
            results.append(result)
            article = telebot.types.InlineQueryResultArticle(
                id=i, title=cur2, description=results[i],
                input_message_content=telebot.types.InputTextMessageContent(message_text=results[i]),
                thumb_url=currensy_pictures[cur2], thumb_width=64, thumb_height=64)
            articles.append(article)
            i += 1
    
    bot.answer_inline_query(query.id, articles)

def two_curencies(scr, tgt, query):
    rate = any_walutes_function(scr, tgt)

    result = f"1 {scr} = {round(rate, 4)} {tgt}"

    article_1 = telebot.types.InlineQueryResultArticle(
        id=1, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=number_pictures[1], thumb_width=64, thumb_height=64)

    result = f"5 {scr} = {round(rate * 5, 2)} {tgt}"

    article_5 = telebot.types.InlineQueryResultArticle(
        id=2, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=number_pictures[5], thumb_width=64, thumb_height=64)
    
    result = f"10 {scr} = {round(rate * 10, 2)} {tgt}"

    article_10 = telebot.types.InlineQueryResultArticle(
        id=3, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=number_pictures[10], thumb_width=64, thumb_height=64)

    result = f"20 {scr} = {round(rate * 20, 2)} {tgt}"

    article_20 = telebot.types.InlineQueryResultArticle(
        id=4, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=number_pictures[20], thumb_width=64, thumb_height=64)

    result = f"50 {scr} = {round(rate * 50,  2)} {tgt}"

    article_50 = telebot.types.InlineQueryResultArticle(
        id=5, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=number_pictures[50], thumb_width=64, thumb_height=64)

    result = f"100 {scr} = {round(rate * 100, 2)} {tgt}"

    article_100 = telebot.types.InlineQueryResultArticle(
        id=6, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=number_pictures[100], thumb_width=64, thumb_height=64)

    bot.answer_inline_query(query.id, [article_1, article_5, article_10, article_20, article_50, article_100])

def two_curencies_with_number(scr, tgt, scr_number, query):
    rate = any_walutes_function(scr, tgt)
    if scr == 1:
        result = f"{scr_number} {scr} = {round(rate * scr_number, 4)} {tgt}"
    else:
        result = f"{scr_number} {scr} = {round(rate * scr_number, 2)} {tgt}"
    article = telebot.types.InlineQueryResultArticle(
    id=1, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
    thumb_url=currensy_pictures[tgt], thumb_width=64, thumb_height=64)

    bot.answer_inline_query(query.id, [article])

def one_curency_with_number(cur1, scr_number, query):
    results = []
    articles = []
    i = 0
    for cur2 in currencies:
        if cur1 != cur2:
            rate = any_walutes_function(cur1, cur2)
            if 0 < scr_number < 2:
                result = f"{scr_number} {cur1} = {round(rate * scr_number, 4)} {cur2}"
            else:
                result = f"{scr_number} {cur1} = {round(rate * scr_number, 2)} {cur2}"
            results.append(result)
            article = telebot.types.InlineQueryResultArticle(
                id=i, title=cur2, description=results[i],
                input_message_content=telebot.types.InputTextMessageContent(message_text=results[i]),
                thumb_url=currensy_pictures[cur2], thumb_width=64, thumb_height=64)
            articles.append(article)
            i += 1
    
    bot.answer_inline_query(query.id, articles)

def komunikat_o_błędzie(query):
    descr = mowa_botu["inline"]["error"]["text"]
    result = mowa_botu["inline"]["error"]["no_tekst_messege"]
    article = telebot.types.InlineQueryResultArticle(
        id=1, title= mowa_botu["inline"]["error"]["title"], description=descr,
        input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url="https://telegra.ph/file/5009881abb1a4f2f8cc82.png", thumb_width=64, thumb_height=64)

    bot.answer_inline_query(query.id, [article])

def isnumeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

bot.polling()