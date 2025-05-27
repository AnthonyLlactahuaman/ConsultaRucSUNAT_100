from Manage.Directory import CompDirectory
from Manage.Bot import CompBot

if __name__ == '__main__':
    dirs = CompDirectory()
    bot = CompBot(dirs)
    bot.main()
