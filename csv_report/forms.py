from django import forms

import datetime


YEARS = range(datetime.date.today().year, datetime.date.today().year - 10, -1)


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='CSV-файл',
        widget=forms.FileInput(attrs={'accept': 'text/csv'}),
    )


class DateRangeForm(forms.Form):
    begin = forms.DateField(
        label='Дата начала выборки',
        widget=forms.SelectDateWidget(years=YEARS),
        initial=datetime.date.today(),
    )
    end = forms.DateField(
        label='Дата конца выборки',
        widget=forms.SelectDateWidget(years=YEARS),
        initial=datetime.date.today(),
    )
