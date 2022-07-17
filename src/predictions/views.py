from typing import Any, Dict

from django.db.models.aggregates import Count, Sum
from django.views.generic import DetailView

from predictions.models import Prediction, Tournament


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "predictions/tournament_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tournament_table = Prediction.objects\
            .filter(game__tournament=self.object)\
            .values("predictor__id", "predictor__name", "predictor__vk_id")\
            .annotate(cnt=Count("pk"), sum_pts=Sum("total_points"))\
            .order_by("-sum_pts", "cnt", "predictor__name")
        context["tournament_table"] = tournament_table
        return context
