import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from questions_list import questions
# Ваш токен Telegram-бота
TOKEN = '7927478236:AAEaWaz1v2rNK9W5Oc2cZ7PPRjDhaZZMUHk'
bot = telebot.TeleBot(TOKEN)
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Хранилище данных пользователей
users = {}

@bot.message_handler(commands=['start', 'menu'])
def menu(message):
    user_id = message.chat.id
    users[user_id] = {"score": 0, "current_question": 0}

    # Создаём обычную кнопку "Начать тест"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    start_test_button = KeyboardButton("Начать тест")
    markup.add(start_test_button)
    bot.send_message(user_id, "Добро пожаловать в главное меню!", reply_markup=markup)


# Обработка нажатия кнопки "Начать тест"
@bot.message_handler(func=lambda message: message.text == "Начать тест")
def handle_start_test_button(message):
    user_id = message.chat.id
    users[user_id]["score"] = 0
    users[user_id]["current_question"] = 0
    send_question(user_id)


# Отправка вопроса в режиме викторины
def send_question(user_id):
    question_index = users[user_id]["current_question"]
    if question_index >= len(questions):
        finish_test(user_id)
        return

    question_data = questions[question_index]
    question_text = question_data["question"]
    options = question_data["options"]

    # Индекс правильного ответа
    correct_option_index = options.index(question_data["correct"])

    # Отправляем аудио, если оно есть
    if "audio" in question_data and question_data["audio"]:
        audio_path = question_data["audio"]
        try:
            with open(audio_path, 'rb') as audio:
                bot.send_audio(user_id, audio)
        except FileNotFoundError:
            bot.send_message(user_id, "Не удалось найти аудиофайл.")

    # Отправляем опрос в режиме викторины
    bot.send_poll(
        chat_id=user_id,
        question=question_text,
        options=options,
        correct_option_id=correct_option_index,
        is_anonymous=False,
        allows_multiple_answers=False,
        type='quiz'
    )


# Обработка ответа на викторину
@bot.poll_answer_handler(func=lambda answer: True)
def handle_poll_answer(answer):
    user_id = answer.user.id
    if user_id not in users or "current_question" not in users[user_id]:
        return

    question_index = users[user_id]["current_question"]
    question_data = questions[question_index]
    correct_answer = question_data["correct"]

    # Получаем выбранный вариант
    selected_option_index = answer.option_ids[0]
    selected_option = question_data["options"][selected_option_index]

    # Проверяем, правильный ли ответ
    if selected_option == correct_answer:
        users[user_id]["score"] += 1

    # Переходим к следующему вопросу
    users[user_id]["current_question"] += 1
    send_question(user_id)


# Завершение теста
def finish_test(user_id):
    score = users[user_id]["score"]
    total_questions = len(questions)
    bot.send_message(user_id, f"Тест завершён! Ваш результат: {score}/{total_questions}.")
    del users[user_id]["current_question"]


# Запуск бота
bot.polling(non_stop=True)
