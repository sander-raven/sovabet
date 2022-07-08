from django.contrib import admin

from .models import Event, Predictor, Round, Season, Tournament


class SeasonAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active")
    search_fields = ("title", "info")
    fields = ("title", "info", "is_active", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")


admin.site.register(Season, SeasonAdmin)


class TournamentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "season", "is_active")
    search_fields = ("title", "info", "season__title", "season__info")
    fields = (
        "title", "info", "is_active", "season", "created_at", "modified_at"
    )
    readonly_fields = ("created_at", "modified_at")


admin.site.register(Tournament, TournamentAdmin)


class EventInline(admin.TabularInline):
    model = Event
    extra = 4
    max_num = 4


class RoundAdmin(admin.ModelAdmin):
    list_display = ("__str__", )
    search_fields = ("title", "info", "tournament__title", "tournament__info")
    fields = ("title", "info", "tournament", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")
    inlines = (EventInline, )


admin.site.register(Round, RoundAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ("__str__", "round")
    search_fields = ("description", "result")
    fields = ("description", "result", "round", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")


admin.site.register(Event, EventAdmin)


class PredictorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id", "vk_id")
    search_fields = ("name", )
    fields = ("name", "vk_id", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")


admin.site.register(Predictor, PredictorAdmin)
