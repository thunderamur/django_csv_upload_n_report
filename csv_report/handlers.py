import csv
import tempfile
from datetime import datetime
from django.db import transaction

from .models import WorkTime


def clear_db():
    WorkTime.objects.all().delete()


def load_file_to_db(file):
    """
    Load rows from file to DB.
    TODO: Need refactor
    """
    DATE = 0
    NAME = 1
    HOURS = 2

    file_temp = tempfile.NamedTemporaryFile()
    file_temp.write(file.read())
    file_temp.seek(0)
    with open(file_temp.name, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        with transaction.atomic():
            for row in reader:
                try:
                    d = datetime.strptime(row[DATE], '%Y-%m-%d')
                    n = row[NAME]
                    h = int(row[HOURS])
                except:
                    print(f'Error with row: {row}')
                    if row == ['date', 'name', 'hours']:
                        continue
                    else:
                        return row

                WorkTime.objects.create(
                    date=d,
                    name=n,
                    hours=h,
                )
    file_temp.close()


def get_report(begin, end):
    """
    Get rows for CSV.
    TODO: Need refactor
    :return: list
    """
    rows = {}
    for row in WorkTime.objects.filter(date__range=(begin, end)):
        if row.name in rows:
            rows[row.name].update({row.date.strftime('%s'): row.hours})
        else:
            rows.update({row.name: {row.date.strftime('%s'): row.hours}})

    dates = WorkTime.objects.filter(date__range=(begin, end)).order_by('date').values('date').distinct()
    date_keys = [date['date'].strftime('%s') for date in dates]
    date_headers = [date['date'].strftime('%Y-%m-%d') for date in dates]

    result = [
        ['name', *date_headers, 'sum_hours']
    ]
    for name in sorted(rows):
        row = [name]
        sum = 0
        for date in date_keys:
            if date in rows[name]:
                row.append(rows[name][date])
                sum += rows[name][date]
            else:
                row.append('-')
        row.append(sum)
        result.append(row)

    return result


class Echo:
    """
    Pseudo-buffer for csv.writer()
    """
    def write(self, value):
        return value
