import json, copy, os, wget, requests, urllib.error
from random import randint, choice as r_choice
from requests.exceptions import ConnectionError

def ConnectionErrorMessage(action_info):
        print(f'\n! Возникла сетевая ошибка и программе не удалось {action_info}.')
        print('! Убедитесь, что у Вас включён интернет и соединение стабильно.')
        print('! Программа работает в автономном режиме.')
        input('\nНажмите Enter чтобы продолжить...\n')

def download_db():
    file_exists = False
    file_name = 'db.json'
    
    if os.path.exists(file_name):
        print('\nСоздание резервной копии вашей Базы данных...')
        file_exists = True
        try:
            os.rename(file_name, file_name+'.bckp')
        except FileExistsError:
            print('Обнаружена существующая резервная копиия. ВНИМАНИЕ, продолжение операции удалит её.')
            if input('Продолжить? [Y/n]: ') in ['Y', 'y', 'Д', 'д']:
                os.replace(file_name, file_name+'.bckp')
            else:
                return
        print('ОК!\n')
    
    try:
        wget.download('https://raw.githubusercontent.com/Neireck/LWS-Testing/main/db.json', file_name)
    except urllib.error.URLError:
        ConnectionErrorMessage('загрузить Базу данных, но Вы можете заполнить её словами самостоятельно')
        return False

    print('\n\nБаза данных обновлена!\n')
    if file_exists:
        print(f'Если вы хотите восстановить резервную копию, то в папке с этой программой найдите файл "{file_name}" и удалите его,')
        print(f'а файл "{file_name+".bckp"}" переименуйте на "{file_name}".')
    
    return True

def check_update_db():
    try:
        remoute_db = requests.get('https://raw.githubusercontent.com/Neireck/LWS-Testing/main/db.json').json()
    except ConnectionError:
        ConnectionErrorMessage('проверить наличие обновлений Базы данных')
        return

    if db != remoute_db:
        print('\n! Обнаружена новая версия Базы данных.\n! Если вы не вносили свои слова в программу, то выберите пункт 998.')
    
    del remoute_db

def create_db(data_array, no_download = False):
    if no_download: answer = 'N'
    else: answer = input("Хотите загрузить Базу данных от разработчика? [Y/n]: ")

    if answer in ['Y', 'y', 'Д', 'д']:
        if download_db() == False:
            create_db(data_array, True)
    else:
        with open('db.json', 'w+', encoding='utf8') as j:
            json.dump(data_array, j, ensure_ascii=False)

def counter_db(db, word_type = 'All'):
    if word_type == 'All':
        return sum([len(db[key]) for key in db])
    else:
        return len(db[word_type])

def get_db(file_name = 'db.json'):
    if os.path.exists(file_name): # Check file DB
        with open(file_name, 'r', encoding='utf8') as j:
            db = json.load(j)
        if counter_db(db) == 0: # Check DB
            global mode
            print(f'\n!!! ВНИМАНИЕ: В базе данных нет слов. Пожалуйста, заполните БД как следует.')
            mode = 999
        return db
    else:
        print('База данных пуста или отсутствует.')
        create_db({'Substantive':[], 'Verben':[], 'Adjektive':[], 'Fragen':[], 'Anderen':[]})
        return get_db()

def get_word_data(db, word_type = 'Random'):
    data = {}
    data['type']   =   r_choice([key for key in db]) if word_type == 'Random' else word_type
    data['id']     =   randint(0, len(db[data['type']])-1)
    return data

def set_user_mode():
    global mode
    global statistic
    global answer
    check_update_db()
    print('''\nРежимы тестирования: 
        1) Deutsch -> Русский 
        2) Русский -> Deutsch
        3) Артикли немецких слов
        998) Обновить базу данных по сети (Ваши добавленные слова исчезнут!)
        999) Добавить слова в базу данных
        0) Выход
        ''')
    try: mode = int(input('Ваш выбор: '))
    except ValueError: mode = None
    statistic = [0, 0]
    answer = ''

def connect_db():
    global db
    global static_len_db
    global dynamic_len_db
    global s_len_substantive
    global d_len_substantive
    db = get_db()
    static_len_db = counter_db(db)
    dynamic_len_db = copy.copy(static_len_db)
    s_len_substantive = counter_db(db, 'Substantive')
    d_len_substantive = copy.copy(s_len_substantive)
connect_db()

# Mode
if 'mode' not in locals():
    set_user_mode()

