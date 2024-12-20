from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

def menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton("📚 Банк тестов")
    button2 = KeyboardButton("✅ Пробный экзамен")
    button4 = KeyboardButton("📖 O‘quv materiallari")
    button3 = KeyboardButton("📝 Rus tili kursiga yozilish")
    markup.add(button1, button2)
    markup.add(button4)
    markup.add(button3)
    return markup

def lessons_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("▶️ Video materiallar")
    button2 = KeyboardButton("📖 Darsliklar")
    button4 = KeyboardButton("⬅️ Назад")
    markup.add(button1, button2)
    markup.add(button4)
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


from telebot.types import ReplyKeyboardMarkup, KeyboardButton

regions = [
    "Andijon viloyati", "Buxoro viloyati", "Jizzax viloyati", "Qoraqalpog‘iston Respublikasi", "Qashqadaryo viloyati",
    "Navoiy viloyati", "Namangan viloyati", "Samarqand viloyati", "Sirdaryo viloyati", "Surxondaryo viloyati",
    "Toshkent viloyati", "Farg‘ona viloyati", "Xorazm viloyati", "Toshkent shahri"
]

learning_centers = {
    "Andijon viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Andijon shahri kasbiy ko‘nikmalar markazi"],
    "Buxoro viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Buxoro shahri kasbiy ko‘nikmalar markazi"],
    "Jizzax viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Jizzax shahri kasbiy ko‘nikmalar markazi"],
    "Qoraqalpog‘iston Respublikasi": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Nukus shahri kasbiy ko‘nikmalar markazi"],
    "Qashqadaryo viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Qarshi shahri kasbiy ko‘nikmalar markazi", "Ko‘kdala tumani kasbiy ko‘nikmalar markazi"],
    "Navoiy viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Navoiy shahri kasbiy ko‘nikmalar markazi", "Nurota tumani kasbiy ko‘nikmalar markazi"],
    "Namangan viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Namangan shahri kasbiy ko‘nikmalar markazi"],
    "Samarqand viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Samarqand shahri kasbiy ko‘nikmalar markazi", "Kattaqo‘rg‘on shahri kasbiy ko‘nikmalar markazi"],
    "Sirdaryo viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Guliston shahri kasbiy ko‘nikmalar markazi", "Sardoba tumani kasbiy ko‘nikmalar markazi"],
    "Surxondaryo viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Angor tumani kasbiy ko‘nikmalar markazi", "Denov tumani kasbiy ko‘nikmalar markazi"],
    "Toshkent viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Oqqo‘rg‘on tumani kasbiy ko‘nikmalar markazi", "Piskent tumani kasbiy ko‘nikmalar markazi"],
    "Farg‘ona viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Farg‘ona shahri kasbiy ko‘nikmalar markazi", "Buvayda tumani kasbiy ko‘nikmalar markazi"],
    "Xorazm viloyati": ["Qurilish soxasida malakali mutaxassislarni tayyorlash markazi", "Urganch shahri kasbiy ko‘nikmalar markazi"],
    "Toshkent shahri": ["Respublika kasbiy ko‘nikmalar markazi"]
}


def create_keyboard(options, request_contact=False):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        if isinstance(option, list):
            buttons = [KeyboardButton(text, request_contact=request_contact) for text in option]
            keyboard.add(*buttons)
        else:
            keyboard.add(KeyboardButton(option))
    return keyboard


def create_main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton("📝 Rus tili kursiga yozilish")
    markup.add(item1)
    return markup

# Кнопки для выбора региона
def create_keyboard(options):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for option in options:
        button = types.KeyboardButton(option)
        markup.add(button)
    return markup

# Кнопки для возвращения на шаг назад
def create_back_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton("⬅️ Orqaga")
    markup.add(back_button)
    return markup

# Кнопка подтверждения или завершения
def create_finish_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    finish_button = types.KeyboardButton("✅ Yakunlash")
    markup.add(finish_button)
    return markup