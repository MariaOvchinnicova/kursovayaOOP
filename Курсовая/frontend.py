from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from backend import Shedule

class ScheduleBot:
    def __init__(self, token):
        self.bot = TeleBot(token)
        self.schedule = Shedule()
        self.register_handlers()

    def create_main_buttons(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Ближайшее занятие", callback_data="near_lesson"))
        keyboard.add(InlineKeyboardButton("Расписание дня недели", callback_data="day_week_number"))
        keyboard.add(InlineKeyboardButton("Расписание следующего дня", callback_data="tommorrow"))
        keyboard.add(InlineKeyboardButton("Расписание всей недели", callback_data="all_week"))
        return keyboard

    def create_day_buttons(self):
        keyboard = InlineKeyboardMarkup()
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        for i, day in enumerate(days):
            keyboard.add(InlineKeyboardButton(day, callback_data=f"day_{i}"))
        keyboard.add(InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
        return keyboard

    def handle_start(self, message):
        self.bot.send_message(
            message.chat.id,
            "Привет! Я помогу тебе получить расписание. Введите номер группы.",
        )

    def handle_group_input(self, message):
        group_number = message.text.strip()
        result = self.schedule.add_group(group_number)

        if result == 0:
            self.bot.send_message(
                message.chat.id,
                "Группа добавлена успешно! Выберите действие:",
                reply_markup=self.create_main_buttons()
            )
        else:
            self.bot.send_message(message.chat.id, "Такой группы не существует! Попробуйте снова.")

    def handle_buttons(self, call):
        try:
            if call.data == "near_lesson":
                result = self.schedule.get_schedule("near_lesson")
                self.bot.edit_message_text(
                    result,
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=self.create_main_buttons(),
                    parse_mode="Markdown"
                )

            elif call.data == "day_week_number":
                self.bot.edit_message_text(
                    "Выберите день недели:",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=self.create_day_buttons(),
                    parse_mode="HTML"
                )

            elif call.data.startswith("day_"):
                day_index = int(call.data.split("_")[1])
                result = self.schedule.get_schedule("day_week_number", week_day=day_index)
                self.bot.edit_message_text(
                    result,
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=self.create_day_buttons(),
                    parse_mode="Markdown"
                )

            elif call.data == "tommorrow":
                result = self.schedule.get_schedule("tommorrow")
                self.bot.edit_message_text(
                    result,
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=self.create_main_buttons(),
                    parse_mode="Markdown"
                )

            elif call.data == "all_week":
                result = self.schedule.get_schedule("all_week")
                self.bot.edit_message_text(
                    result,
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=self.create_main_buttons(),
                    parse_mode="Markdown"
                )

            elif call.data == "main_menu":
                self.bot.edit_message_text(
                    "Выберите действие:",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=self.create_main_buttons(),
                    parse_mode="HTML"
                )

        except Exception as e:
            self.bot.edit_message_text(
                f"Ошибка: {e}",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=self.create_main_buttons(),
                parse_mode="HTML"
            )

    def register_handlers(self):
        self.bot.message_handler(commands=['start', 'help'])(self.handle_start)
        self.bot.message_handler(content_types=['text'])(self.handle_group_input)
        self.bot.callback_query_handler(func=lambda call: True)(self.handle_buttons)

    def start_polling(self):
        self.bot.polling(none_stop=True)

if __name__ == "__main__":
    token = "7865483487:AAFX5_VNkQF6ncEdV9CHBGeebLkT3zoCcmA"
    bot = ScheduleBot(token)
    bot.start_polling()
