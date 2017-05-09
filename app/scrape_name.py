from bs4 import BeautifulSoup
import requests


def scrape_name(netid):
	search_url="http://www.princeton.edu/main/tools/search/?q="
	netid = str("rjaiswal")

	r = requests.get(search_url + netid)
	data=r.text
	soup=BeautifulSoup(data)

	name = soup.find(id = 'people-row-link-3')
	scraped_name = str(name).split("\n")[1]
	just_name = scraped_name.split(",")

	last_name = just_name[0].strip() 
	fname_array = just_name[1].split()

	if "." in fname_array[-1]:
		first_name=fname_array[0:-1] #new array without period name
	else:
		first_name=fname_array

	fname_str = ""
	for index, n in enumerate(first_name):
		fname_str += n
		if index != len(first_name)-1:
			fname_str += " "

	name_list = []
	name_list.append(fname_str)
	name_list.append(last_name)

	return name_list

print(scrape_name("rjaiswal"))