import telebot
from telebot import types
bot = telebot.TeleBot('1892786440:AAExhtjU-Vt49UQsURUPklsLiVsuKkOXi90')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message)
    if message.from_user.id !=1011385498:
        bot.send_message(message.from_user.id,"Ты кто такой?")
        exit()


    if message.text == "Тест":
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Ты прошел мое проверку, тебе помочь?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_photo(call.message.chat.id, open('F:\Mega\Документы\_DSC0009.jpg', 'rb'))
    elif call.data == "no":
        bot.send_message(call.message.chat.id,"Ну и хрен с тобой")
bot.polling(none_stop=True, interval=0)