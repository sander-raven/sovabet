from django.db import models


class Season(models.Model):
    title = models.CharField("заголовок", max_length=50, unique=True)
    info = models.TextField("информация", blank=True)
    is_active = models.BooleanField("действующий?", default=True)

    class Meta:
        verbose_name = "сезон"
        verbose_name_plural = "сезоны"
    
    def __str__(self) -> str:
        return self.title


class Tournament(models.Model):
    title = models.CharField("заголовок", max_length=50, unique=True)
    info = models.TextField("информация", blank=True)
    is_active = models.BooleanField("действующий?", default=True)
    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        related_name="tournaments",
        verbose_name="сезон",
    )

    class Meta:
        verbose_name = "турнир"
        verbose_name_plural = "турниры"
    
    def __str__(self) -> str:
        return self.title


class Round(models.Model):
    title = models.CharField("заголовок", max_length=50)
    info = models.TextField("информация", blank=True)
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.PROTECT,
        related_name="rounds",
        verbose_name="турнир",
    )

    class Meta:
        verbose_name = "раунд"
        verbose_name_plural = "раунды"
    
    def __str__(self) -> str:
        return f"{self.title} :: {self.tournament}"


class Event(models.Model):
    description = models.CharField("описание", max_length=100)
    result = models.CharField("результат", max_length=100, blank=True)
    round = models.ForeignKey(
        Round,
        on_delete=models.PROTECT,
        related_name="events",
        verbose_name="раунд",
    )

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"
    
    def __str__(self) -> str:
        return f"{self.description} >> {self.result}"


class Predictor(models.Model):
    name = models.CharField("имя", max_length=50)
    vk_id = models.CharField("VK ID", max_length=100, blank=True)
    created_at = models.DateTimeField("создан", auto_now_add=True)
    modified_at = models.DateTimeField("изменён", auto_now=True)

    class Meta:
        verbose_name = "прогнозист"
        verbose_name_plural = "прогнозисты"
    
    def __str__(self) -> str:
        return self.name
