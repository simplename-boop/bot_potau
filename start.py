from ManageBot import create_managed_bot

if __name__ == "__main__":
    bot = create_managed_bot(use_openrouter=False)
    bot.run()