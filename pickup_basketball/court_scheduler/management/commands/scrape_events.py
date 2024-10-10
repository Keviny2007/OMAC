from django.core.management.base import BaseCommand
from court_scheduler.models import Event
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import datetime
import time

class Command(BaseCommand):
    help = 'Scrapes and imports gym events into the database'

    def handle(self, *args, **kwargs):
        # Set up Selenium
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        # change this link weekly
        url = "https://25live.collegenet.com/pro/brown/embedded/calendar?comptype=calendar&compsubject=location&itemTypeId=4&queryId=548963&embeddedConfigToken=4C7BA58F-4540-4940-AF8D-25D1A23A3C00#!/home/event/482576/details"
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        driver.quit()

        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Clear previous events in database
        Event.objects.all().delete()

        # Extract days of week
        days_of_week = [th.text for th in soup.find('thead').find_all('th')]

        # Extract date cells
        date_cells = soup.find_all('div', class_='CalendarDayHeader')

        # Map dates to corresponding days
        date_mapping = {}
        previous_date_obj = None
        for i, cell in enumerate(date_cells):
            date_text = cell.find('a').text.strip()
            if len(date_text.split()) > 1:  # check if month text
                date_obj = datetime.datetime.strptime(date_text, "%B %d")
                date_obj = date_obj.replace(year=datetime.datetime.now().year)
            else:  # just date number
                day = int(date_text)
                
                if previous_date_obj and day < previous_date_obj.day:
                    month = previous_date_obj.month + 1
                    if month > 12:
                        month = 1
                    date_obj = previous_date_obj.replace(month=month, day=day)
                else:
                    date_obj = previous_date_obj.replace(day=day)  

            date_mapping[i] = date_obj
            previous_date_obj = date_obj

        # Extract events
        for i, cell in enumerate(date_cells):
            events = cell.find_parent('td').find_all('div', class_='ngCalendarDayEventItem')
            event_date = date_mapping[i]
            for event in events:
                # Extract the event time (start and end)
                start_time_str = event.find('span', class_='startDt').text.strip()
                end_time_str = event.find('span', class_='endDt').text.strip()

                # Combine date with time and parse to datetime
                start_time = datetime.datetime.strptime(f"{event_date.strftime('%Y-%m-%d')} {start_time_str}", "%Y-%m-%d %I:%M %p")
                end_time = datetime.datetime.strptime(f"{event_date.strftime('%Y-%m-%d')} {end_time_str}", "%Y-%m-%d %I:%M %p")

                # Extract the event title
                event_name = event.find('div', class_='s25-item-name').text.strip()

                # Extract the courts (subject)
                courts = event.find_all('div', class_='ngSubjectCalCellText')
                courts_list = [court.text.strip() for court in courts]

                # Create and save the Event instance
                event_obj = Event(
                    name=event_name,
                    start_time=start_time,
                    end_time=end_time,
                    courts=', '.join(courts_list)
                )
                event_obj.save()

                print(f"Event: {event_name}")
                print(f"Time: {start_time} - {end_time}")
                print(f"Courts: {', '.join(courts_list)}\n")

        self.stdout.write(self.style.SUCCESS('Successfully scraped events and updated the database.'))

