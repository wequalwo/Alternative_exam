from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnBack = KeyboardButton('⬅️ Back')
# -- Main --
btnJaccard = KeyboardButton('Simple Jaccard and Levenstein')
btnML = KeyboardButton('Machine learning')
btnCheck = KeyboardButton('Check dictionary')


mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnJaccard, btnML)


# -- Other -- 
MlMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnBack, btnCheck)
