from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.urls import reverse

import csv

from .forms import UploadFileForm, DateRangeForm
from .handlers import load_file_to_db, clear_db, Echo, get_report
from .models import WorkTime


def stat(request, status=None):
    context = {}
    if status == 'loaded':
        context['status'] = status
    context['info'] = [
        ['Всего записей в журнале', WorkTime.objects.count()],
    ]
    context['menu'] = 'stat'
    return render_to_response('csv_report/stat.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            clear_db()
            load_file_to_db(request.FILES['file'])
            return HttpResponseRedirect(reverse('csv_report:stat', args=['loaded']))
    else:
        form = UploadFileForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    context['menu'] = 'upload'
    return render_to_response('csv_report/upload.html', context)


def report(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            begin = f'{request.POST["begin_year"]}-{request.POST["begin_month"]}-{request.POST["begin_day"]}'
            end = f'{request.POST["end_year"]}-{request.POST["end_month"]}-{request.POST["end_day"]}'

            return HttpResponseRedirect(reverse('csv_report:get_csv', args=[begin, end]))
    else:
        form = DateRangeForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    context['menu'] = 'report'
    return render_to_response('csv_report/report.html', context)


def make_streaming_csv(request, begin, end):
    rows = get_report(begin, end)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter=';')
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv",
    )
    response['Content-Disposition'] = 'attachment; filename="report.csv"'
    return response
