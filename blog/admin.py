from django.contrib import admin
from .models import Post, Comment, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'tags')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author__username', 'body')
    actions = ['approve_comments', 'disable_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)
    approve_comments.short_description = 'Активувати вибрані коментарі'

    def disable_comments(self, request, queryset):
        queryset.update(is_active=False)
    disable_comments.short_description = 'Деактивувати вибрані коментарі'
