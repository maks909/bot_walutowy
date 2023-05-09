import telebot
import requests
from telebot import types

plik = open("TOKEN.ini")
TOKEN = plik.read()
plik.close()

bot = telebot.TeleBot(TOKEN)
OPENEXCHANGE_API_KEY = "9c157b50feae410d85148894079c06ca"

currencies = ("USD", "EUR", "PLN", "RUB", "BYN")
currensy_pictures = {"USD":"https://telegra.ph/file/229e7bc4ef6f23d127cc3.png", "EUR":"https://telegra.ph/file/abd077de4d9ab557c77b8.png", "PLN":"https://telegra.ph/file/45d7c30e714afa69f8e36.png", "RUB":"https://telegra.ph/file/564592554d733e6e29724.png", "BYN":"https://telegra.ph/file/93a67e8a5a62a18354b3e.png"}

@bot.inline_handler(lambda query: query.query)
def query_text(query):
    # Dzielimy otrzymane w żądaniu informacje
    req = query.query.upper().split()
    if len(req) != 2:
        return
    scr, tgt = req
    if not scr in currencies or not tgt in currencies:
        return 
    # Zapisujemy adres żądania do API
    url = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGE_API_KEY}&base={scr}&symbols={tgt}"
    # Wysłanie żądania GET do API
    response = requests.get(url)
    # Parsing (rozszyfrowanie) otrzymanej odpowiedzi
    rate = response.json()['rates'][tgt]
    
    result = f"1 {scr} = {rate} {tgt}"

    article_1 = telebot.types.InlineQueryResultArticle(
        id=1, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=currensy_pictures[tgt], thumb_width=64, thumb_height=64)

    result = f"5 {scr} = {rate * 5} {tgt}"

    article_5 = telebot.types.InlineQueryResultArticle(
        id=2, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=currensy_pictures[tgt], thumb_width=64, thumb_height=64)
    
    result = f"10 {scr} = {rate * 10} {tgt}"

    article_10 = telebot.types.InlineQueryResultArticle(
        id=3, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=currensy_pictures[tgt], thumb_width=64, thumb_height=64)

    result = f"20 {scr} = {rate * 20} {tgt}"

    article_20 = telebot.types.InlineQueryResultArticle(
        id=4, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=currensy_pictures[tgt], thumb_width=64, thumb_height=64)

    result = f"50 {scr} = {rate * 50} {tgt}"

    article_50 = telebot.types.InlineQueryResultArticle(
        id=5, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=currensy_pictures[tgt], thumb_width=64, thumb_height=64)

    result = f"100 {scr} = {rate * 100} {tgt}"

    article_100 = telebot.types.InlineQueryResultArticle(
        id=6, title=result, input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumb_url=currensy_pictures[tgt], thumb_width=64, thumb_height=64)

    bot.answer_inline_query(query.id, [article_1, article_5, article_10, article_20, article_50, article_100])

@bot.inline_handler(lambda query: query == 0)
def empty_query(query):
    hint = "Wpisz intyfikatory walut: USD EUR PLN RUB BYN, żeby zobaczyć kursy walut"
    try:
        r = types.InlineQueryResultArticle(
                id="12",title="Bot \"walutowy\"",
                input_message_content=types.InputTextMessageContent(
                    message_text="Mógłbym dowiedzieć się o kursie walut...",
                    parse_mode="Markdown")
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)


bot.polling()