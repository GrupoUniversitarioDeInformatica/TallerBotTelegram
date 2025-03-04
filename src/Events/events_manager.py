from datetime import datetime
import calendar
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton  # type:ignore

from .event import Event

event_data = {}


def new_event(bot, call):
    """Solicita el nombre del evento."""
    event_data = {}

    msg = bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="✏️ Escribe el *nombre* del evento:",
        reply_markup=None,
        parse_mode="Markdown",
    )

    bot.register_next_step_handler(
        msg, lambda message: save_event_name(bot, message, call)
    )


def save_event_name(bot, message, call):
    """Guarda el nombre del evento y pide el año."""
    event_data["name"] = message.text.strip()

    ask_year(bot, call)


def ask_year(bot, call):
    """Solicita la selección del año."""
    actual_year = datetime.today().year
    year_markup = InlineKeyboardMarkup()

    year_markup.row(
        InlineKeyboardButton(str(actual_year), callback_data=f"year_{actual_year}"),
        InlineKeyboardButton(
            str(actual_year + 1), callback_data=f"year_{actual_year + 1}"
        ),
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📅 Selecciona el **año**:",
        reply_markup=year_markup,
        parse_mode="Markdown",
    )


def handle_year(bot, call):
    event_data["year"] = int(call.data.split("_")[1])

    ask_month(bot, call)


def ask_month(bot, call):
    """Solicita la selección del mes."""
    month_markup = InlineKeyboardMarkup()
    months = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]
    botones = [
        InlineKeyboardButton(month, callback_data=f"month_{i}")
        for i, month in enumerate(months, start=1)
    ]

    for i in range(0, len(botones), 4):
        month_markup.row(*botones[i : i + 4])  # Añadir una fila de 4 botones

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📅 Selecciona el **mes**:",
        reply_markup=month_markup,
        parse_mode="Markdown",
    )


def handle_month(bot, call):
    event_data["month"] = int(call.data.split("_")[1])

    ask_day(bot, call)


def ask_day(bot, call):
    year = event_data["year"]
    month = event_data["month"]
    max_days = calendar.monthrange(year, month)[1]

    day_markup = InlineKeyboardMarkup()
    botones = [
        InlineKeyboardButton(str(i), callback_data=f"day_{i}")
        for i in range(1, max_days + 1)
    ]

    for i in range(0, len(botones), 7):
        day_markup.row(*botones[i : i + 7])

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"📅 Selecciona el *día válido* ({max_days} días en {month}/{year}):",
        reply_markup=day_markup,
        parse_mode="Markdown",
    )


def handle_day(bot, call):
    event_data["day"] = int(call.data.split("_")[1])
    event_date = datetime(event_data["year"], event_data["month"], event_data["day"])
    event_data["event_date"] = event_date.strftime("%d/%m/%Y")
    msg = bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📝 Escribe una *descripción* para el evento:",
        reply_markup=None,
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(
        msg, lambda message: save_event_description(bot, message, call)
    )


def save_event_description(bot, message, call):
    event_data["description"] = message.text.strip()

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ *Evento guardado:*\n"
            f"📅 *Fecha:* {event_data['event_date']}\n"
            f"📌 *Nombre:* {event_data['name']}\n"
            f"📝 *Descripción:* {event_data['description']}",
        reply_markup=None,
        parse_mode="Markdown",
    )
    event = Event(
        name=event_data["name"],
        event_date=event_data["event_date"],
        description=event_data["description"],
    )
    event.save_event()
