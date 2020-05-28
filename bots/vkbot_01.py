from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from datetime import datetime
import random
import time

login, password = '89243802946', 'trynottodie'
vk_session = vk_api.VkApi(login=login, password=password, app_id=2685278)
try:
    vk_session.auth(token_only=True)
    print('Succesfully authorised')
except vk_api.AuthError as error_msg:
    print(error_msg)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Сообщение пришло в: ', str(datetime.strftime(datetime.now(), '%H:%M:%S')))
        print('Текст сообщения: ' + str(event.text))
        print(event.user_id)
        response = event.text.lower()
        if event.from_user and not event.from_me:
            if response == "12!":
                vk_session.method('messages.send', {'user_id': event.user_id,
                                                    'message': 'И тебе привет от бота!', 'random_id': 0})
            

