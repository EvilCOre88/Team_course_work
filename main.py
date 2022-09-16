import configparser

from VK.chat_bot import Vk_bot


if __name__ == '__main__':
    """
    Run module of programm.
    Set tokens and database connection info into
    main method from chat_bot.py and start a programm
    """
    config = configparser.ConfigParser()
    config.read(('settings.ini'))
    user_token = config['VK']['token']
    bot_token = config['VK']['bot_token']
    postgres_db_host = config['DB']['db_host']
    postgres_db_name = config['DB']['db_name']
    postgres_username = config['DB']['username']
    postgres_password = config['DB']['password']

    connection = {'drivername': 'postgresql',
                    'username': postgres_username,
                    'password': postgres_password,
                    'host': postgres_db_host,
                    'port': 5432,
                    'database': postgres_db_name
                    }

    vk_bot = Vk_bot(user_token, bot_token, **connection)
    vk_bot.main_bot()