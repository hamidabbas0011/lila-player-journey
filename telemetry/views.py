import json
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from .models import TelemetryEvent

MAPS = {
    "AmbroseValley": {"label": "Ambrose Valley", "image": "telemetry/minimaps/AmbroseValley_Minimap.png", "scale": 900, "origin_x": -370, "origin_z": -473},
    "GrandRift": {"label": "Grand Rift", "image": "telemetry/minimaps/GrandRift_Minimap.png", "scale": 581, "origin_x": -290, "origin_z": -290},
    "Lockdown": {"label": "Lockdown", "image": "telemetry/minimaps/Lockdown_Minimap.jpg", "scale": 1000, "origin_x": -500, "origin_z": -500},
}
def dashboard(request):
    return render(request, "telemetry/dashboard.html", {"maps": MAPS, "maps_json": json.dumps(MAPS)})

def filter_options(request):
    map_id = request.GET.get("map", "AmbroseValley")
    dates = list(TelemetryEvent.objects.values_list("date", flat=True).distinct().order_by("date"))
    matches_qs = TelemetryEvent.objects.all()
    if map_id in MAPS:
        matches_qs = matches_qs.filter(map_id=map_id)
    date = request.GET.get("date", "all")
    if date != "all":
        matches_qs = matches_qs.filter(date=date)
    matches = list(matches_qs.values_list("match_id", flat=True).distinct().order_by("match_id")[:2000])
    return JsonResponse({"dates": dates, "matches": matches, "maps": MAPS})

def telemetry_data(request):
    map_id = request.GET.get("map", "AmbroseValley")
    if map_id not in MAPS:
        return JsonResponse({"error": "Unknown map"}, status=400)
    qs = TelemetryEvent.objects.filter(map_id=map_id)
    date = request.GET.get("date", "all")
    match = request.GET.get("match", "all")
    if date != "all":
        qs = qs.filter(date=date)
    if match != "all":
        qs = qs.filter(match_id=match)

    # Return compact rows; keep the API payload bounded for the all-matches view.
    total = qs.count()
    rows = list(qs.order_by("timestamp_ms").values(
        "user_id", "match_id", "map_id", "event_type", "x", "z", "timestamp_ms", "is_bot", "date"
    ))
    stats = {
        "players": qs.values("user_id").distinct().count(),
        "kills": qs.filter(event_type__in=["Kill", "BotKill"]).count(),
        "deaths": qs.filter(event_type__in=["Killed", "BotKilled", "KilledByStorm"]).count(),
        "loot": qs.filter(event_type="Loot").count(),
        "events": total,
    }
    return JsonResponse({
        "events": rows,
        "stats": stats,
        "total": total,
        "truncated": False,
        "map": MAPS[map_id],
    })
