from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from backend import Shedule


bot = TeleBot("7865483487:AAFX5_VNkQF6ncEdV9CHBGeebLkT3zoCcmA")


schedule = Shedule()


def create_main_buttons():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Ближайшее занятие", callback_data="near_lesson"))
    keyboard.add(InlineKeyboardButton("Расписание дня недели", callback_data="day_week_number"))
    keyboard.add(InlineKeyboardButton("Расписание следующего дня", callback_data="tommorrow"))
    keyboard.add(InlineKeyboardButton("Расписание всей недели", callback_data="all_week"))
    return keyboard


def create_day_buttons():
    keyboard = InlineKeyboardMarkup()
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    for i, day in enumerate(days):
        keyboard.add(InlineKeyboardButton(day, callback_data=f"day_{i}"))
    keyboard.add(InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я помогу тебе получить расписание. Введите номер группы.",
    )


@bot.message_handler(content_types=['text'])
def handle_group_input(message):
    group_number = message.text.strip()
    result = schedule.add_group(group_number)

    if result == 0:
        bot.send_message(
            message.chat.id,
            "Группа добавлена успешно! Выберите действие:",
            reply_markup=create_main_buttons()
        )
    else:
        bot.send_message(message.chat.id, "Такой группы не существует! Попробуйте снова.")


@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    try:
        if call.data == "near_lesson":
            result = schedule.get_schedule("near_lesson")
            bot.edit_message_text(
                result,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=create_main_buttons(),
                parse_mode="Markdown"
            )

        elif call.data == "day_week_number":
            bot.edit_message_text(
                "Выберите день недели:",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=create_day_buttons(),
                parse_mode="HTML"
            )

        elif call.data.startswith("day_"):
            day_index = int(call.data.split("_")[1])
            result = schedule.get_schedule("day_week_number", week_day=day_index)
            bot.edit_message_text(
                result,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=create_day_buttons(),
                parse_mode="Markdown"
            )

        elif call.data == "tommorrow":
            result = schedule.get_schedule("tommorrow")
            bot.edit_message_text(
                result,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=create_main_buttons(),
                parse_mode="Markdown"
            )

        elif call.data == "all_week":
            result = schedule.get_schedule("all_week")
            bot.edit_message_text(
                result,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=create_main_buttons(),
                parse_mode="Markdown"
            )

        elif call.data == "main_menu":
            bot.edit_message_text(
                "Выберите действие:",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=create_main_buttons(),
                parse_mode="HTML"
            )

    except Exception as e:
        bot.edit_message_text(
            f"Ошибка: {e}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_main_buttons(),
            parse_mode="HTML"
        )


bot.polling(none_stop=True)
