from django.contrib import admin
from tags import models

# Register your models here.


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']
