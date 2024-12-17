import telebot
import os
from poll_test import create_poll
from questions_list import questions
from buttons import *

bot = telebot.TeleBot(token=os.environ.get('token'))

users = {}

#---------------registration-------------------
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    bot.send_message(user_id, "🇺🇿Salom. Iltimos, ismingizni yuboring.\n"
                              "------------\n"
                              "🇷🇺Здравствуйте. Пожалуйста, отправьте свое имя.")

    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, f"🇺🇿 {name} tanishganimdan xursandman. Raqamingizni yuboring\n"
                              f"🇷🇺 {name} рад знакомству. Отправьте номер телефона.",reply_markup=phone_button_uz())
    bot.register_next_step_handler(message, contact_handler, name)

def contact_handler(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, "🇺🇿 Tizimda muvaffaqiyatli ro‘yxatdan o‘tdingiz! Pastdagi tugmalar orqali harakatni tanlang."
                                  "\n------------\n"
                                  "🇷🇺 Вы успешно зарегистрировались в системе! Выберите операцию ниже.", reply_markup=menu())
        #db.add_user(name, phone_number, user_id)

    else:
        bot.send_message(user_id, "Raqamingizni pastdagi tugma orqali yuboring",
                         reply_markup=phone_button_uz())

        bot.register_next_step_handler(message, test_base, name)




#---------------Банк тестов-------------------
def test_base(message):
    user_id = message.from_user.id
    users[user_id] = {"score": 0, "current_question": 0}
    bot.send_message(user_id, "Выберите тест", reply_markup=menu())
    bot.register_next_step_handler(message, test_type)

#---------------тесты-------------------
@bot.message_handler(func=lambda message: message.text == "📚 Банк тестов")
def test_base1(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Выберите тип теста", reply_markup=menu_test())
    bot.register_next_step_handler(message, test_type)

#---------------Тип тестов-------------------
@bot.message_handler(func=lambda message: message.text == "🇷🇺 Русский язык")
def test_type(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Выберите тип теста", reply_markup=menu_ru())

@bot.message_handler(func=lambda message: message.text in ["🎧 Аудирование", "📖 Чтение", "✍️ Письмо", "📘 Лексика и грамматика", "⬅️ Назад."])
def test_ru(message):
    user_id = message.from_user.id
    users[user_id]["score"] = 0
    users[user_id]["current_question"] = 0

    if message.text == "🎧 Аудирование":
        create_poll(bot, user_id, questions, users, send_result=False)
    elif message.text == "📖 Чтение":
        create_poll(bot, user_id, questions, users, send_result=False)
    elif message.text == "✍️ Письмо":
        create_poll(bot, user_id, questions, users, send_result=False)
    elif message.text == "📘 Лексика и грамматика":
        create_poll(bot, user_id, questions, users, send_result=False)
    elif message.text == "⬅️ Назад":
        bot.send_message(user_id, "Выберите тест", reply_markup=menu_ru())


@bot.message_handler(func=lambda message: message.text == "🏛 История")
def test_history(message):
    ...
#---------------Mock exam -------------------

bot.polling(non_stop=True)