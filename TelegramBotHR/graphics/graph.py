
import matplotlib.pyplot as plt


async def create_graph(data_survey):

    plt.figure(figsize=(8, 8))
    plt.pie(data_survey.values(), labels=data_survey.keys(), autopct='%1.1f%%', startangle=140,
            colors=['gold', 'lightskyblue', 'lightcoral', 'lightgreen'])
    plt.title('Распределение ответов на опрос Q12')

    name = 'график_q12.png'
    plt.savefig(name)

    return name


