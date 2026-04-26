import socket
import requests
import subprocess
from aiogram import Bot, Dispatcher, types
import re
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json

def load_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "..", "user.json")
        with open(config_path, "r", encoding="utf-8") as v:
            data = json.load(v)
            return data
    except FileNotFoundError:
        print("i cant found 'user.json'\n")

get = load_data()
TOKEN = get["token_1"]
ADMIN_ID = get["admin"]
bot = Bot(token=TOKEN)



def get_actual_gateway():
    try:
        output = subprocess.check_output("route print -4", shell=True).decode('cp866')
        match = re.search(r"0\.0\.0\.0\s+0\.0\.0\.0\s+([\d.]+)", output)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


try:
    target_ext = requests.get("https://api.ipify.org", timeout=5).text
except Exception:
    target_ext = "Unknown"

TARGET = get_actual_gateway()

PORTS = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 3389, 8080]
TIMEOUT = 0.7


def get_os_guess(ttl):
    if ttl <= 64: return "Linux/Unix/IoT"
    if ttl <= 128: return "Windows"
    return "Unknown Device"


async def probe_port(port, semaphore):
    if not TARGET: return

    async with semaphore:
        try:
            conn = asyncio.open_connection(TARGET, port)
            reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)


            # Отправляем данные
            if port in [80, 8080]:
                writer.write(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            await writer.drain()

            # Читаем баннер
            data = await reader.read(1024)
            banner = data.decode(errors='ignore').strip()[:60]
            writer.close()
            await writer.wait_closed()

            await bot.send_message(ADMIN_ID, f"Port: <code>{port}</code>\nInfo: <code>{banner}</code>",
                                   parse_mode="HTML")

        except Exception:
            pass


async def run():
    await bot.send_message(ADMIN_ID, f"IP: <code>{target_ext}</code>\nTargeting: <code>{TARGET}</code> (Local)", parse_mode="HTML")
    semaphore = asyncio.Semaphore(50)
    tasks = [probe_port(port, semaphore) for port in PORTS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run())