from django.contrib import admin

from viewer.models import User, Song


class UserAdmin(admin.ModelAdmin):
    field = ('username', 'password')


class SongAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'chord_image',)
    search_fields = ('description',)


admin.site.register(User, UserAdmin)
admin.site.register(Song, SongAdmin)
