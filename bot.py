import telebot
import os
from poll_test import create_poll, handle_poll_answer
from questions_list import *
from buttons import *

from keep_alive import keep_alive
keep_alive()

from request_to_site import schedule_updater
from threading import Thread
updater_thread = Thread(target=schedule_updater)
updater_thread.daemon = True
updater_thread.start()


BOT_TOKEN = "7033133194:AAGjRf8UglWyUqr3W9Av1mHUnGynF1dPIoA"

#bot = telebot.TeleBot(token=os.environ.get('token'))
bot = telebot.TeleBot(BOT_TOKEN)

users = {}

#---------------registration-------------------
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    users[user_id] = {"score": 0, "current_question": 0}

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
    bot.send_message(user_id, "Выберите тест", reply_markup=menu())
    bot.register_next_step_handler(message, test_type)

#---------------Тип тестов-------------------
@bot.message_handler(func=lambda message: message.text == "📚 Банк тестов")
def test_base1(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Выберите тип теста", reply_markup=menu_test())
    bot.register_next_step_handler(message, test_type)

@bot.message_handler(func=lambda message: message.text in ["🇷🇺 Русский язык", "🏛 История", "⚖️ Законодательство", "⬅️ Назад"])
def test_type(message):
    global user_test
    user_id = message.from_user.id
    if message.text == "🇷🇺 Русский язык":
        bot.send_message(user_id, "Выберите тип теста", reply_markup=menu_ru())
    elif message.text == "🏛 История":
        bot.send_message(user_id, "История")
        user_test = history_quest
        create_poll(bot, user_id, history_quest, users, send_result=True)
    elif message.text == "⚖️ Законодательство":
        bot.send_message(user_id, "Законодательство")
        user_test = law_quest
        create_poll(bot, user_id, law_quest, users, send_result=True)
    elif message.text == "⬅️ Назад":
        bot.send_message(user_id, "Выберите тест", reply_markup=menu())

@bot.message_handler(func=lambda message: message.text in ["🎧 Аудирование", "📖 Чтение", "✍️ Письмо", "📘 Лексика и грамматика", "⬅️ Назад."])
def test_ru(message):
    global user_test
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {"score": 0, "current_question": 0}
    else:
        users[user_id]["score"] = 0
        users[user_id]["current_question"] = 0

    if message.text == "🎧 Аудирование":
        user_test = listening
        create_poll(bot, user_id, listening, users, send_result=True)

    elif message.text == "📖 Чтение":
        user_test = reading
        create_poll(bot, user_id, reading, users, send_result=True)

    elif message.text == "✍️ Письмо":
        user_test = writing
        create_poll(bot, user_id, writing, users, send_result=True)

    elif message.text == "📘 Лексика и грамматика":
        user_test = questions
        create_poll(bot, user_id, questions, users, send_result=True)

    elif message.text == "⬅️ Назад.":
        bot.send_message(user_id, "Выберите тест", reply_markup=menu_test())

@bot.poll_answer_handler(func=lambda answer: True)
def poll_answer_handler(answer):
    user_id = answer.user.id
    if user_id in users:
        if users[user_id]["current_question"] < len(user_test):  # Если ещё есть вопросы
            handle_poll_answer(bot, answer, users, user_test, send_result=True)

        else:
            bot.send_message(user_id, "Тест завершён. Возвращаем вас в меню.", reply_markup=menu())

#---------------Mock test-------------------
@bot.message_handler(func=lambda message: message.text == "✅ Пробный экзамен")
def mock_test(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Выберите вариант экзамена", reply_markup=exam_btns())
    bot.register_next_step_handler(message, test_optons)


@bot.message_handler(func=lambda message: message.text in ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4", "Вариант 5" "⬅️ Назад"])
def test_optons(message):
    global user_test
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {"score": 0, "current_question": 0}
    else:
        users[user_id]["score"] = 0
        users[user_id]["current_question"] = 0

    if message.text == "Вариант 1":
        user_test = option1
        create_poll(bot, user_id, option1, users, send_result=True)

    elif message.text == "Вариант 2":
        user_test = option2
        create_poll(bot, user_id, option2, users, send_result=True)

    elif message.text == "Вариант 3":
        user_test = option3
        create_poll(bot, user_id, option3, users, send_result=True)

    elif message.text == "Вариант 4":
        user_test = option4
        create_poll(bot, user_id, option4, users, send_result=True)

    elif message.text == "Вариант 5":
        user_test = option5
        create_poll(bot, user_id, option5, users, send_result=True)

    elif message.text == "⬅️ Назад":
        bot.send_message(user_id, "Выберите тест", reply_markup=menu())

@bot.poll_answer_handler(func=lambda answer: True)
def poll_test_answer_handler(answer):
    user_id = answer.user.id
    if user_id in users:
        if users[user_id]["current_question"] < len(user_test):  # Если ещё есть вопросы
            handle_poll_answer(bot, answer, users, user_test, send_result=True)
        else:
            bot.send_message(user_id, "Тест завершён. Возвращаем вас в меню.", reply_markup=menu())

@bot.message_handler(func=lambda message: message.text == "Главное меню")
def main_menu(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Главное меню", reply_markup=menu())


bot.polling(non_stop=True)