import configparser

from VK.chat_bot import main_bot


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(('venv/settings.ini'))
    user_token = config['VK']['token']
    bot_token = config['VK']['bot_token']
    postgres_db_host = config['DB']['db_host']
    postgres_db_name = config['DB']['db_name']
    postgres_username = config['DB']['username']
    postgres_password = config['DB']['password']

    connection = {'drivername': 'postgresql+psycopg2',
                    'username': postgres_username,
                    'password': postgres_password,
                    'host': postgres_db_host,
                    'port': 5432,
                    'database': postgres_db_name
                    }

    main_bot(user_token, bot_token, **connection)