from django.db import models


class Timestamp(models.Model):
    created_at = models.DateTimeField("создание", auto_now_add=True)
    modified_at = models.DateTimeField("изменение", auto_now=True)

    class Meta:
        abstract = True


class Active(Timestamp):
    is_active = models.BooleanField("актив?", default=True)

    class Meta:
        abstract = True


class CommonInfo(Active):
    name = models.CharField("название", max_length=50, unique=True)
    info = models.TextField("информация", blank=True)

    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        return self.name


class Season(CommonInfo):

    class Meta:
        verbose_name = "сезон"
        verbose_name_plural = "сезоны"


class Tournament(CommonInfo):
    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        related_name="tournaments",
        verbose_name="сезон",
    )

    class Meta:
        verbose_name = "турнир"
        verbose_name_plural = "турниры"


class Team(CommonInfo):

    class Meta:
        verbose_name = "команда"
        verbose_name_plural = "команды"
        ordering = ["name"]


class Result(CommonInfo):

    class Meta:
        verbose_name = "результат"
        verbose_name_plural = "результаты"
        ordering = ["name"]


class Game(CommonInfo):
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


class Performance(models.Model):
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
    result = models.ForeignKey(
        Result,
        on_delete=models.PROTECT,
        verbose_name="результат",
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


class Predictor(CommonInfo):
    vk_id = models.CharField("VK ID", max_length=50, blank=True)

    class Meta:
        verbose_name = "прогнозист"
        verbose_name_plural = "прогнозисты"
        ordering = ["name"]


class Prediction(Active):
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

    class Meta:
        verbose_name = "прогноз"
        verbose_name_plural = "прогнозы"
    
    def __str__(self) -> str:
        return f"Прогноз {self.predictor} на игру {self.game}"


class PredictionEvent(Timestamp):
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
    result = models.ForeignKey(
        Result,
        on_delete=models.PROTECT,
        verbose_name="результат",
    )
    points = models.FloatField("баллы", default=0.0)

    class Meta:
        verbose_name = "событие прогноза"
        verbose_name_plural = "события прогноза"
    
    def __str__(self) -> str:
        return f"{self.team} >> {self.result}"
