"""
Я вирішив трохи відійти від умови "домашки" і зробити CLI-бота більш атмосферним))))
Бот створений у вигляді персонально джина, який виконує бажання (додає та модифікує телефонну книгу).
Також додав функціонал збереження та зчитування інфи у .txt-файл, бо
    1) при тестуванні лінь було весь час вводити імʼя та телефони,
    2) жаль, коли вся ця робота пропадала в кінці сессії.

--- ГЛОСАРІЙ ---
- The Book of The Damned (Книга Проклятих) - словник з контактами. На початку він пустий, але в кінці першої сессії
            можна вибрати, чи зберегти дані в однойменний .txt файл. На початку наступної сессії
            можна або завантажити в памʼять бота існуючі контакти, або почати з нуля. В такому випадку
            в кінці сессії можна буде або дописати виконані зміни у файл, або проігнорувати
- WISHES - словник з "бажаннями"-командами, на які реагує бот:
    - "hello" - бот відповідає Хазяїну,
    - "add", "insert", "+" - за цими командами бот додає до телефонної книги нові контакти,
    - "change", "modify" - якщо після цих команд подати імʼя та новий телефон, існуючий
                            телефон буде змінений на новий,
    - "phone", "number", "find" - якщо після однієї з цих команд подати імʼя, бот покаже
                                 номер телефону для даної людини,
    - "show all", або просто "show" - бот виведе весь словник з контактами, які знаходяться
                                    в його памʼяті на даний момент,
    - "good bye", "close", "exit", "leave", "bye" - бот закінчує роботу
"""

# Декоратор для функції-санітайзера телефонних номерів
def format_phone_number(func):
    def wrapper(*args, **kwargs):
     
        if len(func(*args, **kwargs)) == 10:  # для коротких укр номерів
            result = "+38" + func(*args, **kwargs)
        elif len(func(*args, **kwargs)) == 12:  # для довгих укр номерів
            result = "+" + func(*args, **kwargs)
        else:                               # для всіх інших номерів
            result = func(*args, **kwargs)
        return result

    return wrapper


# Функція-санітайзер телефонних номерів
@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
    )   # тут ще мали прибиратись пробіли, але тоді глючить парсер
    return new_phone


# Декоратор для функції-парсера, який обробляє помилки
def wish_error(command_parser):
    def wrapper(*args, **kwargs):
        try:
            return command_parser(*args, **kwargs)
        except IndexError:  # тільки один вид помилок, бо наче інші не виникають (або нам потрібен нормальний тестер)
            return "Dear Master, may I kindly request the NAME and NUMBER?"
    return wrapper


the_Book_of_the_Damned = {} # це словник з контактами


# Функція, відповідальна за привітання Хазяїна ботом
def hello_handler(*args):
    return "Your personal Jinn is at your service, Master. Enter your Word of Wisdom!"


# Функція, відповідальна за додавання нових контактів в телефонну книгу
def add_handler(input_data: list):
    name = input_data[0].capitalize()
    phone = sanitize_phone_number(phone=input_data[1])
    the_Book_of_the_Damned.update({name: phone})
    return f"The number {phone} of {name} is sealed in The Book of The Damned till the End of Days or your next Command, Master"


# Функція, відповідальна за зміну у існуючого контакту телефонного номеру на новий
def change_handler(add_new_phone: list):
    name = add_new_phone[0].capitalize()
    new_phone = sanitize_phone_number(phone=add_new_phone[1])
    the_Book_of_the_Damned.update({name: new_phone})
    return f"I modified {name}'s number to {new_phone}, Master"


# Функція, відповідальна за вивід в консоль тел.номеру за імʼям
def show_only_phone_handler(phoneholder_name: list):
    for name in phoneholder_name:
        name = name.capitalize()
        if name in the_Book_of_the_Damned:
            for key, num in the_Book_of_the_Damned.items():
                if key == name:
                    return f"{name}'s phone is {num}"
    return "I'm afraid The Book of The Damned does not contain this contact yet"


# Функція, відповідальна за виведення в консоль всіх контактів з памʼяті бота на даний момент
def show_all_handler(*args):
    if the_Book_of_the_Damned:
        result = the_Book_of_the_Damned
    else:
        result = "The Book of The Damned is yet to be filled, Master"
    return result


# Функція, відповідальна за вихід з вічного циклу роботи бота
def exit_handler(*args):
    return "Summon me whenever you require my assistance, Master"


# Парсер команд
@wish_error
def command_parser(user_string: str):
    string_parts = user_string.split()
    for task, wish in WISHES.items():
        for command in wish:
            if command.startswith(string_parts[0]):
                return task(string_parts[1:])
    return "Master, I humbly admit that my abilities are limited.\nI may not fully understand your certain wishes.\nGive me ORDER, NAME and NUMBER."


# Словник бажань (функція: список команд)
WISHES = {
    hello_handler: ["hello"],
    add_handler: ["add", "insert", "+"],
    change_handler: ["change", "modify"],
    show_only_phone_handler: ["phone", "number", "find"],
    show_all_handler: ["show all"],
    exit_handler: ["good bye", "close", "exit", "leave", "bye"],
    }

# Декоратор до функції завантаження контактів з існуючого файлу
def contacts_loader_decorator(contacts_loader):
    def inner(*args, **kwargs):
        try:
            return contacts_loader(*args)
        except FileNotFoundError:
            print("Appologies, Master. The Book of The Damned does not exist yet.\nI'm already starting to write the new one.\n")
    return inner


# Функція, відповідальна за підвантаження контактів з існуючої бази (на початку сессії бота)
@contacts_loader_decorator
def contacts_loader(*args):
    with open("The_Book_of_The_Damned.txt", "r") as book:
        global the_Book_of_the_Damned
        the_Book_of_the_Damned = eval(book.read())
        print("The Book of The Damned is in my memory now.")

# Декоратор до функції зберігання контактів у файл
def contacts_saver_decorator(contacts_saver):
    def inner(*args, **kwargs):
        try:
            contacts_saver(*args)
        except FileNotFoundError:
            existing_dict = {}
    return inner

# Функція, відповідальна за збереження змін в телефонній книзі і записання їх у .txt файл
@contacts_saver_decorator
def contacts_saver(contact_book: dict):
    with open("The_Book_of_The_Damned.txt", "r") as book:
        existing_data = book.read()
        existing_dict = eval(existing_data)
        
    existing_dict.update(contact_book)

    with open("The_Book_of_The_Damned.txt", "w") as book:
        book.write(str(existing_dict))

    print("I'll guard The Book of The Damned forever")


# Головна функція "Джин", яка в умові задачі має називатись main()
def jinn():
    # привітання і стартові запитання до юзера:
    greeting_message = "-------------------\nMaster, give me the Name and Number,\nand I'll carve them into the Annals of Eternity!\nI can also modify your contact list, show it to you instantly\nand show only the number of your contact.\n"
    print(greeting_message)

    start_input = input("Would you like to behold the existent The Book of the Damned? Y or N\n")
    if start_input.startswith("Y") or start_input.startswith("y"):
        contacts_loader()

    # входимо у вічний цикл роботи з контактами:
    while True:
        user_input = input("I await patiently for you to command me, Master.\n")
        result = command_parser(user_input.lower())
        print(result)
        if result == "Summon me whenever you require my assistance, Master":
            end_input = input("Would you like me to save the information for later? Y or N:\n")
            if end_input.startswith("Y") or end_input.startswith("y"):
                contacts_saver(the_Book_of_the_Damned)
            break


if __name__ == "__main__":
    
    jinn()
