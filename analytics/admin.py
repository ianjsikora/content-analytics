from django.contrib import admin
from models import *

class ContentAdmin(admin.ModelAdmin):
    fields = []


admin.site.register(Content, ContentAdmin)
