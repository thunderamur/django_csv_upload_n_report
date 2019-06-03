import csv
import datetime
import random

numdays = 30
base = datetime.datetime.today() - datetime.timedelta(days=numdays)
date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]


def csv_dict_writer(path):
    with open(path, "w", newline='') as out_file:
        writer = csv.writer(out_file, delimiter=';')
        for date in date_list:
            for i in range(10000):
                row = [date.strftime('%Y-%m-%d'), i, random.randint(4, 12)]
                writer.writerow(row)


if __name__ == "__main__":
    path = "big_data.csv"
    csv_dict_writer(path)
