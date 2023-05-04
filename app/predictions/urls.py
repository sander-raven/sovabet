from django.urls import path

from predictions.views import (
    GameDetailView,
    SeasonDetailView,
    SeasonListView,
    TournamentDetailView,
    TournamentListView,
    home_view,
)


app_name = "predictions"
urlpatterns = [
    path("", home_view, name="home"),
    path(
        "season/<str:pk>/",
        SeasonDetailView.as_view(),
        name="season_detail"
    ),
    path("season/", SeasonListView.as_view(), name="season_list"),
    path(
        "tournament/<str:pk>/",
        TournamentDetailView.as_view(),
        name="tournament_detail"
    ),
    path("tournament/", TournamentListView.as_view(), name="tournament_list"),
    path(
        "game/<str:pk>/",
        GameDetailView.as_view(),
        name="game_detail"
    ),
]
