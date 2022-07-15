"""Application Business Logic."""


from collections import namedtuple
from enum import Enum

from django.db.models.aggregates import Sum
from django.db.models.query import QuerySet

from predictions.models import (
    Game,
    Performance,
    Prediction,
    PredictionEvent,
)


class Points(Enum):
    WINNER_MATCHED = 4
    RUNNER_UP_MATCHED = 3
    THIRD_PLACE_MATCHED = 3
    TEAM_WAS_AWARDED = 2
    NO_MATCHES = 0


RankedPerformances = namedtuple(
    "RankedPerformances",
    [
        "winner",
        "runner_up",
        "third_place",
    ]
)


def get_not_null_performances_for_game(game: Game) -> QuerySet[Performance]:
    """Returns queryset with Performance instances
    that have a non-empty result field.
    """
    performances = Performance.objects.filter(
        game=game, result__isnull=False
    ).order_by("result")
    return performances


def get_ranked_performances(
    performances: QuerySet[Performance]
) -> RankedPerformances:

    prep_performances = []

    # winner
    performance = performances.filter(result__id=1).first()
    prep_performances.append(
        {
            "performance": performance,
            "points": Points.WINNER_MATCHED.value,
        }
    )

    # runner up
    performance = performances.filter(result__id=2).first()
    prep_performances.append(
        {
            "performance": performance,
            "points": Points.RUNNER_UP_MATCHED.value,
        }
    )

    # third place
    performance = performances.filter(result__id=3).first()
    prep_performances.append(
        {
            "performance": performance,
            "points": Points.THIRD_PLACE_MATCHED.value,
        }
    )

    return RankedPerformances(*prep_performances)


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
    prediction: Prediction,
    prediction_events: QuerySet[PredictionEvent] = None,
) -> None:
    """Fills in total_points of prediction and saves it."""
    if not prediction_events:
        prediction_events = get_prediction_events(prediction)
    total_points = prediction_events.aggregate(Sum("points"))
    prediction.total_points = total_points["points__sum"]
    prediction.save()


def calculate_game_results(game: Game) -> None:
    performances = get_not_null_performances_for_game(game)
    ranked_performances = get_ranked_performances(performances)
    predictions = get_game_predictions(game)

    for prediction in predictions:
        prediction_events = get_prediction_events(prediction)
        events = [
            event for event in prediction_events
        ]
        for event in events:
            event.points = Points.NO_MATCHES.value

        for ranked_performance in ranked_performances:
            performance = ranked_performance.get("performance")
            if performance:
                full_hit = [
                    event for event in events
                    if event.result==performance.result and
                    event.team==performance.team
                ]
                if full_hit:
                    full_hit[0].points = ranked_performance.get("points")
                else:
                    prizes_hit = [
                        event for event in events
                        if event.team==performance.team
                    ]
                    if prizes_hit:
                        prizes_hit[0].points = Points.TEAM_WAS_AWARDED.value

        for event in events:
            event.save()

        calculate_total_points_for_prediction(prediction, prediction_events)
