from typing import Any, Dict

from django.db.models.aggregates import Count, Sum
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from predictions.logic import get_not_null_performances_for_game

from predictions.models import Game, Prediction, Season, Tournament


def home_view(request):
    tournaments = Tournament.objects.filter(is_active=True)
    context = {"tournaments": tournaments}
    return render(request, "predictions/home.html", context)


class SeasonListView(ListView):
    model = Season
    template_name = "predictions/season_list.html"


class SeasonDetailView(DetailView):
    model = Season
    template_name = "predictions/season_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        standings = Prediction.objects\
            .filter(game__tournament__season=self.object)\
            .values("predictor__id", "predictor__name", "predictor__vk_id")\
            .annotate(
                count=Count("pk"),
                prize_winners=Sum("prize_winners"),
                third_places=Sum("third_places"),
                runners_up=Sum("runners_up"),
                winners=Sum("winners"),
                total_points=Sum("total_points"),
            ).order_by(
                "-total_points",
                "count",
                "-winners",
                "-runners_up",
                "-third_places",
                "-prize_winners",
                "predictor__name",
            )
        context["standings"] = standings
        tournaments = Tournament.objects.filter(season=self.object)
        context["tournaments"] = tournaments
        return context


class TournamentListView(ListView):
    model = Tournament
    template_name = "predictions/tournament_list.html"


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "predictions/tournament_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        standings = Prediction.objects\
            .filter(game__tournament=self.object)\
            .values("predictor__id", "predictor__name", "predictor__vk_id")\
            .annotate(
                count=Count("pk"),
                prize_winners=Sum("prize_winners"),
                third_places=Sum("third_places"),
                runners_up=Sum("runners_up"),
                winners=Sum("winners"),
                total_points=Sum("total_points"),
            ).order_by(
                "-total_points",
                "count",
                "-winners",
                "-runners_up",
                "-third_places",
                "-prize_winners",
                "predictor__name",
            )
        context["standings"] = standings
        games = Game.objects.filter(tournament=self.object)
        context["games"] = games
        return context


class GameDetailView(DetailView):
    model = Game
    template_name = "predictions/game_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        standings = Prediction.objects\
            .filter(game=self.object)\
            .values("predictor__id", "predictor__name", "predictor__vk_id")\
            .annotate(
                count=Count("pk"),
                prize_winners=Sum("prize_winners"),
                third_places=Sum("third_places"),
                runners_up=Sum("runners_up"),
                winners=Sum("winners"),
                total_points=Sum("total_points"),
            ).order_by(
                "-total_points",
                "count",
                "-winners",
                "-runners_up",
                "-third_places",
                "-prize_winners",
                "predictor__name",
            )
        context["standings"] = standings
        prize_performances = get_not_null_performances_for_game(self.object)
        context["prize_performances"] = prize_performances
        return context
