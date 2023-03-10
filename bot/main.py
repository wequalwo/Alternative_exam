TOKEN = '6225529145:AAEiic5AitqYpKRV16C2tYOCDKHUAvcZnKY'
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


from simple_r import *
from advanced_r import *

import markups as men

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

CORE_TYPE = 0
WORDS = []
ADVANCED = []


class Corrector:
    def __init__(self, sts):
        self.status = sts
    def correct(self, line):
        line = line.lower()
        if self.status == 1: #Jaccard + Levenstein
            return '🍏Jaccard: ' + JDreco([line])[0] + '\n' + '🍎Levenstein: ' + levenstein([line])[0]
        elif self.status == 2: #ML
            return ML_T9_line(line)
        elif self.status == 3: #advanced
            return ADVANCED.advanced_correct(line)
        elif self.status == 4: #check
            
            return 'В основном словаре: ' + ('✅' if line in WORDS else '❌')  + '\nВ advanced- словаре: '  +  ('✅' if line in ADVANCED.COUNTS else '❌')
        else:
            return '🍏Jaccard: ' + JDreco([line])[0] + '\n🍎Levenstein: ' + levenstein([line])[0]  + '\n💩ML v1.2: ' + ML_T9_line(line) + '\n🥭Advanced correct: ' + ADVANCED.advanced_correct(line)
        
USERS_DICT = {}
USERS_MODELS = {}

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    USERS_DICT[message.from_id] = Corrector(0)
    await message.reply("Напиши мне что-нибудь неприличное!", reply_markup=men.mainMenu)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь с ошибкой, и я постараюсь исправить твое сообщение!")   

@dp.message_handler()
async def echo_message(msg: types.Message):
    if  msg.text == '⬅️ Back':
        corrector = USERS_DICT[msg.from_id]
        corrector.status = 0
        await bot.send_message(msg.from_user.id, 'Главное меню. Здесь слова исправляются сразу всеми корректорами.', reply_markup=men.mainMenu)

    elif msg.text == 'Simple Jaccard and Levenstein':
        corrector = USERS_DICT[msg.from_id]
        corrector.status = 1
        await bot.send_message(msg.from_user.id, 'Простейшие корректоры, основаные на расстоянии Жаккара и Левенштейна, к Вашим услугам', reply_markup=men.otherMenu)

    elif msg.text == 'Machine learning':
        corrector = USERS_DICT[msg.from_id]
        corrector.status = 2
        await bot.send_message(msg.from_user.id, 'Machine learning:\n 💩Обращаем ваше внимание на то, что загрузить полноценную версию корректора, основанного на машинном обучении, в бота пока не удалось. Здесь лежит ущербная версия...', reply_markup = men.otherMenu)
    
    elif msg.text == 'Advanced corrector':
        corrector = USERS_DICT[msg.from_id]
        corrector.status = 3
        await bot.send_message(msg.from_user.id, 'Advanced corrector. Слова исправляются с помощью поиска ошибки. В случае провала используем голосование остальных корректоров', reply_markup = men.otherMenu)

    elif msg.text == 'Check dictionary':
        corrector = USERS_DICT[msg.from_id]
        corrector.status = 4
        await bot.send_message(msg.from_user.id, 'Введите слово, а я скажу, есть ли оно в используемых словарях', reply_markup = men.otherMenu)

    else:
        corrector = USERS_DICT[msg.from_id]
        qline = corrector.correct(msg.text)
        await bot.send_message(msg.from_user.id, qline)



if __name__ == '__main__':
    with open('list.data', 'rb') as file:  
        WORDS = pickle.load(file)
    ti = learn()
    ADVANCED = Advanced()
    print(ti)
    executor.start_polling(dp)