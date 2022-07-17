from django.urls import path

from predictions.views import TournamentDetailView, home

app_name = "predictions"
urlpatterns = [
    path("", home, name="home"),
    path(
        "tournament/<int:pk>",
        TournamentDetailView.as_view(),
        name="tournament_detail"
    ),
]
