import json, copy
from random import randint, choice as r_choice

def create_db(data_array):
    with open('db.json', 'w+', encoding='utf8') as j:
        json.dump(data_array, j, ensure_ascii=False)

def get_db():
    with open('db.json', 'r', encoding='utf8') as j:
        return json.load(j)

def check_db_arr(data, word_type = 'All'):
    count = 0
    if word_type == 'All':
        for k in data:
            count += len(data[k])
    else:
        count = len(data[word_type])
    
    if count != 0: return False
    else: return True

def get_word_data(db, word_type = 'Random'):
    data = {}
    data['type']   =   r_choice([key for key in db]) if word_type == 'Random' else word_type
    data['id']     =   randint(0, len(db[data['type']])-1)
    return data

def set_user_mode():
    global mode
    global statistic
    print('''\nРежимы тестирования: 
        1) Deutsch -> Русский 
        2) Русский -> Deutsch
        3) Артикли немецких слов
        999) Добавить слова в базу данных
        0) Выход
        ''')
    try: mode = int(input('Ваш выбор: '))
    except ValueError: mode = None
    statistic = [0, 0]

# Connect database
try:
    db = get_db()
except:
    create_db({'Substantive':[], 'Verben':[], 'Adjektive':[], 'Fragen':[], 'Anderen':[]})
    db = get_db()
    mode = 999

# Сheck database
for key in db:
    if len(db[key]) == 0:
        print(f'!!! ВНИМАНИЕ: В базе данных нет слов типа "{key}". Пожалуйста, заполните БД как следует.')
        mode = 999

# Mode
if 'mode' not in locals():
    set_user_mode()

# Begin test
j = 1
while j == 1:
    if mode == 1:           # Deutsch -> Русский
        if check_db_arr(db) == True:
            print(f"\nПравильных ответов: {statistic[0]}\nОшибок: {statistic[1]}\nВсего попыток: {statistic[0]+statistic[1]}\n")
            db = get_db()
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

        try:                w_artikel = word["artikel"]
        except KeyError:    w_artikel = ''

        print(f'\n({word_data["type"]})\nВаше слово: {w_artikel} {word["word"]}')
        answer = input('Перевод на русский: ')
        
        if word["translate_ru"] == answer: 
            print("\nПравильно!")
            statistic[0] += 1
        elif answer == '!': j = 0
        else: 
            print('\nНе правильно!\nПравильный ответ:', word["translate_ru"])
            statistic[1] += 1
        
        del db[word_data['type']][word_data['id']]

    elif mode == 2:         # Русский -> Deutsch
        if check_db_arr(db) == True:
            print(f"\nПравильных ответов: {statistic[0]}\nОшибок: {statistic[1]}\nВсего попыток: {statistic[0]+statistic[1]}\n")
            db = get_db()
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

        print(f'\nВаше слово: {word["translate_ru"]}')
        answer = input('Перевод на немецкий: ')

        if word["word"] == answer: 
            print("\nПравильно!")
            statistic[0] += 1
        elif answer == '!': j = 0
        else: 
            print('\nНе правильно!\nПравильный ответ:', word["word"])
            statistic[1] += 1
        
        del db[word_data['type']][word_data['id']]
        
    elif mode == 3:         # Артикли немецких слов
        if check_db_arr(db, 'Substantive') == True:
            print(f"\nПравильных ответов: {statistic[0]}\nОшибок: {statistic[1]}\nВсего попыток: {statistic[0]+statistic[1]}\n")
            db = get_db()
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

        print(f'\nВаше слово: {word["word"]}')
        answer = input('Артикль: ')
        
        if word["artikel"] == answer: 
            print("\nПравильно!")
            statistic[0] += 1
        elif answer == '!': j = 0
        else: 
            print('\nНе правильно!\nПравильный ответ:', word["artikel"])
            statistic[1] += 1

        del db[word_data['type']][word_data['id']]

    elif mode == 999:       # Заполнение БД
        print('\n!!! ВЫ В РЕЖИМЕ ДОБАВЛЕНИЕ СЛОВ В БАЗУ ДАННЫХ')

        w = 1
        while w == 1:
            print('\nВыберите тип слова из списка ниже:')
            for k, v in enumerate([key for key in db]):
                print(f'{k+1}) {v}')
            word_type = int(input('\nВаш выбор: '))
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
            
            create_db(db)

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
