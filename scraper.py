''' EDM Train Scraper

This script scrapes the EDM Train website for the latest EDM events in the United States.
Specifically, it hits the following endpoint: https://edmtrain.com/get-events

Additonal arguments are added for location and time zone. Here's an example for the Bay
Area:

https://edmtrain.com/get-events?locationIdArray%5B%5D=72&includeElectronic=true&includeOther=false&timeZoneId=America%2FLos_Angeles

Sending a GET request, we can capture all the events.
'''

import requests
from bs4 import BeautifulSoup
import csv

# For the first version, I am hardcoding the URL for the Bay Area
URL = "https://edmtrain.com/get-events?locationIdArray%5B%5D=72&includeElectronic=true&includeOther=false&timeZoneId=America%2FLos_Angeles"

def main():
    response = requests.get(URL)
    data = response.text

    # Parse the HTML
    soup = BeautifulSoup(data, 'html.parser')

    # Find all event containers
    events = soup.find_all("div", class_="eventContainer")

    # Open a CSV file to store the data
    with open('events.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Event ID", "Image URL", "Date String", "Title", "Venue Name", "Venue Address", "Event URL", "Age Restriction", "Event Date"])

        # Loop through each event and extract details
        for event in events:
            event_id = event['eventid']
            image_url = "https://d2po6uops3e7id.cloudfront.net/" + event['eventimg']
            date_string = event['datestr']
            title = event['titlestr']
            venue_name = event.find(itemprop="name", class_="eventVenue").text
            venue_address = event.find(itemprop="address")['content']
            event_url = event.find('a')['href']
            age_restriction = event.find("span", class_="ageLabel").text if event.find("span", class_="ageLabel") else "All Ages"
            event_date = event.find("time")['datetime']

            # Write to CSV
            writer.writerow([event_id, image_url, date_string, title, venue_name, venue_address, event_url, age_restriction, event_date])

    print("Data scraping and storage complete.")


if __name__ == "__main__":
    main()