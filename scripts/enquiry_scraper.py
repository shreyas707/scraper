import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pdb
import requests
import json
import os

# Ignore SSL certificate errors
ssl._create_default_https_context = ssl._create_unverified_context

def build_link(enquiry) :
	return enquiry.find("a", attrs={"class": "redLink"})['href']

def build_title(details) :
	return details[0].text.strip()

def build_status(details) :
	if details[1].text.strip().split()[-1] == "Closed" :
		return "Closed"
	else :
		return "Open"

def build_name(details) :
	return details[3].text.strip()

def build_location(details) :
	if len(details[4].text.strip().split(', ')) == 1 :
		location = ["online", "online"]
	else :
		location = [details[4].text.strip().split(', ')[0], details[4].text.strip().split(', ')[1]]
	return location

def build_location_preference(details) :
	details_list = []
	for detail in details :
		details_list.append(detail.text.strip())
	return (', '.join(details_list[details_list.index("Location Preference")+1:]))

def build_date(details) :
	date_and_status_details = details[1].text.strip().split()
	# ['Category:', 'Java', 'Training', '|', 'Posted', '1', 'day', 'ago']
	if date_and_status_details[-1] == "ago" :
		return ' '.join(date_and_status_details[-3:])
	# ['Category:', 'Java', 'Training', '|', 'Posted', '06', 'Aug']
	elif date_and_status_details[-1] != "Closed" and date_and_status_details[-2] != "day" :
		return ' '.join(date_and_status_details[-2:])
	# ['Category:', 'Java', 'Training', '|', 'Posted', '06', 'Aug', 'Closed']
	elif date_and_status_details[-1] == "Closed" and date_and_status_details[-2] != "ago" :
		date_and_status_details.pop()
		return ' '.join(date_and_status_details[-2:])
	# ['Category:', 'Java', 'Training', '|', 'Posted', '1', 'day', 'ago', 'Closed']
	elif date_and_status_details[-1] == "Closed" and date_and_status_details[-2] == "ago" :
		date_and_status_details.pop()
		return ' '.join(date_and_status_details[-3:])


courses = { "angular_js": "1564", "java_training": "390", "mobile_app_dev": "1477", "web_designing": "351", "web_developement": "719", "html": "999", "amazon_web_services": "787", "java_script_training": "411", "dev_ops_training": "1794", "jquery": "1056", "node_js": "1565", "mongo_db": "1563", "ajax_training": "414" }

information = {}

i = 1

for course_name, course_id in courses.items() :
	print(course_name)
print("\n")

for course_name, course_id in courses.items() :
	
	information[course_name] = {}
	start_page = 1

	website = "https://www.urbanpro.com"
	end_page = 1 # soup.find_all("a", attrs={"class": "step"})[-1].text

	while start_page <= int(end_page) :

		url = "https://www.urbanpro.com/need/search?topicId=" + course_id + "&distance=2&max=10&refineSearch=true&regularNeed=on&sortBy=CREATED&featuredNeed=on&filterBy=LAST30DAYS&page=" + str(start_page)

		print("\n")
		print("Fetching data from", url)
		html = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html, 'html.parser')

		enquiry_card_divs = soup.find_all("div", attrs={"class": "enquiry-card clearfix"})
		if len(enquiry_card_divs) == 0 :
			print("No records were found in this page.")

		for enquiry in enquiry_card_divs :
			information[course_name][i] = {}
			details = enquiry.find_all('p')

			information[course_name][i]["link"] = website + build_link(enquiry)
			information[course_name][i]["title"] = build_title(details)
			information[course_name][i]["status"] = build_status(details)
			information[course_name][i]["name"] = build_name(details)
			information[course_name][i]["area"] = build_location(details)[0]
			information[course_name][i]["city"] = build_location(details)[1]
			information[course_name][i]["location_preference"] = build_location_preference(details)
			information[course_name][i]["category"] = course_name
			information[course_name][i]["date"] = build_date(details)

			i += 1

		start_page += 1


for course_name, index_and_info in information.items() :
	for index, info in index_and_info.items() :
		enquiry = {}
		enquiry["enquiry"] = info
		requests.post("http://localhost:3000/enquiries", json = enquiry)
		