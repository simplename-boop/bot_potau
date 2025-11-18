import time
from deepseek_service import ask_for_deepseek
from prompt import prompt_for_normal_msg
from vk_service import send_vk_msg, get_histoty


def main():
    last_msg_time = 0
    count_msg_histoty = 30
    my_id = "261497022"
    while True:
        try:
            msg_history = get_histoty(count_msg_histoty)
            if msg_history:
                new_msg_time = msg_history[-1]["date"]
                last_from_id = str(msg_history[-1]["from_id"])
                if new_msg_time > last_msg_time and last_from_id != my_id:
                    prompt, msgs = prompt_for_normal_msg(msg_history, my_id)
                    msg = ask_for_deepseek(prompt)
                    send_vk_msg(msg)

                    lines = msgs.split('\n')
                    for line in lines[-5:]:
                        print(line)

                    last_msg_time = new_msg_time
        except Exception as e:
            print(f"Ошибка: {e}")

        time.sleep(5)

if __name__ == "__main__":
    main()
