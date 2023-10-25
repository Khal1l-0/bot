from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from translations import _

# main = ReplyKeyboardMarkup(resize_keyboard=True)
# main.add('/start').add('Изменить язык').add('Расчет металла').add('Каталог').add('Заявка')
# main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
# main_admin.add('Изменить язык').add('Расчет металла').add('Заявки').add('Список юзеров')


def mainMenu(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    changeLang = KeyboardButton(_('Изменить язык', lang))
    calcMetal = KeyboardButton(_('Расчет металла', lang))
    catalog = KeyboardButton(_('Каталог', lang))
    applic = KeyboardButton(_('Заявка', lang))
    # ----- #
    keyboard.add(changeLang, calcMetal, catalog, applic)
    return keyboard

def mainAdminMenu(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    changeLang = KeyboardButton(_('Изменить язык', lang))
    calcMetal = KeyboardButton(_('Расчет металла', lang))
    catalog = KeyboardButton(_('Каталог', lang))
    applic = KeyboardButton(_('Заявки', lang))
    # ----- #
    keyboard.add(changeLang, calcMetal, catalog, applic)
    return keyboard

def calcMenu(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # ----- #
    weight = KeyboardButton(_('Длину металла', lang))
    lenght = KeyboardButton(_('Вес металла', lang))
    # ----- #
    keyboard.add(weight, lenght)
    return keyboard


def catalog_list(lang):
    keyboard = InlineKeyboardMarkup()
    # ----- #
    catalog_1 = InlineKeyboardButton(text=_('Отцинковка рулон 1-2 сорт.', lang),callback_data='catalog-1')
    catalog_2 = InlineKeyboardButton(text=_('Вентиляция изготовления и установка', lang),callback_data='catalog-2')
    catalog_3 = InlineKeyboardButton(text=_('Черный лист', lang),callback_data='catalog-3')
    catalog_4 = InlineKeyboardButton(text=_('Профиль ПВХ', lang),callback_data='catalog-4') 
    catalog_5 = InlineKeyboardButton(text=_('Профиль металический', lang),callback_data='catalog-5')
    catalog_6 = InlineKeyboardButton(text=_('Контейнеры', lang),callback_data='catalog-6')
    catalog_7 = InlineKeyboardButton(text=_('Арматуры', lang),callback_data='catalog-7')
    catalog_8 = InlineKeyboardButton(text=_('Катанка', lang),callback_data='catalog-8')
    catalog_9 = InlineKeyboardButton(text=_('Профиль гипсакартона', lang),callback_data='catalog-9')
    # ----- #
    keyboard.add(catalog_1)
    keyboard.add(catalog_2)
    keyboard.row(catalog_3, catalog_4,)
    keyboard.add(catalog_5)
    keyboard.row(catalog_6,catalog_7, catalog_8,)
    keyboard.add(catalog_9)
    return keyboard
  
    
# def langMenu(lang):
#     keyboard = InlineKeyboardMarkup(row_width=1)
#     langRU = InlineKeyboardButton(text='Ru', callback_data='lang_ru')
#     langUz = InlineKeyboardButton(text='Uz', callback_data='lang_uz')
#     # ----- #
#     langMenu.insert(langRU)
#     langMenu.insert(langUz)
#     return keyboard
    
    
langMenu = InlineKeyboardMarkup(row_width=1)
# langMenu.add(InlineKeyboardButton(text='UZ', callback_data='lang_uz'))
langRU = InlineKeyboardButton(text='Ru', callback_data='lang_ru')
langUz = InlineKeyboardButton(text='Uz', callback_data='lang_uz')
langMenu.insert(langRU)
langMenu.insert(langUz)





def send_contact():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='Поделится контактом', request_contact=True)]
    ], resize_keyboard=True)