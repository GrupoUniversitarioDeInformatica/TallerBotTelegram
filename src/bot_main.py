import telebot
from dotenv import load_dotenv
import time
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    raise EnvironmentError("Missing critical environment variables. Check .env file.")

bot.telebot.Telebot(TOKEN)

@bot.message_handler(commands=['new'])
def new_event(message):
	pass

@bot.message_handler(commands=['list'])
def list_events(message):
	pass

@bot.message_handler(commands=['edit'])
def edit_event(message):

def run_bot() -> None:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        error_log.write_error(" Bot detenido por el usuario (Ctrl+C)\n")
        bot.stop_polling()
    except Exception as e:
        error_log.write_error(f" Error: {e}. Reintentando en 5 segundos...\n")
        time.sleep(5)
        run_bot()

if __name__ == '__main__':
    run_bot()
