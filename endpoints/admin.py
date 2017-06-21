from django.contrib import admin

# Register your models here.

from endpoints.models import App, UsedApp, AppSession

admin.site.register(App)
admin.site.register(UsedApp)
admin.site.register(AppSession)
