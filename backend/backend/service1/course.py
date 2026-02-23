import csv
from database import DB


def parse_dataset(filename):
    with open(filename, "r", encoding='utf-8') as f:
        lines = f.readlines()
        dataset = []
        for line in lines[1:]:  # пропускаем первую строку
            # Ищем необходимые индексы для деления строки:
            first_comma = line.index(',')
            second_comma = line.index('[', first_comma + 1)

            name = line[:first_comma].strip()
            description = line[first_comma + 1:second_comma].strip()
            keys_string = line[second_comma + 1:].split(']')[0]
            # Обрабатываем строку ключей:
            keys = [key.strip("'") for key in keys_string.split(', ')]
            # Создаем словарь для строки и добавляем его в датасет
            row_dict = {"Name": str(name).replace('",', '').replace('\xa0', ''),
                        "Description": str(description).replace('",', '').replace('\xa0', ''), "Keys": keys}
            dataset.append(row_dict)

    return dataset


collection = DB.get_collection('courses_cfo')
filename = "my_data.csv"
dataset = parse_dataset(filename)
for record in dataset:
    collection.insert_one(
        {"name": record['Name'], "desc": record['Description'], "keywords": record['Keys'], "rating": 0.0,
         "count_views": 0})



