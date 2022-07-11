from django.db import models


class Timestamp(models.Model):
    created_at = models.DateTimeField("создание", auto_now_add=True)
    modified_at = models.DateTimeField("изменение", auto_now=True)

    class Meta:
        abstract = True


class CommonInfo(Timestamp):
    name = models.CharField("название", max_length=50, unique=True)
    info = models.TextField("информация", blank=True)
    is_active = models.BooleanField("актив?", default=True)

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


class Game(CommonInfo):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.PROTECT,
        related_name="games",
        verbose_name="турнир",
    )

    class Meta:
        verbose_name = "игра"
        verbose_name_plural = "игры"
    
    def __str__(self) -> str:
        return f"{self.name} :: {self.tournament}"