# Begin test
j = 1
while j == 1:
    if mode == 1:           # Deutsch -> Русский
        if dynamic_len_db == 0 or answer == '!':
            print(f"\nПравильных ответов: {statistic[0]}\nОшибок: {statistic[1]}\nВсего попыток: {statistic[0]+statistic[1]}\n")
            db = get_db()
            dynamic_len_db = copy.copy(static_len_db)
            answer = ''
            if mode != 999 and input('Тест окончен. Хотите повторить? [Y/n]: ') in ['Y', 'y']:
                statistic = [0, 0]
                continue
            else:
                set_user_mode()
                continue

        try:
            word_data = get_word_data(db)
            word = db[word_data['type']][word_data['id']]
        except: # If no words
            continue

        try:                w_artikel = word["artikel"]
        except KeyError:    w_artikel = ''

        print(f'\n{statistic[0]+statistic[1]+1}/{static_len_db} ({word_data["type"]})\nВаше слово: {w_artikel} {word["word"]}')
        answer = input('Перевод на русский: ')
        
        if word["translate_ru"] == answer: 
            print("\nПравильно!")
            statistic[0] += 1
        elif answer == '!': continue
        else: 
            print('\nНе правильно!\nПравильный ответ:', word["translate_ru"])
            statistic[1] += 1
        
        del db[word_data['type']][word_data['id']]
        dynamic_len_db -= 1

    elif mode == 2:         # Русский -> Deutsch
        if dynamic_len_db == 0 or answer == '!':
            print(f"\nПравильных ответов: {statistic[0]}\nОшибок: {statistic[1]}\nВсего попыток: {statistic[0]+statistic[1]}\n")
            db = get_db()
            dynamic_len_db = copy.copy(static_len_db)
            answer = ''
            if input('Тест окончен. Хотите повторить? [Y/n]: ') in ['Y', 'y']:
                statistic = [0, 0]
                continue
            else:
                set_user_mode()
                continue

        try:    
            word_data = get_word_data(db)
            word = db[word_data['type']][word_data['id']]
        except: 
            continue

        print(f'\n{statistic[0]+statistic[1]+1}/{static_len_db}\nВаше слово: {word["translate_ru"]}')
        answer = input('Перевод на немецкий: ')

        if word["word"] == answer: 
            print("\nПравильно!")
            statistic[0] += 1
        elif answer == '!': continue
        else: 
            print('\nНе правильно!\nПравильный ответ:', word["word"])
            statistic[1] += 1
        
        del db[word_data['type']][word_data['id']]
        dynamic_len_db -= 1
        
    elif mode == 3:         # Артикли немецких слов
        if d_len_substantive == 0 or answer == '!':
            print(f"\nПравильных ответов: {statistic[0]}\nОшибок: {statistic[1]}\nВсего попыток: {statistic[0]+statistic[1]}\n")
            db = get_db()
            answer = ''
            d_len_substantive = copy.copy(s_len_substantive)
            if input('Тест окончен. Хотите повторить? [Y/n]: ') in ['Y', 'y']:
                statistic = [0, 0]
                continue
            else:
                set_user_mode()
                continue
        
        try:    
            word_data = get_word_data(db, 'Substantive')
            word = db[word_data['type']][word_data['id']]
        except: 
            continue

        print(f'\n{statistic[0]+statistic[1]+1}/{s_len_substantive}\nВаше слово: {word["word"]}')
        answer = input('Артикль: ')
        
        if word["artikel"] == answer: 
            print("\nПравильно!")
            statistic[0] += 1
        elif answer == '!': continue
        else: 
            print('\nНе правильно!\nПравильный ответ:', word["artikel"])
            statistic[1] += 1

        del db[word_data['type']][word_data['id']]
        d_len_substantive -= 1

    elif mode == 998:
        download_db()
        connect_db()
        set_user_mode()
    elif mode == 999:       # Заполнение БД
        print('\n!!! ВЫ В РЕЖИМЕ ДОБАВЛЕНИЕ СЛОВ В БАЗУ ДАННЫХ')

        w = 1
        while w == 1:
            print('\nВыберите тип слова из списка ниже:')
            for k, v in enumerate([key for key in db]):
                print(f'{k+1}) {v}')
            print('0) Назад')
            try: word_type = int(input('\nВаш выбор: '))
            except ValueError: word_type = None
            #print('')

            if word_type == 1:
                name_type = 'Substantive'
                print(f'\nДобавление слова типа "{name_type}"')

                db[name_type].append({
                    "artikel":      input('Артикль: '),
                    "word":         input('Слово DE: '),
                    "translate_ru": input('Перевод RU: ')
                })
            elif word_type == 2:
                name_type = 'Verben'
                print(f'\nДобавление слова типа "{name_type}"')

                db[name_type].append({
                    "word":                 input('Слово DE: '),
                    "translate_ru":         input('Перевод RU: '),
                    "perfekt form":         input('Perfekt form: '),
                    "perfekt begin form" :  input('Perfekt begin form (ist/hat): ')
                })
            elif word_type == 3:
                name_type = 'Adjektive'
                print(f'\nДобавление слова типа "{name_type}"')

                db[name_type].append({
                    "word":         input('Слово DE: '),
                    "translate_ru": input('Перевод RU: ')
                })
            elif word_type == 4:
                name_type = 'Fragen'
                print(f'\nДобавление слова типа "{name_type}"')

                db[name_type].append({
                    "word":         input('Слово DE: '),
                    "translate_ru": input('Перевод RU: ')
                })
            elif word_type == 5:
                name_type = 'Anderen'
                print(f'\nДобавление слова типа "{name_type}"')

                db[name_type].append({
                    "word":         input('Слово DE: '),
                    "translate_ru": input('Перевод RU: ')
                })
            elif word_type == 0:
                break
            else:
                print('\nОшибка ввода. Повторите ещё раз!')
                continue
            
            create_db(db, True)
            connect_db()

            confirm = input('\nНажмите Enter чтобы продолжить или введите что либо, чтобы прервать... ')
            print(f'\nПоследнее добавление: {db[name_type][-1]}\n')
            if confirm != '': w = 0
        
        set_user_mode()

    elif mode == 0:         # Выход
        j = 0
        print('\nTschüss!\n')
    
    else:                   # Исключение неверного ответа
        print("\nТакого режима у нас нет! Попробуйте ещё раз...")
        set_user_mode()
