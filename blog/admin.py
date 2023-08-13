from django.contrib import admin

from blog import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-id', 'name')


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author')
    list_filter = ('category',)
    search_fields = ('title', 'body')
    ordering = ('-create_at', '-update_at')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'create_at', 'active')
    list_filter = ('create_at', 'active')
    search_fields = ('post', 'author', 'body')


@admin.register(models.PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_filter = ('create_at',)
    search_fields = ('user', 'post')


@admin.register(models.PostDislike)
class PostDislikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_filter = ('create_at',)
    search_fields = ('user', 'post')

@admin.register(models.CommentLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment')
    list_filter = ('create_at',)
    search_fields = ('user', 'comment')


@admin.register(models.CommentDislike)
class PostDislikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment')
    list_filter = ('create_at',)
    search_fields = ('user', 'comment')

