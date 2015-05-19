
from django.contrib import admin
from rango.models import Category,Page

class Pageadmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class Categoryadmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')
    prepopulated_fields = {'slug':('name', )}
admin.site.register(Category,Categoryadmin)
admin.site.register(Page,Pageadmin)

