from datetime import datetime, timedelta
import random
import csv

DATE_FMT = "%Y-%m-%d"
DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

def rand_reading():
    return random.randint(0, 10000) / 100.0

def create_test_data(total_steps=10):
    with open("testdata.csv", 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        date_col = datetime.now().strftime(DATE_FMT)
        for step in range(total_steps):
            timediff = timedelta(minutes=5*(total_steps - step))
            past = datetime.now() - timediff
            readings = [rand_reading() for _ in range(4)]
            spamwriter.writerow([date_col, past.strftime(DATETIME_FMT)] + readings)

if __name__ == "__main__":
    create_test_data()
