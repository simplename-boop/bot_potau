from prompt import *
from vk_service import *
from deepseek_service import *

history = get_histoty(10)


my_id = "261497022"

prompt, ms = prompt_for_normal_msg(history, my_id)

print("Итоговый промпт:\n")
print(prompt)


ans = ask_for_deepseek(prompt)

print()
print("Ответ:\n")

print(ans)
