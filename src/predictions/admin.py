from django.contrib import admin

from .models import Season, Tournament


class SeasonAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active")
    search_fields = ("title", "info")
    fields = ("title", "info", "is_active")


admin.site.register(Season, SeasonAdmin)


class TournamentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "season", "is_active")
    search_fields = ("title", "info", "season__title", "season__info")
    fields = ("title", "info", "is_active", "season")


admin.site.register(Tournament, TournamentAdmin)
