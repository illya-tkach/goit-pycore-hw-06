from collections import UserDict


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Ім'я контакту (обов'язкове поле)."""

    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Name is required.")
        super().__init__(value)


class Phone(Field):
    """Номер телефону: рівно 10 цифр."""

    def __init__(self, value):
        # isdigit() + len() — перевірка формату
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    """Запис контакту: ім'я та список телефонів."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        found = self.find_phone(phone)
        if found is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(found)

    def edit_phone(self, old_phone, new_phone):
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError(f"Phone {old_phone} not found.")
        # Спершу створюємо новий Phone — щоб невалідний номер не зіпсував запис
        self.phones[self.phones.index(found)] = Phone(new_phone)

    def find_phone(self, phone):
        """Повертає об'єкт Phone або None, якщо номера немає."""
        return next((p for p in self.phones if p.value == phone), None)

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
        )


class AddressBook(UserDict):
    """Адресна книга: ключ — ім'я, значення — Record."""

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        """Повертає Record за ім'ям або None."""
        return self.data.get(name)

    def delete(self, name):
        if name not in self.data:
            raise KeyError(name)
        del self.data[name]


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    print(list(book.data))  # ['John']
