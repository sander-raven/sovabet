"""Application Business Logic."""


from enum import Enum

from django.db.models.aggregates import Sum
from django.db.models.query import QuerySet

from predictions.models import (
    Game,
    Performance,
    Prediction,
    PredictionEvent,
)


class PointsForPredictionEvent(Enum):
    WINNER_MATCHED = 4
    RUNNER_UP_MATCHED = 3
    THIRD_PLACE_MATCHED = 3
    TEAM_WAS_AWARDED = 2
    NO_MATCHES = 0


def get_not_null_performances_for_game(game: Game) -> QuerySet[Performance]:
    """Returns queryset with Performance instances
    that have a non-empty result field.
    """
    performances = Performance.objects.filter(
        game=game, result__isnull=False
    ).order_by("result")
    return performances


def get_game_predictions(game: Game) -> QuerySet[Prediction]:
    """Returns queryset with active Prediction instances."""
    predictions = Prediction.objects.filter(
        game=game, is_active=True
    )
    return predictions


def get_prediction_events(prediction: Prediction) -> QuerySet[PredictionEvent]:
    """Returns queryset with PredictionEvent instances for prediction."""
    prediction_events = PredictionEvent.objects.filter(
        prediction=prediction
    ).order_by("result")
    return prediction_events


def calculate_total_points_for_prediction(
    prediction: Prediction, prediction_events: PredictionEvent = None
) -> None:
    """Fills in total_points of prediction and saves it."""
    if not prediction_events:
        prediction_events = get_prediction_events(prediction)
    total_points = prediction_events.aggregate(Sum("points"))
    prediction.total_points = total_points["points__sum"]
    prediction.save()
