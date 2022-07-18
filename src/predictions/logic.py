"""Application Business Logic."""


from collections import namedtuple
from enum import Enum

from django.db.models.query import QuerySet

from predictions.models import (
    Game,
    Performance,
    Prediction,
    PredictionEvent,
    Season,
    Tournament,
)


# Helper classes

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


# Get different querysets

def get_season_tournaments(
    season: Season, is_active: bool | None = None
) -> QuerySet[Tournament]:
    """Returns a queryset with Tournament instances for the season.

    If is_active is:
        - None - returns a queryset without a filter.
        - True - returns a queryset with active records.
        - False - returns a queryset with inactive records.
    """
    if is_active is None:
        tournaments = Tournament.objects.filter(season=season)
    else:
        tournaments = Tournament.objects.filter(
            season=season, is_active=is_active
        )
    return tournaments


def get_tournament_games(
    tournament: Tournament, is_active: bool | None = None
) -> QuerySet[Game]:
    """Returns a queryset with Game instances for the tournament.

    If is_active is:
        - None - returns a queryset without a filter.
        - True - returns a queryset with active records.
        - False - returns a queryset with inactive records.
    """
    if is_active is None:
        games = Game.objects.filter(tournament=tournament)
    else:
        games = Game.objects.filter(
            tournament=tournament, is_active=is_active
        )
    return games


def get_game_predictions(
    game: Game, is_active: bool | None = None
) -> QuerySet[Prediction]:
    """Returns a queryset with Prediction instances for the game.

    If is_active is:
        - None - returns a queryset without a filter.
        - True - returns a queryset with active records.
        - False - returns a queryset with inactive records.
    """
    if is_active is None:
        predictions = Prediction.objects.filter(game=game)
    else:
        predictions = Prediction.objects.filter(
            game=game, is_active=is_active
        )
    return predictions


def get_prediction_events(prediction: Prediction) -> QuerySet[PredictionEvent]:
    """Returns a queryset with PredictionEvent instances
    for the prediction.
    """
    prediction_events = PredictionEvent.objects.filter(
        prediction=prediction
    ).order_by("result")
    return prediction_events


def get_not_null_performances_for_game(game: Game) -> QuerySet[Performance]:
    """Returns a queryset with Performance instances
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


# Results manipulation

def save_prediction_results(
    prediction: Prediction,
    prediction_results: dict[str | int, float | int] = {},
) -> None:
    prediction.total_points = prediction_results.get("total_points", 0.0)
    prediction.winners = prediction_results.get(1, 0)
    prediction.runners_up = prediction_results.get(2, 0)
    prediction.third_places = prediction_results.get(3, 0)
    prediction.prize_winners = prediction_results.get("prize_winners", 0)
    prediction.save()


def calculate_prediction(
    prediction: Prediction, ranked_performances: RankedPerformances = None
) -> None:
    if not ranked_performances:
        performances = get_not_null_performances_for_game(prediction.game)
        ranked_performances = get_ranked_performances(performances)
    
    prediction_events = get_prediction_events(prediction)
    events = [
        event for event in prediction_events
    ]
    for event in events:
        event.points = Points.NO_MATCHES.value

    prediction_results = {
        "total_points": 0.0,
        1: 0,
        2: 0,
        3: 0,
        "prize_winners": 0,
    }

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
                prediction_results["total_points"] += full_hit[0].points
                prediction_results[performance.result.pk] += 1
            else:
                prizes_hit = [
                    event for event in events
                    if event.team==performance.team
                ]
                if prizes_hit:
                    prizes_hit[0].points = Points.TEAM_WAS_AWARDED.value
                    prediction_results["total_points"] += prizes_hit[0].points
                    prediction_results["prize_winners"] += 1

    for event in events:
        event.save()

    save_prediction_results(prediction, prediction_results)


def calculate_game_predictions(game: Game) -> None:
    performances = get_not_null_performances_for_game(game)
    ranked_performances = get_ranked_performances(performances)
    predictions = get_game_predictions(game, is_active=True)

    for prediction in predictions:
        calculate_prediction(prediction, ranked_performances)


def reset_prediction(prediction: Prediction) -> None:
    prediction_events = get_prediction_events(prediction)
    for event in prediction_events:
        event.points = Points.NO_MATCHES.value
        event.save()
    save_prediction_results(prediction)


def reset_game_predictions(game: Game) -> None:
    predictions = get_game_predictions(game, is_active=True)
    for prediction in predictions:
        reset_prediction(prediction)
