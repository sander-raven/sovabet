import csv
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from import_export import resources
from import_export.admin import ImportExportMixin

from predictions.logic import (
    calculate_game_predictions,
    calculate_prediction,
    calculate_tournament_predictions,
    get_predictors_comments,
    process_raw_predictions,
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
    RawPrediction,
    Season,
    Team,
    Tournament,
)


admin.site.site_header = "Административный сайт SOVABET"
admin.site.site_title = "SOVABET"
admin.site.index_title = "Администрирование SOVABET"


# Admin actions

@admin.action(description="Сделать выбранные записи активными")
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
    modeladmin.message_user(request, 'Выбранные записи сделаны активными')


@admin.action(description="Сделать выбранные записи неактивными")
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
    modeladmin.message_user(request, 'Выбранные записи сделаны неактивными')


@admin.action(description="Обработать выбранные сырые прогнозы")
def process_selected_raw_predictions(modeladmin, request, queryset):
    successful, total = process_raw_predictions(queryset)
    modeladmin.message_user(
        request, f"Создано прогнозов: {successful} из {total}"
    )


@admin.action(
    description="Собрать и сохранить в csv комментарии для выбранных игр"
)
def create_csv_from_vk(modeladmin, request, queryset):
    filename = f"comments_from_vk_{int(datetime.utcnow().timestamp())}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={filename}"

    output = get_predictors_comments(queryset.order_by("started_at"))

    writer = csv.writer(response)
    for line in output:
        writer.writerow(line)

    return response


# Mixins

class ActiveFilterAdminMixin:
    active_filter = {}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in self.active_filter:
            model = self.active_filter.get(db_field.name)
            if model:
                try:
                    kwargs["queryset"] = model.objects.filter(is_active=True)
                except AttributeError:  # as error:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Model resources

class BaseAbstractResource(resources.ModelResource):

    class Meta:
        abstract = True
        skip_unchanged = True
        report_skipped = True


class TournamentResource(BaseAbstractResource):

    class Meta:
        model = Tournament
        fields = ("id", "name", "info", "season")


class TeamResource(BaseAbstractResource):

    class Meta:
        model = Team
        fields = ("id", "name", "info")


class GameResource(BaseAbstractResource):

    class Meta:
        model = Game
        fields = ("id", "name", "info", "tournament", "vk_post_id")


class PredictorResource(BaseAbstractResource):

    class Meta:
        model = Predictor
        fields = ("id", "name", "info", "vk_id")


class RawPredictionResource(BaseAbstractResource):
    text = resources.Field(
        attribute="text",
        column_name="text",
        widget=resources.widgets.CharWidget(),
        default="",
    )
    winner = resources.Field(
        attribute="winner",
        column_name="winner",
        widget=resources.widgets.CharWidget(),
        default="",
    )
    runner_up = resources.Field(
        attribute="runner_up",
        column_name="runner_up",
        widget=resources.widgets.CharWidget(),
        default="",
    )
    third_place = resources.Field(
        attribute="third_place",
        column_name="third_place",
        widget=resources.widgets.CharWidget(),
        default="",
    )
    note = resources.Field(
        attribute="note",
        column_name="note",
        widget=resources.widgets.CharWidget(),
        default="",
    )

    class Meta:
        model = RawPrediction


# Admin models

class BaseAbstractAdmin(ActiveFilterAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "id", "is_active")
    list_display_links = ("__str__", "id")
    list_editable = ("is_active", )
    search_fields = ("id", "name", "info")
    fields = ("id", "name", "info", "is_active", "created_at", "updated_at")
    readonly_fields = ("id", "created_at", "updated_at")
    actions = (make_active, make_inactive)

    class Meta:
        abstract = True


class StartedAtAdmin(BaseAbstractAdmin):
    list_display = ("__str__", "started_at", "id", "is_active")
    list_display_links = ("__str__", "started_at", "id")
    fields = (
        "id",
        "name",
        "info",
        "started_at",
        "is_active",
        "created_at",
        "updated_at",
    )
    ordering = ("-started_at", )

    class Meta:
        abstract = True


