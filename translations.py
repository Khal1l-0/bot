translations = {
    'uz':{
        'Авторизация прошла успешно' : 'Avtorizatsiya muvaffaqiyatli boldi',
        'Добро пожаловать' : 'Xush kelibsiz',
        'Язык успешно изменен' : 'Til ozgardi',
        'Не понял' : 'Tushunmadim sizni',
        'Изменить язык' : 'Til ozgartirish',
        'Расчет металла' : 'Metallni hisoblash',
        'Каталог' : 'Katalog',
        'Наши товары:' : 'Bizning tovarlar:',
        # ----- #
        'Отцинковка рулон 1-2 сорт.' : 'pass1',
        'Черный лист': 'pass2',
        'Профиль гипсакартона': 'pass3',
        'Профиль ПВХ' : 'pass4', 
        'Профиль металический': 'pass5',
        'Вентиляция изготовления и установка': 'pass6',
        'Контейнеры' : 'pass7',
        'Арматуры': 'pass8',
        'Катанка' : 'pass9',
        # ----- #
        'Заявка' : 'Murojaat',
        'Заявки' : 'Murojaatlar',
        'Как вас зовут?' : 'Ismingiz nima?',
        'Какой вопрос вас интересует?': 'Sizni qanaqa savol qiziqtiradi?',
        'Принято, информация уже обрабатывается и в скором времени наш менеджер свяжется с вами' : 'Murojaatingiz qabul qilindi, tez orada menejerimiz siz bilan bog`lanadi',
        'Что найти?' : 'Nimani hisoblash kerak?',
        'Выберите язык' : 'Tilni tanlang',
        'Админ-панель' : 'Admin panel',
        'Вы вошли в админ-панель' : 'Siz admin-panelga kirdingiz',
        'Админ' : 'Admin',
        'Вес металла' : 'Metallni vaznini',
        'Длину металла' : 'Metallni uzunligi',
        'Напишите толщину в мм (0.4 - 3.0)' : 'Metallni qalinligi mm kiriting (0.4 - 3.0)',
        'Напишите длину в м (5, 10, 15)' : 'Metallni uzunligini m kiriting (5, 10, 15)',
        'Напишите вес в кг (5, 10, 15)' : 'Metallni og`irlini kg kiriting',
        'Ответ: ' : 'Javob: ',
        ' кг' : ' kg',
        ' м' : ' m',
        'Ошибка' : 'Xato',
        'Ваше число меньше нормы \nПопробуйте заново' : 'Kiritilgan raqam juda kichkina \n Qayta urinib ko`ring',
        'Ваше число больше нормы \nПопробуйте заново' : 'Kiritilgan raqam juda katta \n Qayta urinib ko`ring'
    }
}

def _(text, lang='ru'):
    if lang == 'ru':
        return text
    else:
        global translations
        try:
            return translations[lang][text]
        except:
            return text