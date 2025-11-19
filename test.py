from prompt import *
from vk_service import *
from deepseek_service import *
from keys import *

history = get_histoty(10)

print(history)

prompt, ms = prompt_for_normal_msg(history, MY_FROM_ID)

print("Итоговый промпт:\n")

ans = ask_for_deepseek(prompt)

print()
print("Ответ:\n")

print(ans)
