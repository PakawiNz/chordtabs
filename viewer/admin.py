from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from viewer.models import User, Song


class UserAdmin(admin.ModelAdmin):
    field = ('username', 'password',)
    list_display = ('username', 'displayname',)


class SongHasImageFilter(SimpleListFilter):
    title = 'Has Image?'
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        return [
            ('YES', 'YES'),
            ('NO', 'NO'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'YES':
            return queryset.exclude(chord_image='')
        elif self.value() == 'NO':
            return queryset.filter(chord_image='')
        else:
            return queryset


class SongAdmin(admin.ModelAdmin):
    list_filter = (SongHasImageFilter,)
    list_display = ('code', 'description', 'chord_image',)
    search_fields = ('description',)


admin.site.register(User, UserAdmin)
admin.site.register(Song, SongAdmin)
