import requests
import datetime
from db.db_dater import DataBase, main_db_dater


# -----------Класс который ищет по параметрам полученных с бота, так же принимает в себя токен api vk для поиска--------
class VK_users(DataBase):
    def __init__(self, token, **connection):
        DataBase.__init__(self, **connection)
        self.token = token
        self.engine = DataBase.engine_start(self)

    def user_construct(self, user: dict):
        birth_day = int
        if 'city' in user:
            user_city_id = user['city']['id']
            user_city_title = user['city']['title']
        else:
            user_city_id = 0
            user_city_title = 0

        user_gender_id = user['sex']
        if user_gender_id == 2:
            user_gender_title = 'мужской'
        else:
            user_gender_title = 'женский'
        if ('bdate' in user) and (len(user['bdate'].split('.')) > 2):
            birth_day = user['bdate'].split('.')
            user_age = int(datetime.date.today().strftime("%Y")) - int(birth_day[2])
            birth_year = int(birth_day[2])
        else:
            user_age = 0
            birth_year = 0

        user = {'last_name': user['last_name'],
                'first_name': user['first_name'],
                'id': user['id'],
                'city': user_city_id,
                'city_title': user_city_title,
                'gender': user_gender_id,
                'gender_title': user_gender_title,
                'age': user_age,
                'birth_year': birth_year,
                'patronymic': user['screen_name']
                }
        return user

    def get_user_info(self):
        """
        Gets user info from VK account and send it to DataBase
        """
        url = "https://api.vk.com/method/users.get"
        params = {
            'access_token': self.token,
            'v': '5.131',
            'fields': 'city, sex, bdate, screen_name'
        }
        user = requests.get(url, params=params).json()['response'][0]
        constructed_user = self.user_construct(user)
        self.add_user(constructed_user)
        return True

    def info_vk_profiles(self, sex, city, age_from, age_to):
        """
        Find users info from VK accounts and send them to DataBase
        """
        url = "https://api.vk.com/method/users.search"
        params = {
            'count': 5,
            'access_token': self.token,
            'v': '5.131',
            'city': city,
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'has_photo': 1,
            'fields': 'bdate, city, sex, screen_name'
        }
        try:
            users = requests.get(url, params=params).json()['response']['items']
        except:
            print('Что-то пошло не так((')
        for user in users:
            if user['is_closed'] == False:
                constructed_user = self.user_construct(user)
                self.add_user(constructed_user, search=1)
                print(user['id'], user['sex'])
                self.get_photos(constructed_user['id'])
        return users

    def get_photos(self, user_id: int) -> list:
        """
        Gets 3 most liked photos from users accounts and add them to database
        """
        photo_dict = {}
        URL = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id, 'album_id': 'profile', 'extended': 1, 'access_token': self.token, 'v': '5.131'}
        res = requests.get(URL, params=params).json()
        for photo in res['response']['items']:
            photo_dict[f"{photo['owner_id']}_{photo['id']}"] = photo['likes']['count']
        photos = sorted(photo_dict.items(), key=lambda x: x[1], reverse=True)[0:3]
        photos_list = [photo[0] for photo in photos]
        self.add_photos(user_id, photos_list)
        return

def vk_main(token, sex, city, age_from, age_to, **connection):
    users = VK_users(token)
    main_db_dater(**connection)
    users.get_user_info()
    users.info_vk_profiles(sex, city, age_from, age_to)
    return True
