from typing import Any, Dict

from django.shortcuts import render
from django.views.generic import DetailView, ListView
from predictions.logic import (
    get_not_null_performances_for_game,
    get_season_tournaments,
    get_standings_for_object,
    get_tournament_games,
)

from predictions.models import Game, Season, Tournament


def home_view(request):
    tournaments = Tournament.objects.filter(is_active=True)\
        .select_related("season").values(
            "pk",
            "name",
            "info",
            "started_at",
            "season_id",
            "season__name",
    )
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
        standings = get_standings_for_object(self.object)
        context["standings"] = standings
        tournaments = get_season_tournaments(season=self.object)
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
        standings = get_standings_for_object(self.object)
        context["standings"] = standings
        games = get_tournament_games(tournament=self.object)
        context["games"] = games
        return context


class GameDetailView(DetailView):
    model = Game
    template_name = "predictions/game_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        standings = get_standings_for_object(self.object)
        context["standings"] = standings
        prize_performances = get_not_null_performances_for_game(self.object)
        context["prize_performances"] = prize_performances
        return context
