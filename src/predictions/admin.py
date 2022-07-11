from django.contrib import admin

from .models import (
    Event, PredictedEvent, PredictedRound, Predictor, Round, Season, Tournament
)


admin.site.site_header = "Административный сайт SOVABET"
admin.site.site_title = "SOVABET"
admin.site.index_title = "Администрирование SOVABET"


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active")
    search_fields = ("title", "info")
    fields = ("title", "info", "is_active", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "season", "is_active")
    search_fields = ("title", "info", "season__title", "season__info")
    fields = (
        "title", "info", "is_active", "season", "created_at", "modified_at"
    )
    readonly_fields = ("created_at", "modified_at")


class EventInline(admin.TabularInline):
    model = Event
    extra = 3
    max_num = 3


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active")
    search_fields = ("title", "info", "tournament__title", "tournament__info")
    fields = (
        "title", "info", "is_active", "tournament", "created_at", "modified_at"
    )
    readonly_fields = ("created_at", "modified_at")
    inlines = (EventInline, )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("__str__", "round")
    search_fields = ("description", "result")
    fields = ("description", "result", "round", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")


@admin.register(Predictor)
class PredictorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id", "vk_id")
    search_fields = ("name", )
    fields = ("name", "vk_id", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")


class PredictedEventInline(admin.TabularInline):
    model = PredictedEvent
    extra = 3
    max_num = 3


@admin.register(PredictedRound)
class PredictedRoundAdmin(admin.ModelAdmin):
    list_display = ("__str__", )
    fields = (
        "predictor", "round", "total_points", "created_at", "modified_at"
    )
    readonly_fields = ("total_points", "created_at", "modified_at")
    inlines = (PredictedEventInline, )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "round":
            kwargs["queryset"] = Round.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PredictedEvent)
class PredictedEventAdmin(admin.ModelAdmin):
    list_display = ("__str__", "predicted_round")
    search_fields = ("description", "result")
    fields = (
        "description", "result", "predicted_round", "created_at", "modified_at"
    )
    readonly_fields = ("created_at", "modified_at")
