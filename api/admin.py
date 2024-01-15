from django.contrib import admin

from api.models import User


# Register your models here.
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('phone', 'telegram_id', 'login_status',)
