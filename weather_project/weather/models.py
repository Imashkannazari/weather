from django.db import models
from django.utils import timezone

# Create your models here.

class ContactTicket(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ارسال')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f'تیکت از {self.name} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'
