the_Book_of_the_Damned = {}


def format_phone_number(func):
    def wrapper(*args, **kwargs):
     
        if len(func(*args, **kwargs)) == 10:  # для коротких укр номерів
            result = "+38" + func(*args, **kwargs)
        elif len(func(*args, **kwargs)) == 12:  # для довгих укр номерів
            result = "+" + func(*args, **kwargs)
        return result

    return wrapper


@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone
# def input_error(inner):
#     def wrap(*args):
#         try:
#             return inner(*args)
#         except IndexError:
#             return "Give me name and phone please"
#     return wrap


# @input_error

def hello_handler(*args):
    return "Your personal Jinn is at your service, Master. Enter your Word of Wisdom!"

def add_handler(input_data: list):
    name = input_data[0].capitalize()
    phone = sanitize_phone_number(phone=input_data[1])
    the_Book_of_the_Damned.update({name: phone})
    return f"The number {phone} of {name} is sealed in The Book of The Damned till the End of Days or your next Command, Master"

def change_handler(add_new_phone: list):
    name = add_new_phone[0].capitalize()
    new_phone = sanitize_phone_number(phone=add_new_phone[1])
    the_Book_of_the_Damned.update({name: new_phone})
    return f"I modified {name}'s number to {new_phone}"

def show_only_phone_handler(phoneholder_name: list):
    number = the_Book_of_the_Damned[phoneholder_name]
    return f"{phoneholder_name}'s phone is {number}"

def show_all_handler(*args):
    return the_Book_of_the_Damned

def exit_handler(*args):
    return "Summon me whenever you require my assistance, Master"
def exit_handler(*args):
    return "Good bye!"


def hello_handler(*args):
    return "Hello"


# @input_error
def command_parser(raw_str: str):  # Парсер команд
    elements = raw_str.split()
    for key, value in WISHES.items():
        if elements[0].lower() in value:
            return key(elements[1:])
    return "Unknown command"


WISHES = {
    hello_handler: ["hello"],
    add_handler: ["add", "insert", "+"],
    change_handler: ["change", "modify"],
    show_only_phone_handler: ["phone", "number"],
    show_all_handler: ["show"],
    exit_handler: ["good bye", "close", "exit", "leave", "bye"],
    }


def main():  # Цикл запит-відповідь.
    while True:
        user_input = input(">>> ")  # add Vlad 0987009090
        result = command_parser(user_input)
        print(result)
        if result == "Good bye!":
            break


if __name__ == "__main__":
    main()
