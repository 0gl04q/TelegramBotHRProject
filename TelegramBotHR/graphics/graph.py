# import matplotlib.pyplot as plt
#
# # Пример данных
# опрос_q12_данные = [
#     {"Ответ": "HRы", "Количество": 25},
#     {"Ответ": "Бухгалтеры", "Количество": 40},
#     {"Ответ": "Диспетчера", "Количество": 15},
#     {"Ответ": "Логисты", "Количество": 30},
# ]
#
# # Извлечение данных для построения графика
# варианты_ответов = [item["Ответ"] for item in опрос_q12_данные]
# количество_ответов = [item["Количество"] for item in опрос_q12_данные]
#
# # Построение графика
# plt.figure(figsize=(10, 6))
# plt.barh(варианты_ответов, количество_ответов, color='skyblue')
# plt.xlabel('Количество баллов')
# plt.title('Распределение ответов на вопрос Q12')
# plt.grid(axis='x')
#
# # Показать график
# plt.show()


import matplotlib.pyplot as plt


async def create_graph(data_survey):

    plt.figure(figsize=(8, 8))
    plt.pie(data_survey.values(), labels=data_survey.keys(), autopct='%1.1f%%', startangle=140,
            colors=['gold', 'lightskyblue', 'lightcoral', 'lightgreen'])
    plt.title('Распределение ответов на опрос Q12')

    name = 'график_q12.png'
    plt.savefig(name)

    return name


