import uuid

from django.db import models
from django.urls import reverse


class Result(models.IntegerChoices):
    WINNER = 1, "Победитель"
    RUNNER_UP = 2, "Второй призёр"
    THIRD_PLACE = 3, "Третий призёр"


class BaseAbstractModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField("создание", auto_now_add=True)
    updated_at = models.DateTimeField("изменение", auto_now=True)
    is_active = models.BooleanField("актив?", default=True)

    class Meta:
        abstract = True
        ordering = ("-created_at", )


class GeneralInfoAbstractModel(BaseAbstractModel):
    name = models.CharField("название", max_length=50, unique=True)
    info = models.TextField("информация", blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class StartedAtAbstractModel(GeneralInfoAbstractModel):
    started_at = models.DateTimeField("начало", blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ("-started_at", )


class Season(StartedAtAbstractModel):

    class Meta:
        verbose_name = "сезон"
        verbose_name_plural = "сезоны"

    def get_absolute_url(self):
        return reverse(
            "predictions:season_detail", kwargs={"pk": self.pk}
        )


class Tournament(StartedAtAbstractModel):
    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        related_name="tournaments",
        verbose_name="сезон",
    )

    class Meta:
        verbose_name = "турнир"
        verbose_name_plural = "турниры"

    def get_absolute_url(self):
        return reverse(
            "predictions:tournament_detail", kwargs={"pk": self.pk}
        )


class Team(GeneralInfoAbstractModel):

    class Meta:
        verbose_name = "команда"
        verbose_name_plural = "команды"
        ordering = ("name", )


class Game(StartedAtAbstractModel):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.PROTECT,
        related_name="games",
        verbose_name="турнир",
    )
    teams = models.ManyToManyField(
        Team,
        related_name="games",
        verbose_name="команды",
        through="Performance",
    )

    class Meta:
        verbose_name = "игра"
        verbose_name_plural = "игры"

    def __str__(self) -> str:
        return f"{self.name} :: {self.tournament}"

    def get_absolute_url(self):
        return reverse(
            "predictions:game_detail", kwargs={"pk": self.pk}
        )


class Performance(BaseAbstractModel):
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        verbose_name="игра"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        verbose_name="команда"
    )
    result = models.IntegerField(
        verbose_name="результат",
        choices=Result.choices,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "выступление"
        verbose_name_plural = "выступления"

    def __str__(self) -> str:
        output = f"#{self.pk}. Команда {self.team} в игре {self.game}"
        if self.result:
            output += f". Результат - {self.result}"
        return output


class Predictor(GeneralInfoAbstractModel):
    name = models.CharField("имя", max_length=50)
    vk_id = models.IntegerField("VK ID", blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "прогнозист"
        verbose_name_plural = "прогнозисты"
        ordering = ("name", )


class Prediction(BaseAbstractModel):
    predictor = models.ForeignKey(
        Predictor,
        on_delete=models.CASCADE,
        related_name="predictions",
        verbose_name="прогнозист",
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="predictions",
        verbose_name="игра",
    )
    total_points = models.FloatField("сумма баллов", default=0.0)
    winners = models.IntegerField("угадано победителей", default=0)
    runners_up = models.IntegerField("угадано вторых призёров", default=0)
    third_places = models.IntegerField("угадано третьих призёров", default=0)
    prize_winners = models.IntegerField(
        "угадано попаданий в призёры", default=0
    )

    class Meta:
        verbose_name = "прогноз"
        verbose_name_plural = "прогнозы"

    def __str__(self) -> str:
        return f"Прогноз {self.predictor} на игру {self.game}"


class PredictionEvent(BaseAbstractModel):
    prediction = models.ForeignKey(
        Prediction,
        on_delete=models.CASCADE,
        related_name="prediction_events",
        verbose_name="прогноз",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="prediction_events",
        verbose_name="команда",
    )
    result = models.IntegerField(
        verbose_name="результат",
        choices=Result.choices,
    )
    points = models.FloatField("баллы", default=0.0)

    class Meta:
        verbose_name = "событие прогноза"
        verbose_name_plural = "события прогноза"

    def __str__(self) -> str:
        return f"{self.team} >> {self.result}"


class RawPrediction(BaseAbstractModel):
    """Raw prediction to be processed further."""
    name = models.CharField("имя", max_length=50)
    vk_id = models.IntegerField("VK ID", blank=True, null=True)
    timestamp = models.FloatField(
        "метка времени", blank=True, null=True
    )
    text = models.TextField("текст", blank=True)
    game = models.CharField("игра", max_length=50)
    winner = models.CharField("победитель", max_length=50, blank=True)
    runner_up = models.CharField("второй призёр", max_length=50, blank=True)
    third_place = models.CharField("третий призёр", max_length=50, blank=True)
    note = models.TextField("примечание", blank=True)

    class Meta:
        verbose_name = "сырой прогноз"
        verbose_name_plural = "сырые прогнозы"
    
    def __str__(self) -> str:
        return f"Сырой прогноз {self.name} на игру {self.game}"
