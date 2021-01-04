from config import keys, TOKEN
from extensions import ConvertionExeption, Cryptoconverter
import telebot

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help']) #инструкция
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты цену которой он хочет узнать> \
<имя валюты в которой надо узнать цену первой валюты> <количество первой валюты> \n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])  #обработчик выводит доступные валюты
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        values = list(map(str.lower, values))
        if len(values) != 3:
            raise ConvertionExeption('Неверное количество параметров')
        quote, base, amount = values
        total_base = Cryptoconverter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} -  {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
