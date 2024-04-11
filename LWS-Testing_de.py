import json, copy, os, wget, requests, urllib.error
from random import randint, choice as r_choice
from requests.exceptions import ConnectionError

def ConnectionErrorMessage(action_info):
        print(f'\n! Ein Netzwerkfehler ist aufgetreten und das Programm {action_info}.')
        print('! Stellen Sie sicher, dass Ihr Internet eingeschaltet und die Verbindung stabil ist.')
        print('! Das Programm funktioniert offline.')
        input('\nDrücken Sie die Eingabetaste, um fortzufahren...\n')

def download_db():
    file_exists = False
    file_name = 'db.json'
    
    if os.path.exists(file_name):
        print('\nSichern Sie Ihre Datenbank...')
        file_exists = True
        try:
            os.rename(file_name, file_name+'.bckp')
        except FileExistsError:
            print('Es wurde ein vorhandenes Backup erkannt. ACHTUNG: Wenn Sie den Vorgang fortsetzen, wird es entfernt.')
            if input('Weitermachen? [Y/n]: ') in ['Y', 'y', 'Д', 'д', 'J', 'j']:
                os.replace(file_name, file_name+'.bckp')
            else:
                return
        print('ОК!\n')
    
    try:
        wget.download('https://raw.githubusercontent.com/Neireck/LWS-Testing/main/db.json', file_name)
    except urllib.error.URLError:
        ConnectionErrorMessage('die Datenbank nicht laden. Sie können sie jedoch selbst mit Wörtern füllen')
        return False

    print('\n\nDatenbank aktualisiert!\n')
    if file_exists:
        print(f'Wenn Sie ein Backup wiederherstellen möchten, suchen Sie im Ordner mit diesem Programm die Datei „{file_name}“ und löschen Sie sie')
        print(f'und benennen Sie die Datei „{file_name+".bckp"}“ in „{file_name}“ um.')
    
    return True

def check_update_db():
    try:
        remoute_db = requests.get('https://raw.githubusercontent.com/Neireck/LWS-Testing/main/db.json').json()
    except ConnectionError:
        ConnectionErrorMessage('konnte nicht nach Datenbankaktualisierungen suchen')
        return

    if db != remoute_db:
        print('\n! Eine neue Version der Datenbank wurde erkannt.\n! Wenn Sie Ihre Wörter nicht in das Programm eingegeben haben, wählen Sie Punkt 998.')
    
    del remoute_db

