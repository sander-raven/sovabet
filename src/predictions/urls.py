from django.urls import path

from predictions.views import SeasonDetailView, TournamentDetailView, home

app_name = "predictions"
urlpatterns = [
    path("", home, name="home"),
    path(
        "season/<int:pk>",
        SeasonDetailView.as_view(),
        name="season_detail"
    ),
    path(
        "tournament/<int:pk>",
        TournamentDetailView.as_view(),
        name="tournament_detail"
    ),
]
