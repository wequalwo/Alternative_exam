from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnBack = KeyboardButton('⬅️ Back')
# -- Main --
btnJaccard = KeyboardButton('Simple Jaccard and Levenstein')
btnML = KeyboardButton('Machine learning')
btnAdvanced = KeyboardButton('Advanced corrector')

btnCheck = KeyboardButton('Check dictionary')

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnJaccard, btnML, btnAdvanced, btnCheck)


# -- Other -- 
otherMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnBack)