import telebot
from telebot import types
import ctypes 
import subprocess
from dotenv import load_dotenv
import os
from pathlib import Path
import winreg



load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

restart_pc_password = os.getenv("RESTART_PC_PASSWORD")
pc_off_password = os.getenv("PC_OFF_PASSWORD")
bot = telebot.TeleBot(BOT_TOKEN)


brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"





SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02


def set_wallpaper(image_path: str) -> None:
    abs_path = str(Path(image_path).resolve())
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        abs_path,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
    )
    if not result:
        raise ctypes.WinError()


@bot.message_handler(commands=['start'])
def start_menu(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)



    bt1 = types.KeyboardButton('Sleep😴')
    bt2 = types.KeyboardButton('Block❌')
    bt3 = types.KeyboardButton('Brave🥶')
    bt4 = types.KeyboardButton('Restart🤫')
    bt5 = types.KeyboardButton('Off pc🫪')
    bt6 = types.KeyboardButton('Change wallpaper📃')
    markup.add(bt1, bt2, bt3, bt4, bt5, bt6)


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
    if message.text == str(restart_pc_password):
        os.system("shutdown /r /f /t 0")
        bot.send_message(message.chat.id, 'Successful! Restarting')
    else:
        bot.send_message(message.chat.id, 'Wrong password')
@bot.message_handler(func=lambda message: message.text in ['Off pc🫪'])
def pc_off(message):
    msg = bot.send_message(message.chat.id, 'Send password: ')
    bot.register_next_step_handler(msg, check_password)
def check_password(message):
    if message.text == str(pc_off_password):
        os.system("shutdown /s /t 0")
        bot.send_message(message.chat.id, 'Successful! PC OFF')
    else:
        bot.send_message(message.chat.id, 'Wrong password')

@bot.message_handler(func=lambda message: message.text in ['Change wallpaper📃'])
def get_photo(message):
    msg = bot.send_message(message.chat.id, 'send photo')
    bot.register_next_step_handler(msg, change_wallpaper)
def change_wallpaper(message):
        try:

            if message.content_type == 'photo':

                file_id = message.photo[-1].file_id

            elif message.content_type == 'document':
                if not message.document.mime_type.startswith('image/'):
                    bot.reply_to(message, "Send photo!")
                    return
                file_id = message.document.file_id


            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)


            wallpaper_path = os.path.abspath("current_wallpaper.jpg")
            with open(wallpaper_path, 'wb') as new_file:
                new_file.write(downloaded_file)



            ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)

            bot.reply_to(message, "Wallpaper successful changed!")

        except Exception as e:
            bot.reply_to(message, f"Erorr: {e}")





bot.infinity_polling()