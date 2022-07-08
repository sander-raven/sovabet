from django.contrib import admin

from .models import Season


class SeasonAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active")
    search_fields = ("title", "info")
    fields = ("title", "info", "is_active")


admin.site.register(Season, SeasonAdmin)
