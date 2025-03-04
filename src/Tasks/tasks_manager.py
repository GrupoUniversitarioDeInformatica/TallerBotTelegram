from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton # type:ignore

from .task import Task, pospone_task

# Diccionario para almacenar tareas temporales
task_data = {}

def new_task(bot, call, pospone=False):
    """Inicia la creación de una nueva tarea."""
    if pospone:
        pospone_task(call.data.split("_")[1])
        return
    chat_id = call.message.chat.id
    task_data[chat_id] = {}

    msg = bot.send_message(
        chat_id, 
        "✏️ Escribe el *nombre* de la tarea:", 
        parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, lambda message: save_task_name(bot, message))

def save_task_name(bot, message):
    """Guarda el nombre de la tarea y solicita la fecha."""
    chat_id = message.chat.id
    task_data[chat_id]["name"] = message.text.strip()
    print(f"📌 Nombre guardado: {task_data[chat_id]['name']}")

    ask_task_date(bot, chat_id)

def ask_task_date(bot, chat_id):
    """Solicita la fecha con opciones 'Mañana' y 'Próxima semana'."""
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📅 Mañana", callback_data="date_tomorrow"),
        InlineKeyboardButton("📅 Próxima semana", callback_data="date_next_week")
    )

    bot.send_message(
        chat_id,
        "📅 ¿Cuándo deseas realizar esta tarea?",
        reply_markup=markup,
        parse_mode="Markdown"
    )

def handle_task_date(bot, call):
    """Guarda la fecha elegida y solicita la descripción."""
    chat_id = call.message.chat.id

    if call.data == "date_tomorrow":
        selected_date = datetime.today() + timedelta(days=1)
    else: 
        today = datetime.today()
        days_until_monday = (7 - today.weekday()) % 7 or 7  # Si es lunes, suma 7 días
        selected_date = today + timedelta(days=days_until_monday)

    task_data[chat_id]["task_date"] = selected_date.strftime("%d/%m/%Y")
    print(f"📌 Fecha guardada: {task_data[chat_id]['task_date']}")

    msg = bot.send_message(chat_id, "📝 Escribe una *descripción* para la tarea:", parse_mode="Markdown")
    bot.register_next_step_handler(msg, lambda message: save_task_description(bot, message))

def save_task_description(bot, message):
    """Guarda la descripción y confirma la tarea."""
    chat_id = message.chat.id
    task_data[chat_id]["description"] = message.text.strip()
    print(f"📌 Descripción guardada: {task_data[chat_id]['description']}")

    bot.send_message(
        chat_id,
        f"✅ *Tarea guardada:*\n"
        f"📅 *Fecha:* {task_data[chat_id]['task_date']}\n"
        f"📌 *Nombre:* {task_data[chat_id]['name']}\n"
        f"📝 *Descripción:* {task_data[chat_id]['description']}",
        parse_mode="Markdown"
    )

    # Guardar la tarea en el sistema
    task = Task(
        name=task_data[chat_id]["name"],
        task_date=task_data[chat_id]["task_date"],
        description=task_data[chat_id]["description"]
    )
    task.save_task()

    # Eliminar los datos temporales
    del task_data[chat_id]
