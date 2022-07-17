from django.urls import path

from predictions.views import (
    home,
    SeasonDetailView,
    SeasonListView,
    TournamentDetailView,
)


app_name = "predictions"
urlpatterns = [
    path("", home, name="home"),
    path(
        "season/<int:pk>/",
        SeasonDetailView.as_view(),
        name="season_detail"
    ),
    path("season/", SeasonListView.as_view(), name="season_list"),
    path(
        "tournament/<int:pk>/",
        TournamentDetailView.as_view(),
        name="tournament_detail"
    ),
]
