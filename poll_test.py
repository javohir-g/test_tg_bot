import telebot
from pyexpat.errors import messages
from buttons import menu, exit_button


# Функция для создания и отправки опросов
def create_poll(bot, user_id, questions, users, send_result=True):
    question_index = users[user_id]["current_question"]
    if question_index >= len(questions):
        finish_test(bot, user_id, users, len(questions), send_result)
        return

    question_data = questions[question_index]
    question_text = question_data["question"]
    options = question_data["options"]
    correct_option_index = options.index(question_data["correct"])

    # Отправляем аудио, если оно есть
    if "audio" in question_data and question_data["audio"]:
        audio_path = question_data["audio"]
        try:
            with open(audio_path, 'rb') as audio:
                bot.send_audio(user_id, audio, caption="Прослушайте и ответьте на вопрос:")
        except FileNotFoundError:
            bot.send_message(user_id, "Не удалось найти аудиофайл.")

    # Отправляем опрос
    bot.send_poll(
        chat_id=user_id,
        question=question_text,
        options=options,
        correct_option_id=correct_option_index,
        is_anonymous=False,
        allows_multiple_answers=False,
        type='quiz', reply_markup=exit_button()
    )

# Обработка ответов на викторину
def handle_poll_answer(bot, answer, users, questions, send_result=True):
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

    # Переход к следующему вопросу
    users[user_id]["current_question"] += 1
    create_poll(bot, user_id, questions, users, send_result)

# Завершение теста и возврат в меню
def finish_test(bot, user_id, users, total_questions, send_result):
    score = users[user_id]["score"]
    bot.send_message(user_id, f"Тест завершён! Ваш результат: {score}/{total_questions}.")
    users[user_id] = {"score": 0, "current_question": 0}

    # Возвращаемся к выбору теста
    bot.send_message(user_id, "Выберите тест", reply_markup=menu())
