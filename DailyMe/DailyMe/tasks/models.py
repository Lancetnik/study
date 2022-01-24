from django.conf import settings
from django.db import models


class Task(models.Model):
    text = models.TextField()
    onwer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    def __str__(self):
        return f'{self.onwer}: {self.text}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskCategory(models.Model):
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,
        related_name='category'
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    is_fault = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task}: с {self.start_date} по {self.end_date}'

    class Meta:
        verbose_name = 'Задача к выполнению'
        verbose_name_plural = 'Задачи к выполнению'

        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F('end_date')),
                name='start_lt_end'
            ),
            models.CheckConstraint(
                check=\
                    models.Q(is_closed=False, is_fault=False) | \
                    models.Q(is_closed=True, is_fault=False) | \
                    models.Q(is_closed=True, is_fault=True),
                name='wrong_fault'
            ),
        ]


class RegularTask(models.Model):
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,
        related_name='regular'
    )
    cron_format = models.TextField()

    def __str__(self):
        return f'Регулярная - {self.task}'

    class Meta:
        verbose_name = 'Регулярная задача'
        verbose_name_plural = 'Регулярные задачи'
