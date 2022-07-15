from django.contrib import admin

# Register your models here.
from Books.models import Book, Author, Comment


class Author_admin(admin.ModelAdmin):
    list_display = ['name']


class AddbookAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'author',
        'price',
        'founded',
        'frontpic',
        'short_desc',
        'file'
    ]


class comment(admin.ModelAdmin):
    list_display = [
        'book',
        'content',
    ]


admin.site.register(Book, AddbookAdmin)
admin.site.register(Author, Author_admin)
admin.site.register(Comment, comment)
