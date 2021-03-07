"""
Получение названий всех сериалов на сайте Lostfilm
"""

import requests
from bs4 import BeautifulSoup
import fake_useragent

def write_json(file_name, data):  # Запись в JSON
	import json
	import os

	# Создание директорий
	directories = file_name.split("/")[:-1]
	path = ""
	for directory in directories:
		path = path + directory + "/"
		if os.path.exists(path):
			if os.path.isdir(path):
				pass
			else:
				os.mkdir(path)
		else:
			os.mkdir(path)

	# Создание файла
	with open(file_name, "w", encoding='utf-8' ) as f:
		json.dump(data, f, indent = 2, ensure_ascii = False)

def load_json(file_name):  # Загрузка из JSONа
	import json

	with open(file_name, 'r', encoding='utf-8') as f:
		data = json.load(f)
	return data

def get_response(link):
	user = fake_useragent.UserAgent().random

	header = {
	    'user-agent': user
	}

	response = requests.post(
	    link,
	    headers=header
	).text

	return response

def get_object_serials(response):

	serials = []

	soup = BeautifulSoup(response, 'lxml')

	serials_list = soup.find(id="serials_list").find_all("a")
	for serial in serials_list:
		link_name = str(serial).split("\n")[0][39:-2]
		# print(link_name)
		name_ru = str(serial.find("div", {"class": "name-ru"}))[21:-6]
		# print(name_ru)
		name_en = str(serial.find("div", {"class": "name-en"}))[21:-6]
		# print(name_en)
		serials.append(
			{
				"link_name": link_name,
				"name_ru": name_ru,
				"name_en": name_en,
			}
		)
	return serials

# Какой должна быть ссылка
link = "https://www.lostfilm.uno/series/?type=search&s={s}&t={t}&o={o}".format(
	s=2,  # Сортировать по 1 - рейтингу; 2 - алфавиту, 3 - Новизне
	t=0,  # 0 - ВСЕ; 1 - НОВЫЕ; 2 - СНИМАЮЩИЕСЯ; 3 - ЗАВЕРШЕННЫЕ; 4 - ИЗБРАННЫЕ
	o=0,  # откуда начинать (по 10 сериалов на странице)
)

if __name__ == '__main__':
	serials = []
	file_name = "serials_from_Lostfilm.json"
	
	i = 0
	while True:
		out = False
		link = "https://www.lostfilm.uno/series/?type=search&s={s}&t={t}&o={o}".format(
			s=2,  # Сортировать по 1 - рейтингу; 2 - алфавиту, 3 - Новизне
			t=0,  # 0 - ВСЕ; 1 - НОВЫЕ; 2 - СНИМАЮЩИЕСЯ; 3 - ЗАВЕРШЕННЫЕ; 4 - ИЗБРАННЫЕ
			o=i*10,  # откуда начинать (по 10 сериалов на странице)
		)
		obj = get_object_serials(get_response(link))
		for serial in obj:
			if serials.count(serial):
				out = True
				print(serial)
				break
			else:
				serials.append(serial)
				print(serial["name_ru"])
		if len(obj) == 0:
			break
		write_json(file_name, serials)
		if out:
			break
		i += 1
