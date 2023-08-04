# import argparse

# parser = argparse.ArgumentParser()

# parser.add_argument("hello", help="Bot will offer its help")
# args = parser.parse_args()


def format_phone_number(func):
    def wrapper(*args, **kwargs):
        if len(func(*args, **kwargs)) == 9:  # для коротких польских номерів
            result = "+48" + func(*args, **kwargs)
        elif len(func(*args, **kwargs)) == 11:  # для довгих польских номерів
            result = "+" + func(*args, **kwargs)
        elif len(func(*args, **kwargs)) == 10:  # для коротких укр номерів
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

if __name__ == "__main__":
    
    phone_dict = {}
    name_number_str = input("Enter name and number (Name, space, number): ")
    name_number_list = name_number_str.split(" ")

    write_phone = sanitize_phone_number(phone=name_number_list[1])

    phone_dict.update({name_number_list[0]: write_phone})
    print(phone_dict)