from django.urls import path

from . import views


app_name = 'csv_report'
urlpatterns = [
    path('', views.stat, name='stat'),
    path('stat/<status>/', views.stat, name='stat'),
    path('upload_csv/', views.upload_file, name='upload_csv'),
    path('report/', views.report, name='report'),
    path('get_csv/<begin>/<end>/', views.make_streaming_csv, name='get_csv'),
]
