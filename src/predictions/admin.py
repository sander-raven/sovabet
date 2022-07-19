from django.contrib import admin
from django.http import HttpResponseRedirect
from import_export import resources
from import_export.admin import ImportExportMixin

from predictions.logic import (
    calculate_game_predictions,
    calculate_prediction,
    calculate_tournament_predictions,
    reset_game_predictions,
    reset_prediction,
    reset_tournament_predictions,
)
from predictions.models import (
    Game,
    Performance,
    Prediction,
    PredictionEvent,
    Predictor,
    Result,
    Season,
    Team,
    Tournament,
)


admin.site.site_header = "Административный сайт SOVABET"
admin.site.site_title = "SOVABET"
admin.site.index_title = "Администрирование SOVABET"


@admin.action(description="Сделать выбранные записи активными")
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
    modeladmin.message_user(request, 'Выбранные записи сделаны активными')


@admin.action(description="Сделать выбранные записи неактивными")
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
    modeladmin.message_user(request, 'Выбранные записи сделаны неактивными')


class ActiveFilterAdminMixin:
    active_filter = {}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in self.active_filter:
            model = self.active_filter.get(db_field.name)
            if model:
                try:
                    kwargs["queryset"] = model.objects.filter(is_active=True)
                except AttributeError as error:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DefaultAdmin(ActiveFilterAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "id", "is_active")
    search_fields = ("name", "info")
    fields = ("name", "info", "is_active", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")
    actions = (make_active, make_inactive)

    class Meta:
        abstract = True


@admin.register(Season)
class SeasonAdmin(DefaultAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(DefaultAdmin):
    list_display = ("__str__", "id", "season", "is_active")
    search_fields = ("name", "info", "season__name", "season__info")
    fields = (
        "name", "info", "is_active", "season", "created_at", "modified_at"
    )
    active_filter = {
        "season": Season,
    }
    change_form_template = "predictions/tournament_changeform.html"

    def response_change(self, request, obj):
        if "_calculate" in request.POST:
            calculate_tournament_predictions(obj)
            self.message_user(
                request, "Результаты прогнозов на игры турнира рассчитаны."
            )
            return HttpResponseRedirect(".")
        if "_reset" in request.POST:
            reset_tournament_predictions(obj)
            self.message_user(
                request, "Результаты прогнозов на игры турнира сброшены."
            )
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class TeamResource(resources.ModelResource):

    class Meta:
        model = Team
        skip_unchanged = True
        report_skipped = True
        fields = ("id", "name", "info")


@admin.register(Team)
class TeamAdmin(ImportExportMixin, DefaultAdmin):
    resource_class = TeamResource


@admin.register(Result)
class ResultAdmin(DefaultAdmin):
    pass


class TeamInLine(ActiveFilterAdminMixin, admin.TabularInline):
    model = Performance
    active_filter = {
        "team": Team,
        "result": Result,
    }


@admin.register(Game)
class GameAdmin(DefaultAdmin):
    search_fields = (
        "name", "info", "id", "tournament__name", "tournament__name"
    )
    fields = (
        "name", "info", "is_active", "tournament", "created_at", "modified_at"
    )
    active_filter = {
        "tournament": Tournament,
    }
    inlines = (TeamInLine, )
    change_form_template = "predictions/game_changeform.html"

    def response_change(self, request, obj):
        if "_calculate" in request.POST:
            calculate_game_predictions(obj)
            self.message_user(
                request, "Результаты прогнозов на игру рассчитаны."
            )
            return HttpResponseRedirect(".")
        if "_reset" in request.POST:
            reset_game_predictions(obj)
            self.message_user(
                request, "Результаты прогнозов на игру сброшены."
            )
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class PredictorResource(resources.ModelResource):

    class Meta:
        model = Predictor
        skip_unchanged = True
        report_skipped = True
        fields = ("id", "name", "vk_id", "info")


@admin.register(Predictor)
class PredictorAdmin(ImportExportMixin, DefaultAdmin):
    list_display = ("__str__", "id", "vk_id", "is_active")
    search_fields = ("name", "info", "vk_id")
    fields = (
        "name", "info", "vk_id", "is_active", "created_at", "modified_at"
    )
    resource_class = PredictorResource


class PredictionEventInline(admin.TabularInline):
    model = PredictionEvent
    max_num = 3
    readonly_fields = ("points", )

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(PredictionEventInline, self).get_formset(
            request, obj, **kwargs
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "team":
            if self.parent_obj and self.parent_obj.game:
                kwargs["queryset"] = Team.objects.filter(
                    games=self.parent_obj.game
                )
            else:
                kwargs["queryset"] = Team.objects.none()
        if db_field.name == "result":
            kwargs["queryset"] = Result.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Prediction)
class PredictionAdmin(ActiveFilterAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "id", "total_points", "is_active")
    search_fields = ("predictor__name", "game__name")
    fields = (
        "predictor",
        "game",
        "total_points",
        "winners",
        "runners_up",
        "third_places",
        "prize_winners",
        "is_active",
        "created_at",
        "modified_at",
    )
    readonly_fields = (
        "total_points",
        "winners",
        "runners_up",
        "third_places",
        "prize_winners",
        "created_at",
        "modified_at",
    )
    active_filter = {
        "predictor": Predictor,
        "game": Game,
    }
    inlines = (PredictionEventInline, )
    actions = (make_active, make_inactive)
    change_form_template = "predictions/prediction_changeform.html"

    def response_change(self, request, obj):
        if "_calculate" in request.POST:
            calculate_prediction(obj)
            self.message_user(request, "Результаты прогноза рассчитаны.")
            return HttpResponseRedirect(".")
        if "_reset" in request.POST:
            reset_prediction(obj)
            self.message_user(request, "Результаты прогноза сброшены.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
