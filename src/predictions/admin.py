from django.contrib import admin

from .models import Event, Round, Season, Tournament


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


class EventInline(admin.TabularInline):
    model = Event
    extra = 4
    max_num = 4


class RoundAdmin(admin.ModelAdmin):
    list_display = ("__str__", )
    search_fields = ("title", "info", "tournament__title", "tournament__info")
    fields = ("title", "info", "tournament")
    inlines = (EventInline, )


admin.site.register(Round, RoundAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ("__str__", "round")
    search_fields = ("description", "result")
    fields = ("description", "result", "round")


admin.site.register(Event, EventAdmin)
