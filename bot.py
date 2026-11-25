import telebot
from telebot import types
import ctypes 
import subprocess
from dotenv import load_dotenv
import os




load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

password = os.getenv("DB_PASSWORD")

bot = telebot.TeleBot(BOT_TOKEN)


brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"





@bot.message_handler(commands=['start'])
def start_menu(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)



    bt1 = types.KeyboardButton('Sleep😴')
    bt2 = types.KeyboardButton('Block❌')
    bt3 = types.KeyboardButton('Brave🥶')
    bt4 = types.KeyboardButton('Restart🤫')
    markup.add(bt1, bt2, bt3, bt4)


    bot.send_message(message.chat.id, 'Choose variant', reply_markup=markup)




@bot.message_handler(func=lambda message: message.text in ['Sleep😴'])
def sleep_pc(message):
    ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
    bot.send_message(message.chat.id, 'Successful! pc is sleeping')
@bot.message_handler(func=lambda message: message.text in ['Block❌'])
def block_pc(message):
    ctypes.windll.user32.LockWorkStation()
    bot.send_message(message.chat.id, 'Successful! pc is blocking')
@bot.message_handler(func=lambda message: message.text in ['Brave🥶'])
def open_brave(message):
    subprocess.Popen([brave_path])
    bot.send_message(message.chat.id, 'successful! brave has been opened')
@bot.message_handler(func=lambda message: message.text in ['Restart🤫'])
def restart(message):
    msg = bot.send_message(message.chat.id, 'Send password: ')
    bot.register_next_step_handler(msg, check_password)
def check_password(message):
    if message.text == str(password):
       # os.system("shutdown /r /f /t 0")
        bot.send_message(message.chat.id, 'Successful! Restarting')
    else:
        bot.send_message(message.chat.id, 'Wrong password')

bot.infinity_polling()