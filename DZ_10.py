import os
import collections
# списки можливих команд
EXIT_CMD = ['good bye', 'close', 'exit']
NO_ARGS_CMD = ['hello', 'show all']
WITH_ARGS_CMD = ['add', 'change', 'phone']
EXIT_ANSWER = 'Good bye!'

# повідомлення запрошення
INVITATION = """ 
------------------------------------------------------------------------------------------------------------------------------------------------
|                                                PHONE BOOK BOT WELCOMES YOU!                                                                  |
------------------------------------------------------------------------------------------------------------------------------------------------
|    COMMANDS:                                                                                                                                 |
|    o	"hello"                                                                                                                                |
|    o	"add ..." По этой команде бот сохраняет в памяти новый контакт.                                                                        |
|        Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.                                                        |
|    o	"change ..." По этой команде бот сохраняет в памяти новый номер телефона для существующего контакта.                                   |
|        Вместо ... пользователь вводит имя , старый и новый номер телефона, обязательно через пробел.                                         |
|    o	"phone ...." По этой команде бот выводит в консоль номер телефона для указанного контакта.                                             |
|        Вместо ... пользователь вводит имя контакта, чей номер нужно показать.                                                                |
|    o	"show all". По этой команде бот выводит все сохраненные контакты с номерами телефонов в консоль.                                       |
|    o	"good bye", "close", "exit" по любой из этих команд бот завершает свою роботу.                                                         |
------------------------------------------------------------------------------------------------------------------------------------------------"""

"""----------------------------------------------------------------------------
                                Реалізація класів
-------------------------------------------------------------------------------"""


class Field:
    """ Батьківський клас "Поле" -  містить в собі якусь інформацію """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, __value: object) -> bool:
        """ Для порівняння на рівність двох екземплярів даного класу """
        # порівнюються значення поля value
        return self.value == __value.value

class Name(Field):
    """ Поле ім'я """

    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    """ Поле номер телефону """

    def __init__(self, value=None):
        super().__init__(value)



class Record:
    """ Запис з книги контактів. Містить в собі поля """

    def __init__(self, name_value, phone_value=None):
        # атрибут ім'я
        self.name = Name(name_value)
        # атрибут список телефонів
        self.phones = []
        # додаємо телефон в список
        self.phones.append(Phone(phone_value))

    def __str__(self) -> str:
        # список екземплярів в список рядків
        phones = [str(x) for x in self.phones]
        # повертаємо загальний рядок
        return f'{self.name} - {phones}'

    def add_phone(self, value):
        """ Додає телефон в список """
        new_phone = Phone(value)
        # випадок : чи телефон існує в списку
        if new_phone not in self.phones:
            self.phones.append(new_phone)

    def del_phone(self, value):
        """ Видаляє телефон з списку """
        # випадок : такого номеру не має в базі
        try:  
            # Видаляємо номер
            self.phones.remove(Phone(value))
        except ValueError:
            pass

    def update_phone(self, old_value, new_value):
        """ Оновлює телефон в списку """
        # знаходимо індекс даного номеру в списку
        # якщо індекс не буде знайдено то буде кинуте виключення input_error його відловить
        idx = self.phones.index(Phone(old_value))
        # заміняємо старе значення новим
        self.phones[idx] = Phone(new_value)


class AddressBook(collections.UserDict):
    """ Книга контактів. Містить в собі записи Record"""

    def __init__(self):
        super().__init__()

    def add_record(self, name_value, phone_value = None):
        """ Додає новий запис в книгу """
        # випадок : якщо ім'я є в базі
        if name_value in self:
            # додаємо новий номер до запису
            self[name_value].add_phone(phone_value)
        else:
            # додаємо новий запис
            self[name_value] = Record(name_value, phone_value)

    def is_empty(self):
        """ Перевіряє чи книга пуста """
        return len(self.items()) == 0

    def has_record(self, name_value):
        """ Перевіряє чи є дане ім'я в базі """
        return name_value in self


"""----------------------------------------------------------------------------
                Функції що відповідають за роботу бота
-------------------------------------------------------------------------------"""


def input_error(func):
    """ Декоратор обробник помилок """
    def wrapper(*args, **kwargs):
        # намагаємось виконати хандлер
        try:
            result = func(*args, **kwargs)
        # відловлюємо помилки
        except SyntaxError:
            result = 'Your command is incorrect!'
        except KeyError:
            result = 'Name was not found or incorrect!'
        except ValueError:
            result = 'Phone number is incorrect!'
        return result
    return wrapper


