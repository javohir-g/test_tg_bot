import telebot
import os
from poll_test import create_poll, handle_poll_answer
from questions_list import *
from buttons import *
from telebot.types import Message
from database import add_user, get_user

ADMIN_CHAT_ID = -4705809842
from keep_alive import keep_alive
keep_alive()

from request_to_site import schedule_updater
from threading import Thread
updater_thread = Thread(target=schedule_updater)
updater_thread.daemon = True
updater_thread.start()

bot = telebot.TeleBot(token=os.environ.get('token'))

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
    users[user_id] = {"name": name}  # Сохраняем имя
    bot.send_message(user_id, f"🇺🇿 {name} tanishganimdan xursandman. Raqamingizni yuboring\n"
                              f"🇷🇺 {name} рад знакомству. Отправьте номер телефона.", reply_markup=phone_button_uz())
    bot.register_next_step_handler(message, contact_handler, name)

def contact_handler(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        users[user_id]["phone_number"] = phone_number  # Сохраняем номер телефона
        add_user(user_id, name, phone_number)  # Добавляем пользователя в базу данных
        bot.send_message(user_id, "🇺🇿 Tizimda muvaffaqiyatli ro‘yxatdan o‘tdingiz! Pastdagi tugmalar orqali harakatni tanlang."
                                  "\n------------\n"
                                  "🇷🇺 Вы успешно зарегистрировались в системе! Выберите операцию ниже.", reply_markup=menu())
    else:
        bot.send_message(user_id, "Raqamingizni pastdagi tugma orqali yuboring",
                         reply_markup=phone_button_uz())
        bot.register_next_step_handler(message, contact_handler, name)

@bot.message_handler(func=lambda message: message.text == "📖 Учебные материалы")
def test_base1(message):
    folder_path = "books"
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)

    bot.send_message(message, "Все доступные учебные материалы отправлены.", reply_markup=exit_button())

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


#-----------"📝 Rus tili kursiga yozilish"-----------
@bot.message_handler(func=lambda message: message.text == "📝 Rus tili kursiga yozilish")
def start_registration(message: Message):
    users[message.chat.id] = {}
    bot.send_message(message.chat.id, "Выберите ваш регион:", reply_markup=create_keyboard(regions + ["⬅️ Orqaga"]))
    bot.register_next_step_handler(message, get_region)

# Обработка выбора региона
def get_region(message: Message):
    if message.text == "⬅️ Orqaga":
        bot.send_message(message.chat.id, "Выберите ваш регион:", reply_markup=create_keyboard(regions + ["⬅️ Orqaga"]))
        bot.register_next_step_handler(message, get_region)
        return

    if message.text not in regions:
        bot.send_message(message.chat.id, "Пожалуйста, выберите регион из списка.")
        bot.register_next_step_handler(message, get_region)
        return

    users[message.chat.id]['region'] = message.text
    bot.send_message(message.chat.id, "O‘quv markazini tanlang:", reply_markup=create_keyboard(learning_centers[message.text] + ["⬅️ Orqaga"]))
    bot.register_next_step_handler(message, get_learning_center)

# Обработка выбора учебного центра
def get_learning_center(message: Message):
    if message.text == "Orqaga":
        bot.send_message(message.chat.id, "Hududingizni tanlang:", reply_markup=create_keyboard(regions + ["Назад"]))
        bot.register_next_step_handler(message, get_region)
        return

    region = users[message.chat.id]['region']
    if message.text not in learning_centers[region]:
        bot.send_message(message.chat.id, "Iltimos, ro‘yxatdan markazini tanlang.")
        bot.register_next_step_handler(message, get_learning_center)
        return

    users[message.chat.id]['learning_center'] = message.text

    # Получаем данные пользователя из базы данных
    user_data = get_user(message.chat.id)
    if user_data:
        name, phone_number = user_data
    else:
        name = "Не указано"
        phone_number = "Не указан"

    # Формируем текст заявки с данными из базы
    application_text = (
        f"Новая заявка на курс Русского языка:\n\n"
        f"Имя: {name}\n"
        f"Номер телефона: {phone_number}\n"
        f"Регион: {users[message.chat.id]['region']}\n"
        f"Центр: {users[message.chat.id]['learning_center']}"
    )

    # Отправляем заявку администратору
    bot.send_message(ADMIN_CHAT_ID, application_text)

    # Завершаем регистрацию
    bot.send_message(message.chat.id, "Arizangiz administratorga yuborildi.\nTez orada siz bilan bog‘lanadii")
    users.pop(message.chat.id)



bot.polling(non_stop=True)