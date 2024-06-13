import csv
import re
from pprint import pprint
from logger import logger_with_path

# Чтение данных из CSV файла
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Преобразование номера телефона в нужный формат
@logger_with_path("phonebook.log")
def format_phone_number(phone):
    pattern = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(?:\s*(доб\.)\s*(\d+))?')
    match = pattern.match(phone)
    if match:
        phone_number = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(6):
            phone_number += f" {match.group(6)}{match.group(7)}"
        return phone_number
    return phone

# Объединение дублирующихся записей
@logger_with_path("phonebook.log")
def merge_contacts(contacts):
    contacts_dict = {}
    for contact in contacts:
        lastname, firstname, surname = contact[:3]
        key = f'{lastname} {firstname}'
        if key in contacts_dict:
            for i, value in enumerate(contact):
                if not contacts_dict[key][i]:
                    contacts_dict[key][i] = value
        else:
            contacts_dict[key] = contact
    return list(contacts_dict.values())

# Приведение данных в порядок
header = contacts_list[0]
contacts = contacts_list[1:]

# Обработка данных: объединение ФИО и форматирование номера телефона
for contact in contacts:
    full_name = ' '.join(contact[:3]).split()
    contact[:3] = full_name + [''] * (3 - len(full_name))
    contact[5] = format_phone_number(contact[5])

# Удаление дублирующихся записей
contacts = merge_contacts(contacts)

# Сохранение отформатированных данных в новый CSV файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(header)
    datawriter.writerows(contacts)

# Печать результата для проверки
pprint(contacts)