def hello_handler(*args):
    """ Обробник команди hello """
    return 'How can I help you?'


def exit_handler(*args):
    """ Обробник команди на вихід """
    return EXIT_ANSWER


def show_all_handler(address_book: AddressBook):
    """ Обробник команди вивести всі записи """
    # випадок : словнки не пустий
    if not address_book.is_empty():
        # список рядків
        strings = []
        # обходимо книгу записів
        for value in address_book.values():
            # друкуємо ключ значення в рядок
            strings.append(f'{value}\n')
        # повертаємо всі рядки об'єднані в один великий загальний
        return ''.join(strings)
    else:
        return 'Phone book is EMPTY!'


@input_error
def parser(expression):
    """ Розбиває рядок на команду та можливі аргументи """
    # розіб'ємо рядок по пробілам та зберемо заново всі частки
    expression = ' '.join(expression.split())
    # випадок : якщо рядок є командою з одного із списків
    if expression in EXIT_CMD or expression in NO_ARGS_CMD:
        # повертаємо вираз як команду і пустий список аргументів
        return expression, []
    # інашке розбиваємо по пробілу
    args = expression.split()
    # випадок : якщо кількість частин від 1 до 4включно
    if len(args) > 1 and len(args) <= 4 and args[0] in WITH_ARGS_CMD:
        # повертаємо першу частину як команду а інщі частини як агрументи
        return args[0], args[1:]
    else:
        # інакше кидаємо виключення
        raise SyntaxError


@input_error
def add_handler(address_book: AddressBook, *args):
    """ Обробка додавання в книгу  """
    # випадок : якщо кількість агрументівн не коректна
    if len(args) != 2:
        raise SyntaxError

    name, tel = args
    # випадок номер не число
    if not tel.isnumeric():
        raise ValueError
    # випадок : ім'я закоротке
    if len(name) < 2:
        raise KeyError
    # додамо в словник
    # address_book[name] = tel
    address_book.add_record(name, tel)
    return f'{name} was included into phone book!'


@input_error
def phone_handler(address_book: AddressBook, *args):
    """ Відображення заданого запису по імені """
    # випадок : аргументів забагато або мало
    if len(args) != 1:
        # кидаємо виключення
        raise SyntaxError
    name = args[0]
    #  випадок : ім'я відсутне в книгі
    if not address_book.has_record(name):
        raise KeyError
    # повертаємо рядок
    return f'{address_book[name]}'


@input_error
def change_handler(address_book: AddressBook, *args):
    """ Обробка команди внесення змін по номеру """
    # випадок : аргументи не коректні
    if len(args) != 3:
        raise SyntaxError
    name = args[0]
    old_tel = args[1]
    new_tel = args[2]

    # випадок : ім'я відсутне в книзі
    if not address_book.has_record(name):
        raise KeyError

    # випадок : номер не коректний
    if not old_tel.isnumeric() or not new_tel.isnumeric():
        raise ValueError

    # робимо зміни
    address_book[name].update_phone(old_tel,new_tel)
    return f'{name} was updated!'


"""----------------------------------------------------------------------------
                                Головна функція
-------------------------------------------------------------------------------"""


def main():
    # пуста книга словник
    address_book = AddressBook()

    # словник обробників команд
    # команда - назва функції
    handlers = {
        'hello': hello_handler,
        'good bye': exit_handler,
        'close': exit_handler,
        'exit': exit_handler,
        'show all': show_all_handler,
        'add': add_handler,
        'phone': phone_handler,
        'change': change_handler
    }

    # безкінечнйи цикл запитів
    while True:
        # очистка консолі
        os.system('cls')
        # друк привітання запрошення
        print(INVITATION)
        # читаємо рядок команд
        # відразу переводимо в нижній регістр
        expression = input('->').lower().strip()
        # якщо рядок пустий то все заново
        if len(expression) == 0:
            continue
        # отримуємо результат парсингу
        answer = parser(expression)
        # випадок : якщо результат не рядок з помилкою
        if not isinstance(answer, str):
            # розпаковуємо кортеж команд і аргументів
            cmd, args = answer
            # викликаємо хандлер по назві команди та передаємо в ного словник-книгу + агрументи
            answer = handlers[cmd](address_book, *args)
        # друкуємо отриманий результат

        print(answer)
        # пауза
        os.system('pause')

        # випадок : отримано команду на вихід
        if answer == EXIT_ANSWER:
            break


if __name__ == "__main__":
    main()
