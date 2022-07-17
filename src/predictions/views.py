from typing import Any, Dict

from django.db.models.aggregates import Count, Sum
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from predictions.models import Prediction, Season, Tournament


def home(request):
    tournament = Tournament.objects.filter(is_active=True).first()
    return redirect(tournament)


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
        return context
