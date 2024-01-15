from django.db import models


# Create your models here.

class User(models.Model):
    """Модель для хранения пользователей в БД."""

    STATUSES = {
        'waiting_qr_login': 'waiting',
        'error': 'error',
        'logined': 'logged',
        'logged_out': 'logged out'
    }

    phone = models.IntegerField(unique=True, verbose_name='Телефон')
    telegram_id = models.IntegerField(verbose_name='Айди телеграм-профиля', null=True, blank=True)
    login_status = models.CharField(
        max_length=16,
        choices=STATUSES,
        default='waiting_qr_login',
        verbose_name='Cтатус аутентификации'
    )
    qr_link = models.CharField(max_length=150, verbose_name='Ссылка для генерации QR-кода', null=True, blank=True)

    def __str__(self):
        return f'{self.phone}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
