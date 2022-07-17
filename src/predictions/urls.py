from django.urls import path

from predictions.views import TournamentDetailView

urlpatterns = [
    path(
        'tournament/<int:pk>',
        TournamentDetailView.as_view(),
        name="tournament_detail"
    ),
]
