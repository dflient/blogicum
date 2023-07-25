from django.contrib import admin

from .models import Category, Comment, Location, Post


class PostInline(admin.TabularInline):
    model = Post
    extra = 0

class CommentInLine(admin.StackedInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    inlines = (
        CommentInLine,
    )
    list_display = (
        'title',
        'text',
        'author',
        'location',
        'category',
        'image',
        'is_published',
        'pub_date',
    )
    exclude = ('comment_count',)
    list_editable = (
        'location',
        'category',
        'is_published',
    )
    search_fields = ('title',)
    list_filter = (
        'category',
        'location',
        'is_published',
    )

class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'description',
    )

class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
    )

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
        'created_at',
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.empty_value_display = 'Не задано'
