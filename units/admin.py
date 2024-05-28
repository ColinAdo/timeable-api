from django.contrib import admin

from .models import Unit


class UnitAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
        "created_at"
    ]


admin.site.register(Unit, UnitAdmin)
