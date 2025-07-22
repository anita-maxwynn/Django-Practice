from django.contrib import admin
from .models import Profile, Result
# Register your models here.
admin.site.register(Result)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'roll', 'email', 'city')
    search_fields = ('name', 'roll')
    list_filter = ('city',)

admin.site.register(Profile, ProfileAdmin)