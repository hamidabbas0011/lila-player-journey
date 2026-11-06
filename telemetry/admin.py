from django.contrib import admin
from .models import TelemetryEvent

@admin.register(TelemetryEvent)
class TelemetryEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "map_id", "date", "match_id", "user_id", "is_bot", "timestamp_ms")
    list_filter = ("map_id", "date", "event_type", "is_bot")
    search_fields = ("user_id", "match_id")
