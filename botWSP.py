import telebot
from telebot import types

TOKEN = "---"
ADMIN_ID = "---"
CHAT_LINK = "---"  #

bot = telebot.TeleBot(TOKEN)

user_states = {}


def create_main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    btn_manual = types.InlineKeyboardButton("📖 Мануал", callback_data="manual")
    btn_question = types.InlineKeyboardButton(
        "❓ Задать вопрос", callback_data="ask_question"
    )
    keyboard.add(btn_manual, btn_question)
    return keyboard


# Приветственное сообщение
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите действие:",
        reply_markup=create_main_keyboard(),
    )


# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "manual":
        send_manual(call.message)

    elif call.data == "ask_question":
        user_states[call.from_user.id] = "waiting_question"
        bot.send_message(
            call.message.chat.id,
            "Напишите ваш вопрос и я перешлю его админу! Он ответит вам в личные сообщения.",
        )

    elif call.data == "confirm_read":
        # ссылку на чат и возвращаем основное меню
        bot.send_message(
            call.message.chat.id,
            f"🎉 Поздравляем! Теперь вы можете присоединиться к нашему чату:\n{CHAT_LINK}",
            reply_markup=create_main_keyboard(),
        )


def send_manual(message):
    manual_text = """📚 Полный мануал:
    
1.  Для чего нужен акк в ватсап:
Только для рекламы магазинов (WB, OZON, MAAG и другие).
— Важно: Твои личные контакты не используются для рассылки! У магазинов своя база номеров.
— Никаких незаконных действий! Только легальная реклама.

 Ты даешь мне номер своего WhatsApp и код для связывания.
— Я плачу тебе 10$ за аккаунт на 8 часов.
— Ты не заходишь в WhatsApp, пока он в аренде.
2.  Как зарегистрировать аккаунт:
Если у вас есть аккаунт, либо же нет, регистрируетесь(проблем зарегестрироваться в ватсапе не должно быть) , дальше нужно прогреть акк вкладка ниже ⬇️ 
3. Как прогреть акк:
Греть не так сложно, но относительно обязательно дабы акки стояли живыми на часы. 5 звонков по 5 минут, 5 чатов по 15 сообщений, 6 гс можно на 1 секунду. Сообщения можно в тупую протыкать Т9.
4.  Суть работы:
— Ты даешь мне номер своего WhatsApp и код для связывания.
— Я плачу тебе 10$ за аккаунт на 8 часов.
— Ты не заходишь в WhatsApp, пока он в аренде.

Для чего используется аккаунт?
— Только для рекламы магазинов (WB, OZON, MAAG и другие).
— Важно: Твои личные контакты не используются для рассылки! У магазинов своя база номеров.
— Никаких незаконных действий! Только легальная реклама.

Оплата:
— Каждый день в 21:00-22:00 на твой счет.(криптокошелёк)

Условия:
— Аккаунт должен быть активным.
— Не заходить в WhatsApp, пока он в аренде.

    
⚠️ Прочитайте все внимательно до конца! После прочтения писать @llzgg1 в личные сообщения!"""

    # клавиатура с кнопкой подтверждения
    confirm_keyboard = types.InlineKeyboardMarkup()
    confirm_btn = types.InlineKeyboardButton(
        "✅ Я прочитал(а) полностью", callback_data="confirm_read"
    )
    confirm_keyboard.add(confirm_btn)

    #  мануал с кнопкой подтверждения
    bot.send_message(
        message.chat.id, manual_text, reply_markup=confirm_keyboard, parse_mode="HTML"
    )


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if user_states.get(message.from_user.id) == "waiting_question":

        username = (
            f"@{message.from_user.username}"
            if message.from_user.username
            else "без username"
        )
        report = f"✉️ Новый вопрос от пользователя {username} (ID: {message.from_user.id}):\n\n{message.text}"
        bot.send_message(ADMIN_ID, report)

        user_states.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "✅ Ваш вопрос отправлен админу! Спасибо!")


# Запуск бота
if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()
