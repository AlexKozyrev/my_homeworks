import telebot
from extensions import APIException, CurrencyConverter
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
telegram_token = config['telegram']['token']
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    help_text = 'Чтобы узнать цену валюты, напишите в формате:\n' \
                '<имя валюты, которую вы переводите> ' \
                '<имя валюты, в которую вы переводите> ' \
                '<количество переводимой валюты>\n\n' \
                'Например: рубль евро 100\n\n' \
                'Для получения списка доступных валют введите команду /values'
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    values_text = 'Доступные валюты:\n' \
                  'USD - доллар США\n' \
                  'EUR - евро\n' \
                  'RUB - российский рубль'
    bot.reply_to(message, values_text)


@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Некорректный ввод, наберите /help для справки')
        base, quote, amount = values
        result = CurrencyConverter.get_price(base.lower(), quote.lower(), float(
            amount))  # понижаем регистр в названиях валют, чтобы понимать ввод разных регистров
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')
    except ValueError:
        bot.send_message(message.chat.id, f'Ошибка: Количество переводимой валюты введено не верно, наберите /help '
                                          f'для справки')
    else:
        text = f'{amount} {base.lower()} = {result} {quote.lower()}'
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling()
