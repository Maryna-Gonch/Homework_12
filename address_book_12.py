from collections import UserDict
from datetime import date


class Field:
    def __init__(self, value: str):
        if self.check_correct(value):
            self.__value = value
        else:
            raise ValueError("Incorrect value")

    def __str__(self):
        return self.__value

    def check_correct(self, string: str):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        if self.check_correct(new_value):
            self.__value = new_value
        else:
            raise ValueError("Incorrect value")


class Name(Field):
    pass


class Phone(Field):
    def check_correct(self, string: str):
        return not any(not char.isnumeric() for char in string.removeprefix('+'))


class Birthday(Field):
    def check_correct(self, string: str):
        args = string.split("-")
        if tuple(map(len, args)) != (2, 2, 4):
            return False
        d, m, y = tuple(map(int, args))
        inp_date = date(y, m, d)
        if inp_date > date.today():
            return False
        return True

    def d_m_y(self):
        return (int(x) for x in self.__value.split("-")[::-1])


class Record:
    def __init__(self, name: Name, *args: Phone, birthday: Birthday = None):
        self.name = name
        self.phones = list(args)
        self.birthday = birthday

    def add_phone(self, *args: Phone):
        self.phones.extend(args)

    def del_phone(self, *args: Phone):
        for phone in args:
            self.phones.remove(phone)

    def edit_phone(self, *args: Phone):
        self.phones = list(args)

    def contain(self, value: str):
        if value in self.name.value:
            return True
        for phone in self.phones:
            if value in phone.value:
                return True
        return False

    def days_to_birthday(self):
        if self.birthday is None:
            return -1
        else:
            d, m, = self.birthday.d_m_y()
            cur_date = date.today()
            if cur_date < date(cur_date.year, m, d):
                return (date(cur_date.year, m, d) - cur_date).days
            else:
                return (date(cur_date.year + 1, m, d) - cur_date).days

    def __str__(self):
        if self.birthday is None:
            return f"{self.name}: {', '.join(str(phone) for phone in self.phones)}"
        else:
            return f"{self.name}: {', '.join(str(phone) for phone in self.phones)} with birthday on {self.birthday}"

    def __repr__(self):
        return str(self)


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.__iterator_counter = 0
        self.__n = 0

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def search(self, value: str):
        return [record for record in self.data.values() if record.contain(value)]

    def __next__(self):
        if self.__iterator_counter * self.__n <= len(self.data):
            self.__iterator_counter += 1
            return list(self.data.values())[(self.__iterator_counter-1)*self.__n:self.__iterator_counter*self.__n]
        self.__iterator_counter = 0
        raise StopIteration

    def __iter__(self):
        return self

    def iterator(self, N: int):
        self.__n = N
        self.__iterator_counter = 0
        return self
