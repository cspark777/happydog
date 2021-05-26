from django.core.management.base import BaseCommand
import random
from datetime import datetime, date, timedelta
from boarding.models import Dateinyear, Dog
# python manage.py seed --mode=refresh

class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self)
        self.stdout.write('done.')

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def run_seed(self):
    usa_national_holidays = [
        (date(2021, 1, 1), date(2021, 1, 3)), # January 1 : new year
        (date(2021, 1, 18), date(2021, 1, 22)), # January 20 : Inauguration Day        
        (date(2021, 2, 15), date(2021, 1, 19)), # George Washington’s Birthday
        (date(2021, 5, 29), date(2021, 6, 2)), # Memorial Day
        (date(2021, 7, 2), date(2021, 7, 6)), # Independence Day
        (date(2021, 9, 4), date(2021, 9, 8)), # Labor Day
        (date(2021, 10, 9), date(2021, 10, 13)), # Columbus Day
        (date(2021, 11, 9), date(2021, 11, 13)), # Veterans Day
        (date(2021, 11, 23), date(2021, 11, 27)), # Thanksgiving Day
        (date(2021, 12, 23), date(2021, 12, 27)), # Christmas Day
        (date(2021, 12, 30), date(2021, 12, 31)), # new year
    ]

    start_date = date(2021, 1, 1)
    end_date = date(2022, 1, 1)
    for single_date in daterange(start_date, end_date):

        is_holiday = False
        for holiday in usa_national_holidays:
            if single_date>=holiday[0] and single_date<=holiday[1]:
                is_holiday = True
                break

        week_day = single_date.weekday()

        is_weekend = week_day==4 or week_day==5

        weight = 1
        if is_weekend:
            weight = 5
        elif is_holiday:
            weight = 3

        print(single_date, is_holiday, is_weekend)
        
        date1 = Dateinyear(
            date=single_date,
            is_weekend=is_weekend,
            is_holiday=is_holiday,
            weight=weight
        )

        date1.save()

    print("init 10 dogs")
    init_dog_first_names = ["Marry", "Jim", "Bella", "Axel", "Alyssa", "Albert", "Ariel", "Jasmine", "King", "Max"]
    init_dog_last_name = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

    for i in range(10):
        dog1 = Dog(first_name=init_dog_first_names[i], last_name=init_dog_last_name[i])
        dog1.save()