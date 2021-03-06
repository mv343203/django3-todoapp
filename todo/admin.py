from django.contrib import admin
from .models import Todo
# Register your models here.

#this helps customize the admin view
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )

admin.site.register(Todo, TodoAdmin)
