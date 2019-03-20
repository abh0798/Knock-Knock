from django.contrib import admin
from .models import CustomUser, Questions, Event, Special

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Questions)
admin.site.register(Event)
admin.site.register(Special)