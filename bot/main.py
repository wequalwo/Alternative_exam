import config as cfg
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from simple_r import *
from advanced_r import *

import markups as men

bot = Bot(token = cfg.TOKEN)
dp = Dispatcher(bot)
import pandas as pd


CORE_TYPE = 0
WORDS = []
ADVANCED = []

class Corrector:
    def __init__(self, sts):
        self.status = sts
        self.eng_rep = 'f,dult`;pbqrkvyjghcnea[wxio]sm\'.z'
        self.alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьяюя'

    def correct(self, line):
        line = line.lower()
        if line[0] not in self.alphabet:
            sent_new = ''
            for i in range(len(line)):
                if line[i] == ' ': 
                    line += ' '
                    continue
                else:
                    sent_new += self.alphabet[self.eng_rep.find(line[i])]
            line = sent_new


        if self.status == 1: #Jaccard + Levenstein
            return '🍏Jaccard: ' + JDreco([line])[0] + '\n' + '🍎Levenstein: ' + levenstein([line])[0]
        elif self.status == 2: #ML
            return ML_T9_line(line)
        elif self.status == 3: #advanced
            return ADVANCED.advanced_correct(line)
        elif self.status == 4: #check
            
            return 'В основном словаре: ' + ('✅' if line in WORDS else '❌')  + '\nВ advanced- словаре: '  +  ('✅' if line in ADVANCED.COUNTS else '❌')
        else:
            return '🍏Jaccard: ' + JDreco([line])[0] + '\n🍎Levenstein: ' + levenstein([line])[0]  + '\n🌚ML v2.4: ' + ML_T9_line(line) + '\n🥭Advanced correct: ' + ADVANCED.advanced_correct(line)
        
USERS_DICT = {}
USERS_MODELS = {}
DICT = pd.DataFrame(columns = ['name', 'request'])


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    USERS_DICT[message.from_id] = Corrector(0)
    await message.reply("Напиши мне что-нибудь, а я попробую исправить ошибки!", reply_markup=men.mainMenu)

    print(len(USERS_DICT), message.from_user.username)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь с ошибкой, и я постараюсь исправить твое сообщение!")   

@dp.message_handler()
async def echo_message(msg: types.Message):
    if  msg.text == '⬅️ Back':
        try:
            corrector = USERS_DICT[msg.from_id]
            corrector.status = 0
            await bot.send_message(msg.from_user.id, 'Главное меню. Здесь слова исправляются сразу всеми корректорами.', reply_markup=men.mainMenu)
        except Exception:  
            await bot.send_message(msg.from_user.id, 'Упс, кажется, я Вас не знаю. Давайте знакомиться! Введите команду\n /start')

    elif msg.text == 'Simple Jaccard and Levenstein':
        try:
            corrector = USERS_DICT[msg.from_id]
            corrector.status = 1
            await bot.send_message(msg.from_user.id, 'Простейшие корректоры, основаные на расстоянии Жаккара и Левенштейна, к Вашим услугам', reply_markup=men.otherMenu)
        except Exception:  
            await bot.send_message(msg.from_user.id, 'Упс, кажется, я Вас не знаю. Давайте знакомиться! Введите команду\n /start')

    elif msg.text == 'Machine learning':
        try:
            corrector = USERS_DICT[msg.from_id]
            corrector.status = 2
            await bot.send_message(msg.from_user.id, 'Machine learning:\n 🌚Обращаем ваше внимание на то, что в бот зашружена не самая лучшая версия корректора. Мы работает над этой проблемой...', reply_markup = men.otherMenu)
        except Exception:  
            await bot.send_message(msg.from_user.id, 'Упс, кажется, я Вас не знаю. Давайте знакомиться! Введите команду /start')

    elif msg.text == 'Advanced corrector':
        try:
            corrector = USERS_DICT[msg.from_id]
            corrector.status = 3
            await bot.send_message(msg.from_user.id, 'Advanced corrector. Слова исправляются с помощью поиска ошибки. В случае провала используем голосование остальных корректоров', reply_markup = men.otherMenu)
        except Exception:  
            await bot.send_message(msg.from_user.id, 'Упс, кажется, я Вас не знаю. Давайте знакомиться! Введите команду\n /start')

    elif msg.text == 'Check dictionary':
        try:
            corrector = USERS_DICT[msg.from_id]
            corrector.status = 4
            await bot.send_message(msg.from_user.id, 'Введите слово, а я скажу, есть ли оно в используемых словарях', reply_markup = men.otherMenu)
        except Exception:  
            await bot.send_message(msg.from_user.id, 'Упс, кажется, я Вас не знаю. Давайте знакомиться! Введите команду\n /start')
    elif msg.text == 'Фарид':
        try:
            corrector = USERS_DICT[msg.from_id]
            DICT.loc[len(DICT)] = [msg.from_user.username, msg.text]
            print([msg.from_user.username, msg.text])

            corrector.status = 4
            await bot.send_message(msg.from_user.id, 'Фарид, Михайлов - аспираснт третьего курса СПбГЭТУ "ЛЭТИ", научный руководитель авторов проекта. Более подробную информацию можете найти по ссылке https://www.youtube.com/watch?v=dQw4w9WgXcQ', disable_web_page_preview=True)
        except Exception:  
            await bot.send_message(msg.from_user.id, 'Упс, кажется, я Вас не знаю. Давайте знакомиться! Введите команду\n /start')
    
    
    elif msg.text == '#47':
        print(DICT)
        DICT.to_excel("output.xlsx")
    else:
        try:
            corrector = USERS_DICT[msg.from_id]
            DICT.loc[len(DICT)] = [msg.from_user.username, msg.text]
            qline = corrector.correct(msg.text)
            print([msg.from_user.username, msg.text])
            await bot.send_message(msg.from_user.id, qline)
        except Exception:  
            await bot.send_message(msg.from_user.id, 'Упс, кажется, я Вас не знаю. Давайте знакомиться! Введите команду\n /start')




if __name__ == '__main__':
    with open('list.data', 'rb') as file:  
        WORDS = pickle.load(file)
    ti = learn()
    ADVANCED = Advanced()
    print(ti)
    executor.start_polling(dp)