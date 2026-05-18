from django.contrib import admin
from .models import Author, Category, Tag, Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author', 'category')
    list_display_links = ('title',)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)