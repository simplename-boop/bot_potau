import time
import threading
from deepseek_service import ask_for_deepseek, ask_openrouter
from prompt import prompt_for_normal_msg, prompt_for_stupid_msg
from vk_service import send_vk_msg, get_histoty
from keys import MY_FROM_ID, MUR_FROM_ID, AND_FROM_ID


class ManagedVKBot:
    def __init__(self, use_openrouter=True):
        self.use_openrouter = use_openrouter
        self.count_msg_history = 50
        self.smart_bot_running = False
        self.stupid_bot_running = False

        self.last_processed_id = None
        self.smart_bot_thread = None
        self.stupid_bot_thread = None

        self.commands = {
            "!start_potau_bot1": self.start_smart_bot,
            "!stop_potau_bot1": self.stop_smart_bot,
            "!start_potau_bot2": self.start_stupid_bot,
            "!stop_potau_bot2": self.stop_stupid_bot,
            "!status": self.show_status,
            "!help": self.help
        }


    def ask_ai(self, prompt):
        if self.use_openrouter:
            return ask_openrouter(prompt)
        else:
            return ask_for_deepseek(prompt)

    def check_commands(self):
        try:
            msg_history = get_histoty(10)
            if not msg_history:
                return

            last_msg = msg_history[-1]
            id_msg = last_msg["id"]
            text = last_msg.get("text", "").strip().lower()
            from_id = str(last_msg["from_id"])

            if (from_id != MY_FROM_ID and from_id != MUR_FROM_ID and from_id != AND_FROM_ID) or id_msg == self.last_processed_id:
                return

            if text in self.commands:
                print(f"Команда: {text}")
                self.commands[text]()
                self.last_processed_id = id_msg

        except Exception as e:
            print(f"Ошибка: {e}")


    def smart_bot_loop(self):
        last_msg_time = 0
        print("Умный бот старт\n")
        while self.smart_bot_running:
            try:
                msg_history = get_histoty(self.count_msg_history)
                if msg_history:
                    new_msg_time = msg_history[-1]["date"]
                    last_from_id = str(msg_history[-1]["from_id"])

                    if new_msg_time > last_msg_time and last_from_id != MY_FROM_ID:
                        prompt, msgs = prompt_for_normal_msg(msg_history, MY_FROM_ID)
                        msg = self.ask_ai(prompt)
                        send_vk_msg(msg)

                        lines = msgs.split('\n')
                        for line in lines[-5:]:
                            print(line)

                        last_msg_time = new_msg_time

            except Exception as e:
                print(f"Ошибка: {e}")

            time.sleep(5)

    def stupid_bot_loop(self):
        print("Тупой бот старт\n")
        while self.stupid_bot_running:
            try:
                prompt = prompt_for_stupid_msg()
                ans = self.ask_ai(prompt)
                r = send_vk_msg(ans)
                print("Отправлено:", r.json())
            except Exception as e:
                print(f"Ошибка: {e}")

            for i in range(4*30*2):
                if not self.stupid_bot_running:
                    break
                time.sleep(30)
    def start_smart_bot(self):
        if not self.smart_bot_running:
            self.smart_bot_running = True
            self.smart_bot_thread = threading.Thread(target=self.smart_bot_loop, daemon=True)
            self.smart_bot_thread.start()
            print("Умный бот запущен")
            send_vk_msg("---ПЕРВЫЙ ПОТАУ БОТ ЗАПУЩЕН---")

    def stop_smart_bot(self):
        if self.smart_bot_running:
            self.smart_bot_running = False
            if self.smart_bot_thread:
                self.smart_bot_thread.join(timeout=5)
            print("Умный бот остановлен")
            send_vk_msg("---ПЕРВЫЙ ПОТАУ БОТ ОСТАНОВЛЕН---")

    def start_stupid_bot(self):
        if not self.stupid_bot_running:
            self.stupid_bot_running = True
            self.stupid_bot_thread = threading.Thread(target=self.stupid_bot_loop, daemon=True)
            self.stupid_bot_thread.start()
            print("Тупой бот запущен")
            send_vk_msg("---ВТОРОЙ ПОТАУ БОТ ЗАПУЩЕН---")

    def stop_stupid_bot(self):
        if self.stupid_bot_running:
            self.stupid_bot_running = False
            if self.stupid_bot_thread:
                self.stupid_bot_thread.join(timeout=5)
            print("Тупой бот остановлен")
            send_vk_msg("---ВТОРОЙ ПОТАУ БОТ ОСТАНОВЛЕН---")

    def help(self):
        print("Помощь")
        help_text = """
            Команды:
            !start_potau_bot1
            !start_potau_bot2  
            !stop_potau_bot1
            !stop_potau_bot2
            !status
            !help
        """
        send_vk_msg(help_text)

    def show_status(self):
        status = f"""Статус ботов:
        ПЕРВЫЙ ПОТАУ БОТ: {'Запущен' if self.smart_bot_running else 'Остановлен'}
        ВТОРОЙ ПОТАУ БОТ: {'Запущен' if self.stupid_bot_running else 'Остановлен'}"""
        send_vk_msg(status)
        print("Статус отправлен")

    def run(self):
        print("Запуск системы")
        while True:
            try:
                self.check_commands()
            except Exception as e:
                print("Ошибка:")
            time.sleep(5)


def create_managed_bot(use_openrouter=True):
    return ManagedVKBot(use_openrouter=use_openrouter)
