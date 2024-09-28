from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

# Path to your ChromeDriver
chrome_driver_path = '/Users/kevinyang/Desktop/Projects/chrome-mac-arm64'  # Replace with your ChromeDriver path

# Set up the Selenium WebDriver (with Chrome)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the calendar page
url = 'https://25live.collegenet.com/pro/brown/embedded/calendar?comptype=calendar&compsubject=location&itemTypeId=4&queryId=548963&embeddedConfigToken=4C7BA58F-4540-4940-AF8D-25D1A23A3C00#!/home/calendar'

# Open the page with Selenium
driver.get(url)

# Let the page load completely (adjust the sleep time as needed)
time.sleep(10)  # You might need to increase the sleep time if the page is slow to load

# Get the page source after JavaScript has run
html = driver.page_source

# Close the Selenium browser
driver.quit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all event containers
events = soup.find_all('div', class_='ngCalendarDayEventItem')

for event in events:
    # Extract the event time (start and end)
    start_time = event.find('span', class_='startDt').text.strip()
    end_time = event.find('span', class_='endDt').text.strip()

    # Extract the event title
    event_name = event.find('div', class_='s25-item-name').text.strip()

    # Extract the courts (subject)
    courts = event.find_all('div', class_='ngSubjectCalCellText')
    courts_list = [court.text.strip() for court in courts]

    # Output the details
    print(f"Event: {event_name}")
    print(f"Time: {start_time} - {end_time}")
    print(f"Courts: {', '.join(courts_list)}\n")

