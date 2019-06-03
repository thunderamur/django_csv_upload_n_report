from django.db import models


class WorkTime(models.Model):
    date = models.DateField('Дата')
    name = models.CharField('Имя сотрудника', max_length=50)
    hours = models.IntegerField('Отработано часов')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ('-date',)

    def __str__(self):
        return f'{self.date};{self.name};{self.hours}'
