# coding: UTF-8
payload = {
	"username": "Drakona", 
	"password": "password", 
	"sid": "f4cd64c990eb89e7c38b6975762808dc",
	"redirect":"index.php",
	"mode": "login",
	"login": "Вход"
}
import requests
import math
from lxml import html
session_requests = requests.session()
login_url = "http://casualclan.com/forum/ucp.php?mode=login"
users_count_url = "http://casualclan.com/forum/index.php"
after_url = "http://casualclan.com/forum/memberlist.php?mode=viewprofile&u=1055"
user_url = "http://casualclan.com/forum/memberlist.php?mode=viewprofile&u="
result = session_requests.get(login_url)
#print result.content
tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='sid']/@value")))[0]
#print(authenticity_token)
payload['auth_key'] = authenticity_token
result = session_requests.post(
	login_url, 
	data = payload, 
	headers = dict(referer=login_url)
)
result = session_requests.get(
	users_count_url, 
	data = payload, 
	headers = dict(referer=login_url)
)
main_page = result.content
new_user  = "Новый пользователь"
A = main_page.find(new_user)
users_count = int(main_page[A+94:A+98])
#users_count = 80
bank1 = 0
bank_of_deleted_users = 0
bank_of_la2_users = 0
bank_of_total_age = 0
bank_of_la2_users_without_age = 0
incorrect_date_of_reg = 0
incorrect_date_of_last_visit = 0
USER_DELETED_TEXT  = "Информация"#"Запрашиваемого пользователя не существует"
DATE_OF_REGISTRATION = "Зарегистрирован"
NICKNAME = "Профиль пользователя"
DATE_OF_LAST_VISIT = "Последнее посещение"
ALL_MESSAGES = "Всего сообщений"
REPUTATION = "Репутация"
REP_WEIGHT = "Показатель репутации"
EMAIL = "Адрес email"
MSNM = "MSNM/WLM"
YIM = "YIM"
GROUPS = "Группы"
GROUP_LA2 = "Игроки L2"
ADDRESS = "Откуда"
AGE = "Возраст"
OCCUPATION = "Род занятий"
INTERESTS = "Интересы"
USERSITE = "Сайт"
USER_REAL_NAME = "Имя в реале"
MONTH_OF_REG = {'1':'янв', '2':'фев', '3':'мар', '4':'апр', '5':'май', '6':'июн', '7':'июл', '8':'авг', '9':'сен', '10':'окт', '11':'ноя', '12':'дек'}
class gamer(object):
    def __init__(self, date_of_reg):
        self.date_of_reg = date_of_reg
#instancelist = [ MyClass() for i in range(29)]
#instancelist[5].attr1 = 'whamma'
#print(users_count)
for x in range (1, users_count):
    #print(user_url + str(x))
    result = session_requests.get(
	user_url + str(x), 
	data = payload, 
	headers = dict(referer=login_url)
    )
    tmp = result.content
    if x % 50 == 0:
        print(x)
    #print(tmp)
    user_deleted_flag = tmp.find(USER_DELETED_TEXT)
    if user_deleted_flag != -1:
        bank_of_deleted_users = bank_of_deleted_users+1
	continue
    user_group = tmp.find(GROUP_LA2)
    if user_group == -1:
        continue
    bank_of_la2_users = bank_of_la2_users + 1
    #print('finally la2 user')
    #f = open(str(x)+".html","w")
    #f.write(tmp)
    #f.close()
    age = tmp.find(AGE)
    #print(tmp[age+48:age+50])
    if age == -1:
        bank_of_la2_users_without_age = bank_of_la2_users_without_age + 1
    else:
        bank_of_total_age = bank_of_total_age + int(tmp[age+48:age+50]) #!!!
    A = tmp.find(DATE_OF_REGISTRATION)
    DD = tmp[A+73:A+76]
    MM = tmp[A+77:A+83]
    YY = tmp[A+84:A+89]
    for key in MONTH_OF_REG:
        #print(key)
        if MM == MONTH_OF_REG[key]:
            MM = int(key)
    #gamer(str(DD) + "-" + str(MM) + "-" + str(YY))
    #print(gamer.date_of_reg)
    #print(DD + " " + MM + " " + YY)
avg_age = math.floor((bank_of_total_age / (bank_of_la2_users - bank_of_la2_users_without_age)) * 10)/10
print('average age is ' + str(avg_age))
print('total age is ' + str(bank_of_total_age))
print('total la2 users is ' + str(bank_of_la2_users))
print('total la2 users without age is ' + str(bank_of_la2_users_without_age))    
print('total deleted users is ' + str(bank_of_deleted_users))
