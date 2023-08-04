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


the_Book_of_the_Damned = {}


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
   for name in phoneholder_name:
        name = name.capitalize()
        for key, num in the_Book_of_the_Damned.items():
            if key == name:
                return f"{name}'s phone is {num}"


def show_all_handler(*args):
    if the_Book_of_the_Damned:
        result = the_Book_of_the_Damned
    else:
        result = "The Book of The Damned is yet to be filled, Master"
    return result

def exit_handler(*args):
    return "Summon me whenever you require my assistance, Master"


def command_parser(user_string: str):
    string_parts = user_string.split()
    for task, wish in WISHES.items():
        for command in wish:
            if command.startswith(string_parts[0]):
                return task(string_parts[1:])
    return "Unknown command"

WISHES = {
    hello_handler: ["hello"],
    add_handler: ["add", "insert", "+"],
    change_handler: ["change", "modify"],
    show_only_phone_handler: ["phone", "number"],
    show_all_handler: ["show all"],
    exit_handler: ["good bye", "close", "exit", "leave", "bye"],
    }


def jinn():
    while True:
        user_input = input("I await patiently for you to command me, Master: ")
        result = command_parser(user_input.lower())
        print(result)
        if result == "Summon me whenever you require my assistance, Master":
            break


if __name__ == "__main__":
    jinn()

#    "Master, give me the Name and Number, and I'll carve them into the Annals of Eternity: ")

