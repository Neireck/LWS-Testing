import json
from random import randint, choice as r_choice

# Connect database
try:
    with open('db.json', 'r', encoding='utf8') as j:
        db = json.load(j)
except:
    with open('db.json', 'w+', encoding='utf8') as j:
        json.dump({'Substantive':[], 'Verben':[], 'Adjektive':[], 'Fragen':[], 'Anderen':[]}, j, ensure_ascii=False)
    with open('db.json', 'r', encoding='utf8') as j:
        db = json.load(j)
    mode = 999
        
for key in db:
    if len(db[key]) == 0:
        print(f'!!! ВНИМАНИЕ: В базе данных нет слов типа "{key}". Пожалуйста, заполните БД как следует.')
        mode = 999

# Mode
if 'mode' not in locals():
    print('''Режимы тестирования: 
        1) Deutsch -> Русский 
        2) Русский -> Deutsch
        3) Артикли немецких слов
        999) Добавить слова в базу данных
        ''')
    mode = int(input('Ваш выбор: '))
    statistic = [0, 0]
    last_world = ''

# Begin test
j = 1
while j == 1:
    #word = db[randint(1,8)]
    if mode == 1:
        # Deutsch -> Русский
        
        word_type = r_choice([key for key in db])
        word = r_choice(db[word_type])
        if last_world == word: continue
        
        try:
            w_artikel = word["artikel"]
        except KeyError:
            w_artikel = ''

        print(f'\n({word_type})\nВаше слово: {w_artikel} {word["word"]}')
        answer = input('Перевод на русский: ')
        
        if word["translate_ru"] == answer: 
            print("\nПравильно!")
            statistic[0] += 1
        elif answer == '!': j = 0
        else: 
            print('\nНе правильно!\nПравильный ответ:', word["translate_ru"])
            statistic[1] += 1
        last_world = word
    elif mode == 2:
        # Русский -> Deutsch

        word_type = r_choice([key for key in db])
        word = r_choice(db[word_type])
        if last_world == word: continue

        print(f'\nВаше слово: {word["translate_ru"]}')
        answer = input('Перевод на немецкий: ')

        if word["word"] == answer: 
            print("\nПравильно!")
            statistic[0] += 1
        elif answer == '!': j = 0
        else: 
            print('\nНе правильно!\nПравильный ответ:', word["word"])
            statistic[1] += 1
        last_world = word
    elif mode == 3:
        # Артикли немецких слов

        word_type = r_choice([key for key in db])
        word = r_choice(db[word_type])
        if last_world == word: continue

        print(f'\nВаше слово: {word["word"]}')
        answer = input('Артикль: ')
        
        if word["artikel"] == answer: 
            print("\nПравильно!")
            statistic[0] += 1
        elif answer == '!': j = 0
        else: 
            print('\nНе правильно!\nПравильный ответ:', word["artikel"])
            statistic[1] += 1
        last_world = word
    elif mode == 999:
        # Заполнение БД
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
            
            with open("db.json", "w", encoding='utf8') as wdb:
                json.dump(db, wdb, ensure_ascii=False)

            confirm = input('\nНажмите Enter чтобы продолжить или введите что либо, чтобы прервать... ')
            print(f'\nПоследнее добавление: {db[name_type][-1]}\n')
            if confirm != '': w = 0
            
        j = 0

if mode != 999: print(f"\nПравильных ответов: {statistic[0]}\nОшибок: {statistic[1]}\nВсего попыток: {statistic[0]+statistic[1]}\n")