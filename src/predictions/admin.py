from django.contrib import admin

from .models import (
    Season,
    Tournament,
    Game,
)


admin.site.site_header = "Административный сайт SOVABET"
admin.site.site_title = "SOVABET"
admin.site.index_title = "Администрирование SOVABET"


class DefaultAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active")
    search_fields = ("name", "info")
    fields = ("name", "info", "is_active", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")
    active_filter = {}

    class Meta:
        abstract = True
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in self.active_filter:
            model = self.active_filter.get(db_field.name)
            if model:
                kwargs["queryset"] = model.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Season)
class SeasonAdmin(DefaultAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(DefaultAdmin):
    list_display = ("__str__", "season", "is_active")
    search_fields = ("name", "info", "season__name", "season__info")
    fields = (
        "name", "info", "is_active", "season", "created_at", "modified_at"
    )
    active_filter = {
        "season": Season,
    }


@admin.register(Game)
class GameAdmin(DefaultAdmin):
    search_fields = ("name", "info", "tournament__name", "tournament__name")
    fields = (
        "name", "info", "is_active", "tournament", "created_at", "modified_at"
    )
    active_filter = {
        "tournament": Tournament,
    }
