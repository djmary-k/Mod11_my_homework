# Завдання
# У цьому домашньому завданні ми:
# +Додамо поле для дня народження Birthday. Це поле не обов'язкове, але може бути тільки одне.
# +Додамо функціонал роботи з Birthday у клас Record, а саме функцію days_to_birthday, яка повертає кількість днів до наступного дня народження.
# +Додамо функціонал перевірки на правильність наведених значень для полів Phone, Birthday.
# -?Додамо пагінацію (посторінковий висновок) для AddressBook для ситуацій, коли книга дуже велика і треба показати вміст частинами, а не все одразу. Реалізуємо це через створення ітератора за записами.

# Критерії прийому:
# +AddressBook реалізує метод iterator, який повертає генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів.
# +Клас Record приймає ще один додатковий (опціональний) аргумент класу Birthday
# +Клас Record реалізує метод days_to_birthday, який повертає кількість днів до наступного дня народження контакту, якщо день народження заданий.
# +setter та getter логіку для атрибутів value спадкоємців Field.
# +Перевірку на коректність веденого номера телефону setter для value класу Phone.
# +Перевірку на коректність веденого дня народження setter для value класу Birthday.

from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value
        # print(f'from Field: {self.value}')


class Name(Field):
    # name = True
    pass


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
        super().__init__(self.__value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        # print(value.__class__)
        if (type(value) == int) and (len(str(value)) == 12):
            self.__value = value



class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
        super().__init__(self.__value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        # print(value.__class__)
        if type(value) == datetime:
            self.__value = value


class Record:
    def __init__(self, name: Name, phone: Phone=None, birthday: Birthday=None): #: phone - це не обовязковий агрумент, тому по замовчюванню None
        """в тестах ми заповнюємо класс Record обьектами класів name та phone, тому в цьому конструкторі вже приходять
        не просто строки типу 'Bill', а саме обьекти классу name
        name = Name('Bill')
        phone = Phone('1234567890')
        """
        self.name = name
        self.phone = []
        self.birthday = birthday
        if phone:
            self.phone.append(phone)

    def __str__(self):
        return f"{self.name.value} {[ph.value for ph in self.phone]} {self.birthday.value}"
        
    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phone:
            self.phone.append(phone_number)

    # def find_phone(self, value):
    #     pass

    def delete_phone(self, phone):
        self.phone.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phone.index(old_phone)
        self.phone[index] = new_phone

    def days_to_birthday(self, birthday): #повертає кількість днів до наступного дня народження
        current_date = datetime.now().date()
        if birthday:
            birthday_date = birthday.replace(year=datetime.now().year).date() 
            delta = birthday_date - current_date
            if delta.days >= 0:
                return f'{delta.days} days to birthday'
            else:
                delta = birthday_date.replace(year=datetime.now().year+1) - current_date
                return f'{delta.days} days to birthday'
        else:
            return None


class AddressBook(UserDict):
    N = 2 # чому 2?

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        # {‘Bill’: “Bill 0987777 22.09.2000”} - результат add_record
    
    def find_record(self, value):
        return self.data.get(value)
    
    def iterator(self, n) -> list[dict]:
        contact_list = []  # список записів контактів
        if n:
            AddressBook.N = n
        for record in self.data.values():
            contact_list.append(record)
        return self.__next__(contact_list)
    
    # def __iter__(self):
    #     return self
    
    # def __next__(self):
    #     self.count += 1
    #     if self.count > len(self.data):
    #         raise StopIteration
    #     else:
    #         return self.data[list(self.data.keys())[self.count-1]]

    def __iter__(self, contact_list: list[dict]):
        n_list = []
        counter = 0
        for contact in contact_list:
            n_list.append(contact)
            counter += 1
            if counter >= AddressBook.N:  # якщо вже створено список із заданої кількості записів
                yield n_list
                n_list.clear()
                counter = 0
        yield n_list

    def __next__(self, contact_list):
        generator = self.__iter__(contact_list)
        page = 1
        while True:
            user_input = input("Press ENTER")
            if user_input == "":
                try:
                    result = next(generator)
                    if result:
                        print(f"{'*' * 20} Page {page} {'*' * 20}")
                        page += 1
                    for var in result:
                        print(var)
                except StopIteration:
                    print(f"{'*' * 20} END {'*' * 20}")
                    break
            else:
                break




# ### Checking mentor
if __name__ == "__main__":
    # record contact 1
    name = Name('Bill')
    phone = Phone(123456789012)
    birthday = Birthday(datetime(1990, 8, 3))
    rec = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)
    print(ab)
    print(rec.birthday.value)
    print(rec.days_to_birthday(datetime(1990, 8, 3)))
    print(rec.phone)
    # record contac 2
    name2 = Name('Mary')
    phone2 = Phone(987654321012)
    birthday2 = Birthday(datetime(1993, 9, 25))
    rec2 = Record(name2, phone2, birthday2)
    ab.add_record(rec2)
    print(ab)
    print(rec2.birthday.value)
    print(rec2.days_to_birthday(datetime(1993, 9, 25)))
    print(rec2.phone)

    ##print(isinstance(ab['Bill'], Record))
    assert isinstance(ab['Bill'], Record) # оператор assert працює так, він порівнює щось, я якщо це порівняння дає false - він викликає помилку
    ##print(isinstance(ab['Bill'].name, Name))
    assert isinstance(ab['Bill'].name, Name) # тут він перевіряє що в книзі контактів під ключем 'Bill' - знаходиться обьект классу Name
    ##print(isinstance(ab['Bill'].phone, list))
    assert isinstance(ab['Bill'].phone, list)
    ##print(isinstance(ab['Bill'].phone[0], Phone))
    assert isinstance(ab['Bill'].phone[0], Phone)
    ##print(ab['Bill'].phone[0].value == '1234567890')
    assert ab['Bill'].phone[0].value == 123456789012

    
    """Додамо контактів для перевірки ітератора"""
    name = Name('Bob')
    phone = Phone(123456789012)
    birthday = Birthday(datetime(1980, 1, 31))
    rec2 = Record(name, phone, birthday)

    name = Name('Tom')
    phone = Phone(123456789012)
    birthday = Birthday(datetime(1992, 12, 13))
    rec3 = Record(name, phone, birthday)

    name = Name('Bard')
    phone = Phone(123456789012)
    birthday = Birthday(datetime(2000, 4, 10))
    rec4 = Record(name, phone, birthday)

    ab.add_record(rec2)
    ab.add_record(rec3)
    ab.add_record(rec4)

    ab.iterator(n=3)
    
    print('All Ok)')

