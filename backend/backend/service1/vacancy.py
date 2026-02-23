import csv
from database import DB


def parse_dataset(filename):
    with open(filename, "r", encoding='utf-8') as f:
        lines = f.readlines()
        dataset = []
        for line in lines[1:]:  # пропускаем первую строку
            parts = line.split(',', 7)  # split line into 8 parts
            schedule_keys = parts[-1].split('[', 1)  # split last part into Schedule and Keys
            keys_description = schedule_keys[1].split(']', 1)  # split last part into Keys and Description
            parts[-1] = schedule_keys[0]  # replace last part with split result
            parts.extend(keys_description)  # append split results to parts

            row_dict = {
                "Ids": parts[0].strip().replace(',"', '').replace('","', '').replace('(', '').replace("'", ''),
                "Employer": parts[1].strip().replace(',"', '').replace('","', '').replace("'", ''),
                "Name": parts[2].strip().replace(',"', '').replace('","', '').replace("'", ''),
                "Salary": parts[3].strip().replace(',"', '').replace('","', '').replace("'", ''),
                "From": parts[4].strip().replace(',"', '').replace('","', '').replace("'", ''),
                "To": parts[5].strip().replace(',"', '').replace('","', '').replace("'", ''),
                "Experience": parts[6].strip().replace(',"', '').replace('","', '').replace("'", ''),
                "Schedule": parts[7].strip().replace(',"', '').replace('","', '').replace("',", '').replace("'", ''),
                "Keys": '[' + parts[8].strip().replace('[', '') + ']',
                "Description": str(parts[9].strip()).replace('","', '').replace('"', '').replace(',"', '').replace("'",
                                                                                                                   ''),
            }

            dataset.append(row_dict)
    return dataset


filename = "vacancy1.csv"
dataset = parse_dataset(filename)

collection = DB.get_collection('vacs_cfo')
for record in dataset:
    collection.insert_one(record)
