import time
import os
import threading

import telebot  # type:ignore
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton  # type:ignore
from dotenv import load_dotenv

from Events.events_manager import new_event, handle_year, handle_month, handle_day  # type:ignore
from Events.event import load_events
from Tasks.tasks_manager import new_task, handle_task_date
from Reminder.reminder import items_reminder, setup_default_reminders, change_item_reminder, save_new_hour, set_new_time, list_tasks  # type: ignore


load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise EnvironmentError("Missing bot token")

bot = telebot.TeleBot(TOKEN)
setup_default_reminders(bot)


@bot.message_handler(commands=["configure"])
def configure_settings(message):
    """Muestra el menú para añadir un evento o una tarea."""
    configure_markup = InlineKeyboardMarkup()
    configure_markup.add(
        InlineKeyboardButton("Horario de avisos", callback_data="item_remind_time")
    )
    configure_markup.add(InlineKeyboardButton("Otro (en developing)", callback_data="No"))
    bot.send_message(
        message.chat.id, "¿Qué quieres configurar?", reply_markup=configure_markup
    )

@bot.message_handler(commands=["new"])
def new_item(message):
    """Muestra el menú para añadir un evento o una tarea."""
    add_markup = InlineKeyboardMarkup()
    add_markup.add(InlineKeyboardButton("📅 Evento", callback_data="event"))
    add_markup.add(InlineKeyboardButton("✅ Tarea", callback_data="task"))
    bot.send_message(message.chat.id, "¿Qué quieres añadir?", reply_markup=add_markup)


@bot.message_handler(commands=["list"])
def list_items(message):
    add_markup = InlineKeyboardMarkup()
    add_markup.add(InlineKeyboardButton("📅 Eventos", callback_data="events"))
    add_markup.add(InlineKeyboardButton("✅ Tareas", callback_data="tasks"))
    bot.send_message(message.chat.id, "¿Qué quieres listar?", reply_markup=add_markup)


@bot.callback_query_handler(func=lambda call: call.data in ["event", "task"])
def handle_event(call):
    if call.data == "event":
        new_event(bot, call)
    elif call.data == "task":
        new_task(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("year_"))
def callback_year(call):
    handle_year(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("month_"))
def callback_month(call):
    handle_month(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
def callback_day(call):
    handle_day(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("date_"))
def callback_task_day(call):
    handle_task_date(bot, call)


@bot.callback_query_handler(func=lambda call: call.data == "events")
def list_events(call):
    events_markup = InlineKeyboardMarkup()
    for event in load_events():
        events_markup.row(
            InlineKeyboardButton(f"{event.name}", callback_data="ignore"),
            InlineKeyboardButton("Delete", callback_data=f"delete_{event.name}"),
        )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Eventos guardados",
        reply_markup=events_markup,
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func = lambda call: call.data == "tasks")
def handle_list_tasks(call):
    list_tasks(bot)

@bot.callback_query_handler(func = lambda call: call.data == "item_remind_time")
def handle_remind_time(call):
    change_item_reminder(bot, call)

@bot.callback_query_handler(func = lambda call: call.data.startswith("hour_"))
def handle_new_hour(call):
    save_new_hour(bot, call)
    
@bot.callback_query_handler(func = lambda call: call.data.startswith("minute_"))
def handle_new_time(call):
    set_new_time(bot, call)
 
@bot.callback_query_handler(func = lambda call: call.data.startswith("pospone_"))
def handle_pospone_task(call):
    new_task(bot, call, pospone=True)

def run_bot() -> None:
    try:
        items_reminder.start()
        print(items_reminder.get_jobs())
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        items_reminder.shutdown()
        bot.stop_polling()
    except Exception as e:
        print(f"Error en polling: {e}")
        time.sleep(5)
        run_bot()


if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=items_reminder.start)
    scheduler_thread.start()
    run_bot()
