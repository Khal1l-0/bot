from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from translations import _
from app import keyboards as kb
from app import database as db
from dotenv import load_dotenv
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)

async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен')

class GetInfoForWeigth(StatesGroup):
    thickness = State()
    length = State()

class GetInfoForLength(StatesGroup):
    thickness = State()
    weight = State()

class GetApplication(StatesGroup):
    name = State()
    applications = State()



    
    
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await register_authenticated_user(message)
    
async def register_authenticated_user(message: Message):
    chat_id = message.chat.id
    user = db.first_select_user(chat_id)
    print(user)
    if user:
        await bot.send_message(message.from_user.id, 'Авторизация прошла успешно')
        await show_main_menu(message)
    else:
        await message.answer('Для регистрации поделитесь контактом', reply_markup=kb.send_contact())

@dp.message_handler(content_types=['contact'])
async def fist_register_user(message: Message):
    chat_id = message.chat.id
    number = message.contact.phone_number   
    db.save_user_info(chat_id, number)
    await message.answer('Регистрация прошла успешно')
    await show_main_menu(message)

async def show_main_menu(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAEKjl1lMUFWTyAUD6oFU7aHYmbpdLSpGQAC2A8AAkjyYEsV-8TaeHRrmDAE')
    chat_id = message.from_user.id  
    lang = db.get_lang(chat_id)     
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(_('Админ', lang), reply_markup=kb.mainAdminMenu(lang)) 
    else:
        await bot.send_message(chat_id=message.from_user.id, text=f' <em>Metall Stroy</em> \n Мижозлар ишончи биз учун мухим!🏆 \n 🔹Оцинковка 1-2 сорт (рулон) \n 🔹Қора лист металл \n🔹Профиль гипсокартон учун \n🔹Профиль ПВХ \n🔹Вентиляция каналларини ишлаб чиқариш ва ўрнатиш \n 📞+998995217700 \n https://www.instagram.com/metallstroy_uz/ \n https://t.me/metallstroy_uz \n', parse_mode='HTML')
        await bot.send_message(message.from_user.id, _('Добро пожаловать', lang), reply_markup=kb.mainMenu(lang))
         


@dp.message_handler()
async def answer(message: types.Message):
    # await message.reply('Не понял')
    lang = db.get_lang(message.from_user.id)
    if message.text == _('Расчет металла', lang):
        await message.answer(_('Что найти?', lang), reply_markup=kb.calcMenu(lang))
    if message.text == _('Изменить язык', lang):
        await message.answer(_('Выберите язык', lang), reply_markup=kb.langMenu)
    if message.text == _('Каталог', lang):
        await message.answer(_('Наши товары:', lang), reply_markup=kb.catalog_list(lang))
    if message.text == _('Админ-панель', lang) and message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(_('Вы вошли в админ-панель', lang), reply_markup=kb.mainAdminMenu(lang))
    if message.text == _('Заявка', lang):
        await GetApplication.name.set()
        await message.answer(_('Как вас зовут?', lang))
    
    #Вес:
    if message.text == _('Вес металла', lang):
        await GetInfoForWeigth.thickness.set()
        await bot.send_message(chat_id=message.from_user.id, text=_('Напишите толщину в мм (0.4 - 3.0)', lang), reply_markup=kb.ReplyKeyboardRemove())
    #Длина
    if message.text == _('Длину металла', lang):
        await GetInfoForLength.thickness.set()
        await bot.send_message(chat_id=message.from_user.id, text=_('Напишите толщину в мм (0.4 - 3.0)', lang), reply_markup=kb.ReplyKeyboardRemove())
          
    # else:
    #     await message.reply(_('Не понял', lang))
    

#Вес
@dp.message_handler(state=GetInfoForWeigth.thickness)
async def weightByLengthItem1(message: types.Message, state: FSMContext):
    def is_number(item):
        try:
            float(item)
            return True
        except ValueError:
            return False
    lang = db.get_lang(message.from_user.id)
    if is_number(message.text):
        if float(message.text) > 0.4 and float(message.text) < 3.0:
            async with state.proxy() as data:
                data['thickness'] = message.text
            await message.answer(_('Напишите длину в м (5, 10, 15)', lang))
            await GetInfoForWeigth.next()
        if float(message.text) < 0.4:
            await state.finish()
            if message.from_user.id == int(os.getenv('ADMIN_ID')):
                await message.reply(_('Ваше число меньше нормы \nПопробуйте заново', lang), reply_markup=kb.mainAdminMenu(lang))
            else:
                await message.reply(_('Ваше число меньше нормы \nПопробуйте заново', lang), reply_markup=kb.mainMenu(lang))
        if float(message.text) > 3.0:
            await state.finish()
            if message.from_user.id == int(os.getenv('ADMIN_ID')):
                await message.reply(_('Ваше число больше нормы \nПопробуйте заново', lang), reply_markup=kb.mainAdminMenu(lang))
            else:
                await message.reply(_('Ваше число больше нормы \nПопробуйте заново', lang), reply_markup=kb.mainMenu(lang))
               
    if not is_number(message.text):
        await state.finish()
        if message.from_user.id == int(os.getenv('ADMIN_ID')):
            await message.reply(_('Ошибка', lang), reply_markup=kb.mainAdminMenu(lang))
        else:
            await message.reply(_('Ошибка', lang), reply_markup=kb.mainMenu(lang))
        
@dp.message_handler(state=GetInfoForWeigth.length)
async def weightByLengthItem2(message: types.Message, state: FSMContext):
    def is_number(item):
        try:
            float(item)
            return True
        except ValueError:
            return False
   
    lang = db.get_lang(message.from_user.id)
   
    if is_number(message.text):
        async with state.proxy() as data:
            data['length'] = message.text
            
        width = float(1.25)
        formula = float(7.85)
        async with state.proxy() as data:
            length = data['length']
            thickness = data['thickness']
            
        answer= width * formula * float(thickness) * float(length)
        await state.finish()
        await message.answer((_('Ответ: ', lang) + str(round(answer, 3)) + _(' кг', lang)), reply_markup=kb.mainMenu(lang))
    
    if not is_number(message.text):
        await state.finish()
        if message.from_user.id == int(os.getenv('ADMIN_ID')):
            await message.reply(_('Ошибка', lang), reply_markup=kb.mainAdminMenu(lang))
        else:
            await message.reply(_('Ошибка', lang), reply_markup=kb.mainMenu(lang))
        
#---------#

#Длина
@dp.message_handler(state=GetInfoForLength.thickness)
async def lengthByWeightItem1(message: types.Message, state: FSMContext):
    def is_number(item):
        try:
            float(item)
            return True
        except ValueError:
            return False
    lang = db.get_lang(message.from_user.id)
    if is_number(message.text):
        if float(message.text) > 0.4 and float(message.text) < 3.0:
            async with state.proxy() as data:
                data['thickness'] = message.text
            await message.answer(_('Напишите вес в кг (5, 10, 15)', lang))
            await GetInfoForLength.next()
        if float(message.text) < 0.4:
            await state.finish()
            if message.from_user.id == int(os.getenv('ADMIN_ID')):
                await message.reply(_('Ваше число меньше нормы \nПопробуйте заново', lang), reply_markup=kb.mainAdminMenu(lang))
            else:
                await message.reply(_('Ваше число меньше нормы \nПопробуйте заново', lang), reply_markup=kb.mainMenu(lang))
        if float(message.text) > 3.0:
            await state.finish()
            if message.from_user.id == int(os.getenv('ADMIN_ID')):
                await message.reply(_('Ваше число больше нормы \nПопробуйте заново', lang), reply_markup=kb.mainAdminMenu(lang))
            else:
                await message.reply(_('Ваше число больше нормы \nПопробуйте заново', lang), reply_markup=kb.mainMenu(lang))
               
    if not is_number(message.text):
        await state.finish()
        if message.from_user.id == int(os.getenv('ADMIN_ID')):
            await message.reply(_('Ошибка', lang), reply_markup=kb.mainAdminMenu(lang))
        else:
            await message.reply(_('Ошибка', lang), reply_markup=kb.mainMenu(lang))
     
@dp.message_handler(state=GetInfoForLength.weight)
async def lengthByWeightItem2(message: types.Message, state: FSMContext):
    def is_number(item):
        try:
            float(item)
            return True
        except ValueError:
            return False
    lang = db.get_lang(message.from_user.id)
    if is_number(message.text):
        async with state.proxy() as data:
            data['weight'] = message.text
        width = float(1.25)
        formula = float(7.85)
        async with state.proxy() as data:
            thickness = data['thickness']
            weight = data['weight']

        answer = float(weight) / (width * formula * float(thickness))
        await state.finish()
        await message.answer((_('Ответ: ', lang) + str(round(answer, 3)) + _(' м', lang)), reply_markup=kb.mainMenu(lang))
    
    if not is_number(message.text):
        await state.finish()
        if message.from_user.id == int(os.getenv('ADMIN_ID')):
            await message.reply(_('Ошибка', lang), reply_markup=kb.mainAdminMenu(lang))
        else:
            await message.reply(_('Ошибка', lang), reply_markup=kb.mainMenu(lang))
   
#---------#      

#Заявка
    
@dp.message_handler(state=GetApplication.name)
async def GetAppName(message: types.Message, state: FSMContext):
    lang = db.get_lang(message.from_user.id)
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(_('Какой вопрос вас интересует?',lang))
    await GetApplication.next()

@dp.message_handler(state=GetApplication.applications)
async def GetApp(message: types.Message, state: FSMContext):
    lang = db.get_lang(message.from_user.id)
    async with state.proxy() as data:
        data['applications'] = message.text
    await db.add_application(state)
    await state.finish()
    await message.answer(_('Принято, информация уже обрабатывается и в скором времени наш менеджер свяжется с вами',lang), reply_markup=kb.mainMenu(lang)) 

    
#---------# 
@dp.callback_query_handler(text_contains = "lang_")
async def setLanguage(callback: types.CallbackQuery):
    lang = callback.data[5:]
    db.change_lang(lang)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    lang2 = db.get_lang(callback.from_user.id)
    if callback.from_user.id == int(os.getenv('ADMIN_ID')):
        await bot.send_message(callback.from_user.id, _('Язык успешно изменен', lang), reply_markup=kb.mainAdminMenu(lang2))
    else:
        await bot.send_message(callback.from_user.id, _('Язык успешно изменен', lang), reply_markup=kb.mainMenu(lang2))

@dp.callback_query_handler()
async def callback_query_keyboards(callback_query: types.CallbackQuery):
    lang = db.get_lang(callback_query.from_user.id)
    media = types.MediaGroup()
    if callback_query.data == 'catalog-1':
        price = '100'
        
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        media.attach_photo(types.InputFile('media/otsinkovka_rulon.jpg'), _('Отцинковка рулон 1-2 сорт.', lang) + _('\nЦена', lang) + price + '$')
        await bot.send_media_group(callback_query.from_user.id, media=media)
    
    elif callback_query.data == 'catalog-2':
        price = '100'
        
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        media.attach_photo(types.InputFile('media/ventilasiya.jpg'), _('Вентиляция изготовления и установка', lang) + _('\nЦена', lang) + price + '$')
        await bot.send_media_group(callback_query.from_user.id, media=media)
        
    elif callback_query.data == 'catalog-3': 
        price = '100'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        media.attach_photo(types.InputFile('media/cherniy_list.jpg'), _('Черный лист', lang) + _('\nЦена', lang) + price + '$')
        await bot.send_media_group(callback_query.from_user.id, media=media)
        
    elif callback_query.data == 'catalog-4':
        price = '100'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        media.attach_photo(types.InputFile('media/pvx.jpg'), _('Метал профиль для ПВХ', lang) + _('\nЦена', lang) + price + '$')
        await bot.send_media_group(callback_query.from_user.id, media=media)
    
    elif callback_query.data == 'catalog-5':
        price = '100'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        media.attach_photo(types.InputFile('media/metal.jpg'), _('Профиль металический', lang) + _('\nЦена', lang) + price + '$')
        await bot.send_media_group(callback_query.from_user.id, media=media)
    
    elif callback_query.data == 'catalog-6':
        price = '100'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        media.attach_photo(types.InputFile('media/konteyner.jpg'), _('Контейнеры любого размера', lang) + _('\nЦена', lang) + price + '$')
        await bot.send_media_group(callback_query.from_user.id, media=media)
    
    elif callback_query.data == 'catalog-7':
        price = '100'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        media.attach_photo(types.InputFile('media/armatura.jpg'), _('Арматуры в ассортименте', lang) + _('\nЦена', lang) + price + '$')
        await bot.send_media_group(callback_query.from_user.id, media=media)
    
    elif callback_query.data == 'catalog-8':
        price = '100'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        media.attach_photo(types.InputFile('media/kanatka.jpg'), _('Катанка', lang) + _('\nЦена', lang) + price + '$')
        await bot.send_media_group(callback_query.from_user.id, media=media)
    
    elif callback_query.data == 'catalog-9':
        price = '100'
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        # media.attach_photo(types.InputFile('media/gipsokarton-1.jpg'))
        media.attach_photo(types.InputFile('media/gipsokarton-1.jpg'), _('Профиль гипсакартона', lang) + _('\nЦена', lang) + price + '$')
        await bot.send_media_group(callback_query.from_user.id, media=media)
    

    
@dp.message_handler(commands=['ru'])
async def cmd_ru(message: types.Message):
    await register_authenticated_user(message)
       
    
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)