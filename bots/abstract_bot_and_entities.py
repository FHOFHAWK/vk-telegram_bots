import vk_api
import server.main_server as server

from abc import abstractmethod, ABC
from telebot import TeleBot, types
from system.constants import TELEGRAM_BOT_TOKEN, VK_BOT_TOKEN, STR_HELLO_IN_CHOSEN_CHANEL, TELEGRAM_MESSENGER, \
    VK_MESSENGER
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

markup_teleg = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
change_channel_btn = types.KeyboardButton('Сменить канал коммуникации')
markup_teleg.add(change_channel_btn)

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Сменить канал коммуникации', color=VkKeyboardColor.PRIMARY)


class BotEntity(ABC):
    @abstractmethod
    def send_mes_in_new_platform(self, user_id):
        pass


class TelegramBot(BotEntity):
    telegram_bot = TeleBot(TELEGRAM_BOT_TOKEN)

    def __init__(self):
        @self.telegram_bot.message_handler(content_types=['text'])
        def send_message(message):
            answer = server.get_answer_from_server(message.text.lower(), message.from_user.id,
                                                   TELEGRAM_MESSENGER['messenger_name'])
            self.telegram_bot.send_message(message.from_user.id, answer, reply_markup=markup_teleg)

        self.telegram_bot.polling()

    def send_mes_in_new_platform(self, user_id):
        self.telegram_bot.send_message(user_id, STR_HELLO_IN_CHOSEN_CHANEL, reply_markup=markup_teleg)


class VKBot(BotEntity):
    vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)

    def __init__(self):
        longpoll = VkLongPoll(self.vk_session)
        vk = self.vk_session.get_api()
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    new_message_from_user = event.text.lower()  # сохраняем полученное сообщение
                    id = event.user_id  # сохраняем id

                    # отправляем сообщение, id, тип платформы серверу на обработку
                    answer = server.get_answer_from_server(new_message_from_user, id, VK_MESSENGER['messenger_name'])
                    self.vk_session.method('messages.send', {'user_id': id, 'message': answer, 'random_id': 0,
                                                             'keyboard': keyboard.get_keyboard()})

    def send_mes_in_new_platform(self, user_id):
        self.vk_session.method('messages.send',
                               {'user_id': user_id, 'message': STR_HELLO_IN_CHOSEN_CHANEL,
                                'random_id': 0, 'keyboard': keyboard.get_keyboard()})
