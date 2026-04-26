import json
from aiogram import Bot, Dispatcher, types
import ctypes
import os

def load_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "..", "user.json")
        with open(config_path, "r", encoding="utf-8") as v:
            data = json.load(v)
            return data
    except FileNotFoundError:
        print("i cant found 'user.json'\n")

display_pass = True
get = load_data()
TOKEN = get["token_1"]
ADMIN_ID = get["admin"]
bot = Bot(token=TOKEN)

async def moff_command(message: types.Message):
    if display_pass:
        if message.from_user.id != ADMIN_ID:
            return
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
    return await bot.send_message(ADMIN_ID, "display was turned off")


async def mon_command(message: types.Message):
    if display_pass:
        if message.from_user.id != ADMIN_ID:
            return
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
    ctypes.windll.user32.mouse_event(0x0001, 1, 1, 0, 0)
    ctypes.windll.user32.mouse_event(0x0001, -1, -1, 0, 0)
    return await bot.send_message(ADMIN_ID, "display was turned on")


async def mlock_command(message: types.Message):
    if display_pass:
        if message.from_user.id != ADMIN_ID:
            return
    ctypes.windll.user32.LockWorkStation()
    return await bot.send_message(ADMIN_ID, "display was locked")


async def mon_start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    global display_pass
    display_pass = False
    commands = {
        "on": mon_command,
        "off": moff_command,
        "lock": mlock_command,
    }

    args = message.text.split()

    if len(args) < 2:
        return await message.reply("arguments: on, off, lock")

    action = args[1].lower()
    command_func = commands.get(action)

    if command_func:
        response = await command_func(ADMIN_ID)
        if response:
            pass
        else:
            await bot.send_message(ADMIN_ID, f"Команда {action} выполнена, но отчет не получен.")
    else:
        await message.reply("unknown argument\narguments: on, off, lock")