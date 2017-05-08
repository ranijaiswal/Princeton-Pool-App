from bs4 import BeautifulSoup
import requests


def scrape_name(netid):
	search_url="http://www.princeton.edu/main/tools/search/?q="
	netid = str(netid)

	r = requests.get(search_url + netid)
	data=r.text
	soup=BeautifulSoup(data)

	name = soup.find(id = 'people-row-link-3')
	just_name = str(name).split("\n")[1]
	# print just_name
	clean_name = just_name.split(",")
	# print clean_name
	final_name = clean_name[1].strip() 

	return final_name
