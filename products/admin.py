from django.contrib import admin

from .models import Category, Product, File

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'Title', 'Parent', 'IsEnable', 'CreatedTime']
    list_filter = ['IsEnable', 'Parent']
    search_fields = ['Title']


class FileInlineAdmin(admin.StackedInline):
    model = File
    fields = ['id', 'Title', 'file', 'FileType', 'IsEnable']
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'Title', 'IsEnable', 'CreatedTime']
    list_filter = ['IsEnable']
    search_fields = ['Title']
    filter_horizontal = ['Category']
    inlines = [FileInlineAdmin]