def create_db(data_array, no_download = False):
    if no_download: answer = 'N'
    else: answer = input("Möchten Sie die Datenbank vom Entwickler herunterladen? [Y/n]: ")

    if answer in ['Y', 'y', 'Д', 'д', 'J', 'j']:
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
            print(f'\n!!! ACHTUNG: Die Datenbank enthält keine Wörter. Bitte füllen Sie die Datenbank ordnungsgemäß aus.')
            mode = 999
        return db
    else:
        print('Die Datenbank ist leer oder fehlt.')
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
    print('''\nTestmodi: 
        1) Deutsch -> Übersetzung 
        2) Übersetzung -> Deutsch
        3) Artikel
        998) Datenbank online aktualisieren (Ihre hinzugefügten Wörter verschwinden!)
        999) Wörter zur Datenbank hinzufügen
        0) Ausgang
        ''')
    try: mode = int(input('Ihre Wahl: '))
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
    if mode == 1:           # Deutsch -> Übersetzung
        if dynamic_len_db == 0 or answer == '!':
            print(f"\nRichtige Antworten: {statistic[0]}\nFehler: {statistic[1]}\nGesamtversuche: {statistic[0]+statistic[1]}\n")
            db = get_db()
            dynamic_len_db = copy.copy(static_len_db)
            answer = ''
            if mode != 999 and input('Der Test ist beendet. Möchten Sie es wiederholen? [Y/n]: ') in ['Y', 'y', 'Д', 'д', 'J', 'j']:
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

        print(f'\n{statistic[0]+statistic[1]+1}/{static_len_db} ({word_data["type"]})\nIhre Wort: {w_artikel} {word["word"]}')
        answer = input('Übersetzung: ')
        
        if word["translate"] == answer: 
            print("\nRechts!")
            statistic[0] += 1
        elif answer == '!': continue
        else: 
            print('\nFalsch!\nRichtige Antwort:', word["translate"])
            statistic[1] += 1
        
        del db[word_data['type']][word_data['id']]
        dynamic_len_db -= 1

    elif mode == 2:         # Русский -> Deutsch
        if dynamic_len_db == 0 or answer == '!':
            print(f"\nRichtige Antworten: {statistic[0]}\nFehler: {statistic[1]}\nGesamtversuche: {statistic[0]+statistic[1]}\n")
            db = get_db()
            dynamic_len_db = copy.copy(static_len_db)
            answer = ''
            if mode != 999 and input('Der Test ist beendet. Möchten Sie es wiederholen? [Y/n]: ') in ['Y', 'y', 'Д', 'д', 'J', 'j']:
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

        print(f'\n{statistic[0]+statistic[1]+1}/{static_len_db}\nIhre Wort: {word["translate"]}')
        answer = input('Übersetzung ins Deutsche: ')

        if word["word"] == answer: 
            print("\nRechts!")
            statistic[0] += 1
        elif answer == '!': continue
        else: 
            print('\nFalsch!\nRichtige Antwort:', word["word"])
            statistic[1] += 1
        
        del db[word_data['type']][word_data['id']]
        dynamic_len_db -= 1
        
    elif mode == 3:         # Артикли немецких слов
        if d_len_substantive == 0 or answer == '!':
            print(f"\nRichtige Antworten: {statistic[0]}\nFehler: {statistic[1]}\nGesamtversuche: {statistic[0]+statistic[1]}\n")
            db = get_db()
            answer = ''
            d_len_substantive = copy.copy(s_len_substantive)
            if mode != 999 and input('Der Test ist beendet. Möchten Sie es wiederholen? [Y/n]: ') in ['Y', 'y', 'Д', 'д', 'J', 'j']:
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

        print(f'\n{statistic[0]+statistic[1]+1}/{s_len_substantive}\nIhre Wort: {word["word"]}')
        answer = input('Artikel: ')
        
        if word["artikel"] == answer: 
            print("\nRechts!")
            statistic[0] += 1
        elif answer == '!': continue
        else: 
            print('\nFalsch!\nRichtige Antwort:', word["artikel"])
            statistic[1] += 1

        del db[word_data['type']][word_data['id']]
        d_len_substantive -= 1

    elif mode == 998:
        download_db()
        connect_db()
        set_user_mode()
    elif mode == 999:       # Заполнение БД
        print('\n!!! SIE SIND DABEI, DEM DATENBANKMODUS WÖRTER HINZUZUFÜGEN')

        w = 1
        while w == 1:
            print('\nWählen Sie einen Worttyp aus der Liste unten aus:')
            for k, v in enumerate([key for key in db]):
                print(f'{k+1}) {v}')
            print('0) Zurück')
            try: word_type = int(input('\nIhre Wahl: '))
            except ValueError: word_type = None
            #print('')

            if word_type == 1:
                name_type = 'Substantive'
                print(f'\nEin Wort hinzufügen. Typ ist "{name_type}"')

                db[name_type].append({
                    "artikel":      input('Artikel: '),
                    "word":         input('Wort DE: '),
                    "translate": input('Übersetzung: ')
                })
            elif word_type == 2:
                name_type = 'Verben'
                print(f'\nДобавление слова типа "{name_type}"')

                db[name_type].append({
                    "word":                 input('Wort DE: '),
                    "translate":         input('Übersetzung: '),
                    "perfekt form":         input('Perfekt form: '),
                    "perfekt begin form" :  input('Perfekt begin form (ist/hat): ')
                })
            elif word_type == 3:
                name_type = 'Adjektive'
                print(f'\nДобавление слова типа "{name_type}"')

                db[name_type].append({
                    "word":         input('Wort DE: '),
                    "translate": input('Übersetzung: ')
                })
            elif word_type == 4:
                name_type = 'Fragen'
                print(f'\nДобавление слова типа "{name_type}"')

                db[name_type].append({
                    "word":         input('Wort DE: '),
                    "translate": input('Übersetzung: ')
                })
            elif word_type == 5:
                name_type = 'Anderen'
                print(f'\nДобавление слова типа "{name_type}"')

                db[name_type].append({
                    "word":         input('Wort DE: '),
                    "translate": input('Übersetzung: ')
                })
            elif word_type == 0:
                break
            else:
                print('\nEingabe Fehler. Noch einmal wiederholen!')
                continue
            
            create_db(db, True)
            connect_db()

            confirm = input('\nDrücken Sie die Eingabetaste, um fortzufahren, oder geben Sie etwas ein, um den Vorgang abzubrechen... ')
            print(f'\nZuletzt hinzugefügt: {db[name_type][-1]}\n')
            if confirm != '': w = 0
        
        set_user_mode()

    elif mode == 0:         # Выход
        j = 0
        print('\nTschüss!\n')
    
    else:                   # Исключение неверного ответа
        print("\nWir haben kein solches Regime! Versuchen Sie es nochmal...")
        set_user_mode()
