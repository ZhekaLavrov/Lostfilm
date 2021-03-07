import requests
from bs4 import BeautifulSoup
import fake_useragent

import parseSerials

def get_links_to_episodes(response):
	links = []
	soup = BeautifulSoup(response, 'lxml')
	# print(response)
	series = soup.find_all("div", {"class": "serie-block"})
	for serie in series:
		for episode in serie.find("table").find_all("td", {"class":"beta"}):
			links.append(str(episode)[str(episode).index("(")+2:str(episode).index("',")])
	return links

if __name__ == '__main__':
	episodes = []
	serials = parseSerials.load_json("serials_from_Lostfilm.json")
	# print(serials[0])

	for serial in serials:

		link = "https://www.lostfilm.uno/series/{serial}/seasons".format(
			serial = serial["link_name"]
		)

		response = parseSerials.get_response(link)
		episodes.append({
				"link_name": serial["link_name"],
				"episodes": get_links_to_episodes(response)
			})

		parseSerials.write_json("Episodes.json", episodes)
		print(serial["name_ru"])