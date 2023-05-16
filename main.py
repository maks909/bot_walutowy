import telebot
import requests
from telebot import types

#Spetial thank's for flaticon.com for it's icons

plik = open("TOKEN.ini")
TOKEN = plik.read()
plik.close()

bot = telebot.TeleBot(TOKEN)
OPENEXCHANGE_API_KEY = "9c157b50feae410d85148894079c06ca"

currencies = ("USD", "EUR", "PLN", "RUB", "BYN", "GBP", "CNY", "CHF", "UAH", "JPY")

currensy_pictures = {"USD":"https://telegra.ph/file/229e7bc4ef6f23d127cc3.png", "EUR":"https://telegra.ph/file/abd077de4d9ab557c77b8.png", "PLN":"https://telegra.ph/file/45d7c30e714afa69f8e36.png", "RUB":"https://telegra.ph/file/564592554d733e6e29724.png", "BYN":"https://telegra.ph/file/93a67e8a5a62a18354b3e.png", "GBP":"https://telegra.ph/file/6e99f7dcf172b7b802ffb.png", "CNY":"https://telegra.ph/file/ed8cec61f2943bcfb9f5a.png", "CHF":"https://telegra.ph/file/e672f46428eb3612c8311.png", "UAH":"https://telegra.ph/file/20d4d140fa6cc5b7deb1f.png", "JPY":"https://telegra.ph/file/0ed34d05c60533bc85eb2.png"}

number_pictures = {1:"https://telegra.ph/file/31f2b3d588e89638e5c20.png", 5:"https://telegra.ph/file/8e5155ea17c4eef7c0f11.png", 10:"https://telegra.ph/file/3f3b2e0d83d82dd1b69a2.png", 20:"https://telegra.ph/file/2f43f402eb5054de068b9.png", 50:"https://telegra.ph/file/864c79280630d1e6837ae.png", 100:"https://telegra.ph/file/7b284263ea92b9ca95cef.png"}

@bot.message_handler(commands=["start"])
def początek(m):
    bot.send_message(m.chat.id, " Jestem botem do pomocy w napisaniu walut. \n Możesz mnie zawołać w każdym czacie z pomocą @currency_rate_help_bot I nazw walut. \n Dowiesz się więcej jeżeli napiszesz /help.")

@bot.message_handler(commands=["help"])
def pomoc(m):
    bot.send_message(chat_id=m.chat.id, text="Teraz opowiem panu/pani jak mnie używać. :)")
    bot.send_message(chat_id=m.chat.id, text="Możesz mnie używać w jakim kolwiek czacie. \nPoprostu napisz moje imię (@currency_rate_help_bot) i kilka innych rzeczy, póżniej wybierz coś w liście sugestii i kiedy wyślisz wiadomość będzie widać tylko coś podobnego do x USD = y EUR.")
    bot.send_message(chat_id=m.chat.id, text='''Przykłady:
    1) Napisz @currency_rate_help_bot i dwie waluty. Np. @currency_rate_help_bot PLN EUR.
    
    2) Napisz @currency_rate_help_bot i jedną walutę. Np. @currency_rate_help_bot PLN.
    
    3) Napisz @currency_rate_help_bot, dwie waluty i liczbę pieniędzy do wymiany. Np. @currency_rate_help_bot PLN USD 23 albo @currency_rate_help_bot PLN USD 23.50.
    
    4) Napisz @currency_rate_help_bot, jedną walutę i liczbę pieniędzy. Np. @currency_rate_help_bot PLN 105 albo @currency_rate_help_bot PLN 105.67.''')


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
    hint = "Wpisz intyfikatory walut: USD EUR PLN RUB BYN GBP CNY CHF UAH JPY, żeby zobaczyć kursy walut"
    try:
        r = types.InlineQueryResultArticle(
                id="12",
                title="Bot \"walutowy\"",
                description=hint,
                input_message_content=types.InputTextMessageContent(
                message_text="Mógłbym dowiedzieć się o kursie walut...",
                parse_mode="Markdown")
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)

def any_walutes_function(cur1, cur2):
    url2 = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGE_API_KEY}&base=USD&symbols={cur2}"

    response = requests.get(url2)

    rate2 = response.json()['rates'][cur2]
    if cur1 == "USD":
        return rate2
    else:
        url = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGE_API_KEY}&base=USD&symbols={cur1}"

        response = requests.get(url)

        rate1 = response.json()['rates'][cur1]
        rate = rate2/rate1
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
    descr = "Coś żle wpisałeś. Wpisz intyfikatory walut: USD EUR PLN RUB BYN, żeby zobaczyć kursy walut. Możesz też dodać liczbę pieniędzy na końcu."
    result = "Nic dobrego nie wpisałem... A mogłem :("
    article = telebot.types.InlineQueryResultArticle(
        id=1, title="Coś jest żle :(", description=descr,
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