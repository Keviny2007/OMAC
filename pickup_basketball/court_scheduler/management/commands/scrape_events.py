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
        url = 'https://25live.collegenet.com/pro/brown/embedded/calendar?comptype=calendar&compsubject=location&itemTypeId=4&queryId=548963&embeddedConfigToken=4C7BA58F-4540-4940-AF8D-25D1A23A3C00#!/home/event/482576/details'
        driver.get(url)
        time.sleep(10)
        html = driver.page_source
        driver.quit()

        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Clear the previous events in the database
        Event.objects.all().delete()

        # Extract the days of the week
        days_of_week = [th.text for th in soup.find('thead').find_all('th')]

        # Extract date cells
        date_cells = soup.find_all('div', class_='CalendarDayHeader')

        # Map dates to their corresponding days
        date_mapping = {}
        for i, cell in enumerate(date_cells):
            date_text = cell.find('a').text.strip()
            if i == 0:  # The first cell shows the full date (e.g., "September 22")
                date_obj = datetime.datetime.strptime(date_text, "%B %d")
            else:  # Subsequent cells only show the day (e.g., "23")
                date_obj = datetime.datetime.strptime(f"{date_mapping[0].month} {date_text} {datetime.datetime.now().year}", "%m %d %Y")
                date_obj = date_obj.replace(month=date_mapping[0].month)  # Keep the same month as the first

            date_mapping[i] = date_obj

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

