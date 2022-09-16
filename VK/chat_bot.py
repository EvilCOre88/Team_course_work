import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from VK.vk_get_info import VkUsers
from DB.db_dater import DataBase

from sqlalchemy.orm import sessionmaker

from time import sleep


class Vk_bot(VkUsers, DataBase):
    def __init__(self, user_token, bot_token, **connection: dict):
        """
        Sets attribute user_token, bot_token, connection: users token with required rights,
        bot token and connection SQLalchemy driver info. Also initialize session with vk_api
        """
        DataBase.__init__(self, **connection)
        VkUsers.__init__(self, user_token)
        self.bot_token = bot_token
        self.user_token = user_token
        self.connection = connection
        self.vk_session = vk_api.VkApi(token=self.bot_token)
        self.session_api = self.vk_session.get_api()
        self.longpool = VkLongPoll(self.vk_session)

    def send_some_msg(self, id, some_text):
        """
        Send user message preparation
        """
        self.vk_session.method("messages.send", {"user_id": id, "message": some_text, "random_id": "0"})

    def start_chat_bot(self):
        """
        Starts interaction with user for find other persons
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('Старт', color=VkKeyboardColor.SECONDARY)
                self.session_api.messages.send(peer_id=id,
                                          random_id=get_random_id(),
                                          keyboard=keyboard.get_keyboard(),
                                          message=f'Привет! Это бот для поиска своей половинки!\n'
                                                  f'Чтобы найти свою любовь просто нажмите "Старт".')
                self.count_chat_bot()
                break

    def count_keyboard(self, user_id):
        """
        Message with keybord with choosing count of persons
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('5', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('10', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('20', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('30', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('50', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('100', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('200', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('300', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('500', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('1000', color=VkKeyboardColor.SECONDARY)
        self.session_api.messages.send(peer_id=user_id,
                                       random_id=get_random_id(),
                                       keyboard=keyboard.get_keyboard(),
                                       message=f'(или нажмите на один из предложенных):')

    def count_chat_bot(self):
        """
        Start of dialog
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == 'старт' or msg == 'новый поиск':
                    self.send_some_msg(id, 'Введите приблизительное количество собеседников для поиска '
                                           '(не должно превышать 1000 человек).')
                    self.count_keyboard(id)
                    self.choose_sex()
                    break

    def sex_keyboard(self, user_id):
        """
        Message with keybord with choosing sex of persons
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('М', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Д', color=VkKeyboardColor.SECONDARY)
        self.session_api.messages.send(peer_id=user_id,
                                       random_id=get_random_id(),
                                       keyboard=keyboard.get_keyboard(),
                                       message=f'Введите желаемый пол собеседника:\n'
                                               f'М - Мужчина / Д - Девушка')

    def choose_sex(self):
        """
        Choose count of searching persons
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == msg:
                    try:
                        int(msg)
                    except:
                        self.send_some_msg(id, "Введено не число, попробуйте еще раз")
                        continue
                    if int(msg) <= 1000:
                        self.count = int(msg)
                        self.sex_keyboard(id)
                        self.sex_chat_bot()
                    else:
                        self.send_some_msg(id, "Введено число больше 1000, попробуйте еще раз")
                        continue
                    break

    def city_keyboard(self, user_id):
        """
        Message with keybord with choosing city of persons
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Москва', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Хабаровск', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Владивосток', color=VkKeyboardColor.SECONDARY)
        self.session_api.messages.send(peer_id=user_id,
                                  random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard(),
                                  message=f'''Введите город:''')
    def sex_chat_bot(self):
        """
        Choose sex of searching persons
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == "м":
                    self.city_keyboard(id)
                    self.sex = '2'
                    self.city_chat_bot()
                    break
                elif msg == "д":
                    self.city_keyboard(id)
                    self.sex = '1'
                    self.city_chat_bot()
                    break
                else:
                    self.send_some_msg(id, "Таких людей не существует, введите коректно пол")
                    continue

    def age_keyboard(self, user_id):
        """
        Message with keybord with choosing age from of persons
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('20', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('22', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('25', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('27', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('30', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('33', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('35', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('37', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('40', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('43', color=VkKeyboardColor.SECONDARY)
        self.session_api.messages.send(peer_id=user_id,
                                  random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard(),
                                  message = f'''(или нажмите на один из предложенных):''')
    def city_chat_bot(self):
        """
        Choose city of searching persons
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == 'москва':
                    self.city = '1'
                    self.send_some_msg(id, 'Введите возраст ОТ')
                    self.age_keyboard(id)
                    self.age_from_chat_bot()
                    break
                elif msg == 'хабаровск':
                    self.city = '153'
                    self.send_some_msg(id, 'Введите возраст ОТ')
                    self.age_keyboard(id)
                    self.age_from_chat_bot()
                    break
                elif msg == 'владивосток':
                    self.city = '37'
                    self.send_some_msg(id, 'Введите возраст ОТ')
                    self.age_keyboard(id)
                    self.age_from_chat_bot()
                    break
                else:
                    self.send_some_msg(id, "Таких городов я не знаю(( Введите Москва/Хабаровск/Владивосток")
                    continue

    def age_from_chat_bot(self):
        """
        Choose age from of searching persons
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == msg:
                    try:
                        int(msg)
                    except:
                        self.send_some_msg(id, "Введено не число, попробуйте еще раз")
                        continue
                    self.age_from = int(msg)
                    self.send_some_msg(id, 'Введите возраст ДО')
                    self.age_keyboard(id)
                    self.age_to_chat_bot()
                    break

    def age_to_chat_bot(self):
        """
        Choose age to of searching persons
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == msg:
                    try:
                        int(msg)
                    except:
                        self.send_some_msg(id, "Введено не число, попробуйте еще раз")
                        continue
                    self.age_to = int(msg)
                    self.vk_session.method('messages.send', {'user_id': id,
                                                        'message': 'Спасибо за введенные данные поиск может '
                                                                   'занять некоторое время...',
                                                        'attachment': 'photo257448556_457239684',
                                                        'random_id': get_random_id()})
                    break
        return

    def next_user_keyboard(self, user_id):
        """
        Message with keybord with next and add to favorites buttons
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Следующий пользователь', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.SECONDARY)
        self.session_api.messages.send(peer_id=user_id,
                                  random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard(),
                                  message=f'''Выберите действие''')

    def next_user(self, user_id, search_user_id):
        """
        Choose next person in found persons
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == 'следующий пользователь':
                    return 'next'
                elif msg == 'добавить в избранное':
                    self.add_to_favorite(id, search_user_id)
                    return

    def next_favorite_keyboard(self, user_id):
        """
        Message with keybord with next and delete buttons
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Следующий пользователь', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Убрать из избранного', color=VkKeyboardColor.SECONDARY)
        self.session_api.messages.send(peer_id=user_id,
                                  random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard(),
                                  message=f'''Выберите действие''')

    def next_favorite(self, search_user_id):
        """
        Choose next person in favorite persons
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == 'следующий пользователь':
                    return 'next'
                elif msg == 'убрать из избранного':
                    self.delete_from_favorite(id, search_user_id)
                    return

    def send_message(self,user_id, send):
        """
        Messages sending form for show found persons
        """
        message = f'''{send['first_name']} {send['last_name']}\nhttps://vk.com/id{send['id']}'''
        if len(send['photos']) == 3:
            photo = f'''photo{send['photos'][0]},photo{send['photos'][1]},photo{send['photos'][2]}'''
        elif len(send['photos']) == 2:
            photo = f'''photo{send['photos'][0]},photo{send['photos'][1]}'''
        elif len(send['photos']) == 1:
            photo = f'''photo{send['photos'][0]}'''
        else:
            return
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                            'attachment': photo, 'random_id': get_random_id()})

    def next_end_keyboard(self, user_id):
        """
        Message with keybord with new search, list and show favorites buttons
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Посмотреть избранное', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Листать пользователей', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('Новый поиск', color=VkKeyboardColor.SECONDARY)
        self.session_api.messages.send(peer_id=user_id,
                                  random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard(),
                                  message=f'''Вы посмотрели всех пользователей, выберите действие:''')

    def start_keyboard(self, user_id):
        """
        Message with keybord of starting search
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Начать поиск', color=VkKeyboardColor.SECONDARY)
        self.session_api.messages.send(peer_id=user_id,
                                  random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard(),
                                  message='------------------------')

    def next_end(self):
        """
        Last dialog screen after listing of found persons
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == 'посмотреть избранное':
                    self.show_favorites(id)
                elif msg == 'листать пользователей':
                    self.show_results(id)
                elif msg == 'новый поиск':
                    self.start_keyboard(id)
                    self.main_bot()

    def show_results(self, user_id):
        """
        Show results of searching persons to user
        """
        users = self.read_search_user()
        to_send = []
        for user in users:
            to_send.append({'first_name': user[1],
                            'last_name': user[2],
                            'photos': self.read_photos(user[0]),
                            'id': user[0],
                            'sex': user[5],
                            'city': user[6]
                            })

        for send in to_send:
            if len(send['photos']) != 0:
                self.send_message(user_id, send)
                self.next_user_keyboard(user_id)
                if self.next_user(user_id, send['id']) == 'next':
                    continue

        self.next_end_keyboard(user_id)
        self.next_end()
        return

    def end_keyboard(self, user_id):
        """
        Message with keybord with new search and list persons buttons
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Новый поиск', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Листать пользователей', color=VkKeyboardColor.SECONDARY)
        self.session_api.messages.send(peer_id=user_id,
                                  random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard(),
                                  message=f'У вас пока нет никого в избранном(\n'
                                          f'Вы можете начать новый поиск или листать уже найденных пользователей')

    def end(self):
        """
        Last dialog screen
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == 'новый поиск':
                    self.start_keyboard(id)
                    self.main_bot()
                elif msg == 'листать пользователей':
                    self.show_results(id)

    def show_favorites(self, user_id):
        """
        Show favorites persons
        """
        users = self.read_search_user()
        favorites = self.read_favorites()
        fav = [favorite[2] for favorite in favorites]
        to_send = []
        if len(favorites) != 0:
            for user in users:
                if user[0] in fav:
                    to_send.append({'first_name': user[1],
                                    'last_name': user[2],
                                    'photos': self.read_photos(user[0]),
                                    'id': user[0]
                                    })
        else:
            self.end_keyboard(user_id)
            self.end()
        for send in to_send:
            self.send_message(user_id, send)
            self.next_favorite_keyboard(user_id)
            if self.next_favorite(send['id']) == 'next':
                continue

        self.next_end_keyboard(user_id)
        self.next_end()
        return

    def main_bot(self):
        """
        Main method which connect all methods of project:
        Create database
        Search for persons
        Add persons to database
        Show found persons
        Add persons to favorites
        Delete persons from favorites
        Show favorite persons
        """
        work = DataBase(**self.connection)
        engine = work.engine_start()
        create = work.create_table(engine)
        if create:
            print(f'База данных успешно создана!')
        else:
            return print(f'База не создана, что-то пошло не так')

        user = self.get_user_info()
        self.add_user(self.user_construct(user))
        id = self.read_user(user['id'])['user_id']

        self.start_chat_bot()

        users = self.info_vk_profiles(self.sex, self.city, self.age_from, self.age_to, self.count)
        for user in users:
            if user['is_closed'] == False:
                constructed_user = self.user_construct(user)
                self.add_user(constructed_user, search=1)
                print(user['id'], user['sex'])
                photos_list = self.get_photos(constructed_user['id'])
                sleep(0.34)
                self.add_photos(user['id'], photos_list)
        self.show_results(id)

