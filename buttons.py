from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton("📚 Банк тестов")
    button2 = KeyboardButton("✅ Пробный экзамен")
    button4 = KeyboardButton("📖 Учебные материалы")
    button3 = KeyboardButton("📝 Rus tili kursiga yozilish")
    markup.add(button1, button2)
    markup.add(button4)
    markup.add(button3)
    return markup

def menu_test():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton("🇷🇺 Русский язык")
    button2 = KeyboardButton("🏛 История")
    button3 = KeyboardButton("⚖️ Законодательство")
    button4 = KeyboardButton("⬅️ Назад")
    markup.add(button1, button2)
    markup.add(button3, button4)
    return markup

def menu_ru():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton("🎧 Аудирование")
    button2 = KeyboardButton("📖 Чтение")
    button3 = KeyboardButton("✍️ Письмо")
    button4 = KeyboardButton("📘 Лексика и грамматика")
    button5 = KeyboardButton("⬅️ Назад.")
    markup.add(button1, button2)
    markup.add(button3, button4)
    markup.add(button5)
    return markup

def phone_button_uz():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phone = KeyboardButton("Telefon raqamini yuboring", request_contact=True)
    markup.add(button_phone)
    return markup

def exam_btns():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Вариант 1")
    button2 = KeyboardButton("Вариант 2")
    button3 = KeyboardButton("Вариант 3")
    button4 = KeyboardButton("Вариант 4")
    button5 = KeyboardButton("Вариант 5")
    button6 = KeyboardButton("⬅️ Назад")
    markup.add(button1, button2)
    markup.add(button3, button4)
    markup.add(button5)
    markup.add(button6)
    return markup

def exit_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 =KeyboardButton("Главное меню")
    markup.add(button1)
    return markup


def create_inline_keyboard_with_feedback(options, correct_answer=None, selected_option=None):
    """
    Создаёт инлайн-клавиатуру с обратной связью.
    Если передан correct_answer и selected_option, добавляет галочки/крестики.
    """
    keyboard = InlineKeyboardMarkup()
    for option in options:
        # Определяем текст кнопки
        if correct_answer and selected_option:
            if option == correct_answer:
                text = f"{option} ✅"  # Правильный ответ
            elif option == selected_option:
                text = f"{option} ❌"  # Неправильный выбранный ответ
            else:
                text = option  # Оставшиеся варианты
        else:
            text = option

        # Создаём кнопку
        button = InlineKeyboardButton(text=text, callback_data=option)
        keyboard.add(button)

    return keyboard