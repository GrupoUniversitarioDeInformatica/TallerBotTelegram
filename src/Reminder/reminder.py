from tzlocal import get_localzone
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler #type:ignore
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup #type:ignore

from Events.event import load_events #type:ignore
from Tasks.task import load_tasks #type:ignore

local_timezone = get_localzone()
items_reminder = BackgroundScheduler(timezone = local_timezone)

new_time: dict[str, int] = {}

def list_events(bot):
    message = "EVENTOS\n"
    for event in load_events():
        print(event.event_date, "\n",f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year}")
        if event.event_date == f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year}":
            message += f" -{event.name} {event.event_date} {event.description}\n"
    bot.send_message(
        "1501345393",
        message
    )
    
def list_tasks(bot):
    task_markup = InlineKeyboardMarkup()
    message = "TAREAS\n"
    for task in load_tasks():
        if task.task_date == f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year}":
            task_markup.add(InlineKeyboardButton(f"{message} - {task.name} {task.task_date} {task.description}", callback_data="ignore"))
            task_markup.row(
                InlineKeyboardButton("Posponer", callback_data = f"pospone_{task.name}"),
                InlineKeyboardButton("Completada", callback_data = f"completed_{task.name}")
            )
    bot.send_message(
        "1501345393",
        message,
        reply_markup=task_markup
    )

def change_item_reminder(bot, call) -> None:
    markup = InlineKeyboardMarkup()
    hours = [
        InlineKeyboardButton(str(i), callback_data=f"hour_{i}")
        for i in range(0, 24)
    ]
    
    for i in range(0, len(hours), 6):
        markup.row(*hours[i : i + 6])
        
    bot.edit_message_text(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        text = "Selecciona una nueva hora",
        reply_markup = markup
    )

def save_new_hour(bot, call):
    """Guarda el nombre de la tarea y solicita la fecha."""
    new_time["hour"] = call.data.split("_")[1]
    ask_new_minute(bot, call)

def ask_new_minute(bot, call):
    """Solicita la fecha con opciones 'Mañana' y 'Próxima semana'."""
    markup = InlineKeyboardMarkup()
    minutes = [
        InlineKeyboardButton(str(i), callback_data=f"minute_{i}")
        for i in range(0, 60)
    ]
    
    for i in range(0, len(minutes), 10):
        markup.row(*minutes[i : i + 10])
        
    bot.edit_message_text(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        text = "Selecciona un nuevo minuto",
        reply_markup = markup
    )

def set_new_time(bot, call):
    new_time["minute"] = call.data.split("_")[1]
    
    items_reminder.add_job(
        lambda: list_events(bot),
        "cron",
        hour = new_time["hour"],
        minute = new_time["minute"],
        second=0,
        id = "daily_event_list",
        replace_existing=True
    )
    items_reminder.add_job(
        lambda: list_tasks(bot),
        "cron",
        hour = new_time["hour"],
        minute = new_time["minute"],
        second=0,
        id = "daily_tasks_list",
        replace_existing=True
    )
    
    bot.edit_message_text(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        text = "Hora de avisos cambiada correctamente",
        reply_markup = None
    )
   
def setup_default_reminders(bot):
    """Configura y agrega los trabajos al scheduler."""
    items_reminder.add_job(
        lambda: list_events(bot),
        "cron",
        hour=8,
        minute=30,
        second=0,
        id="daily_event_list",
        replace_existing=True
    )
    items_reminder.add_job(
        lambda: list_tasks(bot),
        "cron",
        hour=8,
        minute=30,
        second=0,
        id="daily_tasks_list",
        replace_existing=True
    )