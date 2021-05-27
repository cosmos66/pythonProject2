import telebot
bot=telebot.TeleBot('1892786440:AAExhtjU-Vt49UQsURUPklsLiVsuKkOXi90')

@bot.message_handler(content_types=['text'])
def send_welcome(message):
    bot.send_message(message.chat.id,message.text)


bot.polling(none_stop=True)

