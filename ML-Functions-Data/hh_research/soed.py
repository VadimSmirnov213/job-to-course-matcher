import pandas as pd

# Считываем данные из файлов
df1 = pd.read_csv('new1.csv')
df3 = pd.read_csv('new3.csv')
df4 = pd.read_csv('new4.csv')
df5 = pd.read_csv('new5.csv')
df6 = pd.read_csv('new6.csv')
df7 = pd.read_csv('new7.csv')
df8 = pd.read_csv('new8.csv')
df9 = pd.read_csv('new9.csv')
df10 = pd.read_csv('new10.csv')
df11 = pd.read_csv('new11.csv')
df12 = pd.read_csv('new12.csv')

# Объединяем данные
df = pd.concat([df1, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12])

# Удаляем строки, где значение в третьем столбце пустое
df = df[df[df.columns[2]].notna()]

# Удаляем строки, где значение в девятом столбце пустой список
df = df[df[df.columns[8]].apply(lambda x: len(eval(x)) != 0 if isinstance(x, str) and x.startswith('[') else True)]

# Записываем результат в новый файл
df.to_csv('combined.csv', index=False)
