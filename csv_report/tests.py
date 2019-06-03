from django.test import TestCase
from django.urls import reverse

from csv_report.models import WorkTime


class WorkTimeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        WorkTime.objects.create(date='2019-06-02', name='John Doe', hours=6)
        WorkTime.objects.create(date='2019-06-03', name='John Doe', hours=4)
        WorkTime.objects.create(date='2019-06-03', name='Foo Bar', hours=8)

    def test_model_str(self):
        row = WorkTime.objects.get(name='Foo Bar')
        expected = '2019-06-03;Foo Bar;8'
        result = str(row)
        self.assertEqual(expected, result)

    def test_stat(self):
        url = reverse('csv_report:stat')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['info'])
        self.assertEqual(response.context.get('menu'), 'stat')

    def test_upload_file(self):
        url = reverse('csv_report:upload_csv')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('menu'), 'upload')

    def test_report(self):
        url = reverse('csv_report:report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('menu'), 'report')

    def test_make_streaming_csv(self):
        url = reverse('csv_report:get_csv', args=['2019-06-02', '2019-06-03'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.serialize_headers(),
            b'Content-Type: text/csv\r\nContent-Disposition: attachment; filename="report.csv"\r\nX-Frame-Options: SAMEORIGIN',
        )

