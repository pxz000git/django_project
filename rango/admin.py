from django.contrib import admin

from rango.models import Category, Page, UserProfile


class CategoryAdmin(admin.ModelAdmin):
    # fields = ['name', 'views', 'likes']
    list_display = ['name', 'views', 'likes']
    prepopulated_fields = {'slug': ('name',)}


class PageAdmin(admin.ModelAdmin):
    # fields = ['category', 'title', 'url']
    list_display = ['category', 'title', 'url']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