@admin.register(Season)
class SeasonAdmin(StartedAtAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(ImportExportMixin, StartedAtAdmin):
    list_display = ("__str__", "started_at", "id", "season", "is_active")
    search_fields = ("id", "name", "info", "season__name", "season__info")
    fields = (
        "id",
        "name",
        "info",
        "season",
        "started_at",
        "is_active",
        "created_at",
        "updated_at",
    )
    active_filter = {
        "season": Season,
    }
    resource_class = TournamentResource
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


@admin.register(Team)
class TeamAdmin(ImportExportMixin, BaseAbstractAdmin):
    resource_class = TeamResource


class PerformanceInLine(ActiveFilterAdminMixin, admin.TabularInline):
    model = Performance
    fields = ("team", "result")
    active_filter = {
        "team": Team,
    }


@admin.register(Game)
class GameAdmin(ImportExportMixin, StartedAtAdmin):
    search_fields = (
        "id", "name", "info", "tournament__name", "tournament__info"
    )
    list_display = ("__str__", "started_at", "id", "vk_post_id", "is_active")
    fields = (
        "id",
        "name",
        "info",
        "vk_post_id",
        "tournament",
        "started_at",
        "is_active",
        "created_at",
        "updated_at",
    )
    active_filter = {
        "tournament": Tournament,
    }
    inlines = (PerformanceInLine, )
    resource_class = GameResource
    change_form_template = "predictions/game_changeform.html"
    actions = (make_active, make_inactive, create_csv_from_vk)

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


@admin.register(Predictor)
class PredictorAdmin(ImportExportMixin, BaseAbstractAdmin):
    list_display = ("__str__", "id", "vk_id", "is_active")
    search_fields = ("id", "name", "info", "vk_id")
    fields = (
        "id",
        "name",
        "info",
        "vk_id",
        "is_active",
        "created_at",
        "updated_at",
    )
    resource_class = PredictorResource


class PredictionEventInline(admin.TabularInline):
    model = PredictionEvent
    fields = ("team", "result", "points")
    max_num = 3
    readonly_fields = ("points", )


@admin.register(Prediction)
class PredictionAdmin(ActiveFilterAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "id", "datetime", "total_points", "is_active")
    search_fields = ("predictor__name", "game__name")
    fields = (
        "predictor",
        "game",
        "datetime",
        "total_points",
        "winners",
        "runners_up",
        "third_places",
        "prize_winners",
        "is_active",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "total_points",
        "winners",
        "runners_up",
        "third_places",
        "prize_winners",
        "created_at",
        "updated_at",
    )
    active_filter = {
        "predictor": Predictor,
        "game": Game,
    }
    inlines = (PredictionEventInline, )
    ordering = ("-datetime", "-created_at")
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


@admin.register(RawPrediction)
class RawPredictionAdmin(
    ImportExportMixin, ActiveFilterAdminMixin, admin.ModelAdmin
):
    list_display = (
        "name",
        "game",
        "winner",
        "runner_up",
        "third_place",
        "note",
        "is_active",
    )
    list_display_links = (
        "name",
        "game",
        "winner",
        "runner_up",
        "third_place",
        "note",
    )
    search_fields = (
        "name",
        "game",
        "winner",
        "runner_up",
        "third_place",
        "note",
        "text",
        "vk_id",
    )
    fieldsets = (
        ("Информация о записи", {
            "fields": ("id", "created_at", "updated_at", "is_active")
        }),
        ("Информация о прогнозисте", {
            "fields": ("name", "vk_id")
        }),
        ("Информация о прогнозе", {
            "fields": (
                "timestamp",
                "text",
                "game",
                "winner",
                "runner_up",
                "third_place",
                "note",
            )
        }),
    )
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at", )
    resource_class = RawPredictionResource
    actions = (make_active, make_inactive, process_selected_raw_predictions)
    # change_list_template = "predictions/rawpredictions_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("process/", self.process_raw_predictions),
        ]
        return extra_urls + urls

    def process_raw_predictions(self, request):
        successful, total = process_raw_predictions()
        self.message_user(
            request, f"Создано прогнозов: {successful} из {total}"
        )
        return HttpResponseRedirect("../")
