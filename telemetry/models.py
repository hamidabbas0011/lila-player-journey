from django.db import models

class TelemetryEvent(models.Model):
    user_id = models.CharField(max_length=80)
    match_id = models.CharField(max_length=100)
    map_id = models.CharField(max_length=40)
    event_type = models.CharField(max_length=32)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    timestamp_ms = models.BigIntegerField(db_index=True)
    date = models.CharField(max_length=20)
    is_bot = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["map_id", "date"], name="tel_map_date_idx"),
            models.Index(fields=["map_id", "match_id"], name="tel_map_match_idx"),
            models.Index(fields=["map_id", "date", "match_id"], name="tel_map_date_match_idx"),
            models.Index(fields=["event_type"], name="tel_event_type_idx"),
        ]
        ordering = ["timestamp_ms"]

    def __str__(self):
        return f"{self.event_type} | {self.map_id} | {self.match_id}"
