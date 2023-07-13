from django.contrib import admin
from .models import PossibleBoard


@admin.register(PossibleBoard)
class PossibleBoardAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "name",
        "email",
        # "position",
        # "get_keywords",
        # "keywords",
        "created_at",
    )

    list_display_links = ("pk", "title", "name", "email")

    list_filter = (
        "title",
        "name",
        "email",
        # "keywords",
        # "position",
    )

    search_fields = (
        "title",
        "name",
        # "keywords",
    )
    
    # # 키워드를 보기 위한 메서드
    # def get_keywords(self, obj):
    #     return obj.get_keywords()
    # get_keywords.short_description = 'Keywords'
