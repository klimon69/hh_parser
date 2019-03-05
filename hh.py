# импортируем библиотеку request для работы с данными в сети
import pypyodbc
import requests

search = input('Введи слово по которому будет осуществляться поиск вакансий: ')

f = open('vacancy.txt', 'w', encoding="utf-8")

connection =  pypyodbc.connect('Driver={SQL Server};'
                               'Server=DESKTOP-AJAIFVP;'
                               'Database=HH;'
                               #'uid=username;'
                               #'pwd=pmypassword'
                               )

cursor = connection.cursor()

mySQLQuery = ("""


IF OBJECT_ID(N'dbo.vacancyold', N'U') IS NOT NULL
		BEGIN
			drop table vacancyold
		END

		create table vacancyold (
		
		position varchar(200) NOT NULL,
		sallary varchar(30) NOT NULL,
		curensy varchar(10) NOT NULL,
		city varchar(105) NOT NULL,
		lastdate varchar(105) NOT NULL
		
		); 
--==================================================================


INSERT INTO vacancyold
SELECT * FROM vacancy


--==================================================================
IF OBJECT_ID(N'dbo.vacancy', N'U') IS NOT NULL
		BEGIN
			drop table vacancy
		END

		create table vacancy (
		
		position varchar(200) NOT NULL,
		sallary varchar(30) NOT NULL,
		curensy varchar(10) NOT NULL,
		city varchar(105) NOT NULL,
		lastdate varchar(105) NOT NULL
		
		); 




""")
cursor.execute(mySQLQuery)
connection.commit()


x=[]
all_zp = 0
all_n = 0
#цикл, который скачивает вакансии
for i in range(200):
    # запрос
    url = 'https://api.hh.ru/vacancies'
    #параметры, которые будут добавлены к запросу
    par = {'text': str(search),

           #"area": {"id":"89","parent_id":"1783","name":"Тверь"},
           # "areas": {
           #     "url": "https://api.hh.ru/areas/1",
           #     "id": "1",
           #     "name": "Москва"},

           'per_page':'10', 'page':i}
    r = requests.get(url, params=par)
    e=r.json()
    x.append(e)

for j in x:
    y = j['items']
    #объявляем переменную n для подсчета, количества итераций цикла перебирающего зарплаты в вакансиях
    n=0
    #объявляем переменную sum_zp для подсчета, суммы зарплат в вакансиях
    sum_zp=0
    #цикл, переберает объекты, т.е перебирает вакансии
    for i in y:
        # проверяем есть ли значения в словаре по ключу salary. Т.е проверяем есть ли в вакансии данные по зарплате
        if i['salary'] !=None:
            #записываем значение в переменную s

            sal=i['salary']

            if sal['from'] !=None:
                fromsal = sal['from']
            else:
                fromsal = 0

            if sal['to'] != None:
                tosal = sal['to']
            else:
                tosal = 0

            avgsal = (fromsal+tosal)/2

            currency = sal['currency']

            pos = i['name']
            date = i['published_at']
            if i['address'] !=None:
                fulladdr = i['address']
                city = fulladdr['city']
            else:
                city = "ЖОПА"
            f.write(str(avgsal) + " " + str(currency) + " " + pos + " " + str(date) + " " + str(city) + '\n')

            mySQLQuery = ("""INSERT INTO vacancy VALUES (?, ?, ?, ?, ?);""")
            cursor.execute(mySQLQuery,(str(pos),str(avgsal),str(currency),str(city),str(date)))
            connection.commit()



mySQLQuery = ("""select * from vacancy
                  WHERE vacancy.lastdate not in (
                                                  SELECT lastdate FROM vacancyold)""")
cursor.execute(mySQLQuery)

results = cursor.fetchall()

for row in results:
    pos = row[0]
    avgsal = row[1]
    currency = row[2]
    city = row[3]
    date = row[4]

    print(str(avgsal) + " " + str(currency) + " " + pos + " " + str(date) + " " + str(city))
    print("-"*50)

f.close()
connection.close()






