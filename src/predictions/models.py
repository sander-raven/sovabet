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
