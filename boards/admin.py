from django.contrib import admin
from .models import PossibleBoard


@admin.register(PossibleBoard)
class PossibleBoardAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "name",
        "email",
        "created_at",
    )

    list_display_links = ("pk", "title", "name", "email")

    list_filter = (
        "title",
        "name",
        "email",
    )

    search_fields = (
        "title",
        "name",
    )
   