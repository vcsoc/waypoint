from datetime import date, datetime, time, timedelta, timezone
from typing import Final
from zoneinfo import ZoneInfo

import pytest

from waypoint.repositories.daily_activity_timezone import local_day_window


@pytest.mark.parametrize("zone_name", ["UTC", "America/New_York", "Europe/Athens", "Asia/Kathmandu"])
@pytest.mark.parametrize("day", [date(2025, 3, 9), date(2025, 11, 2), date(1945, 8, 14)])
def test_local_days_have_exact_half_open_utc_bounds(zone_name: str, day: date) -> None:
    zone: Final = ZoneInfo(zone_name)
    window: Final = local_day_window(day, day, zone)
    assert window.start.tzinfo is timezone.utc and window.end.tzinfo is timezone.utc
    assert window.start.astimezone(zone).date() == day
    assert window.start.astimezone(zone).time() == time.min
    assert (window.end - timedelta(microseconds=1)).astimezone(zone).date() == day
    assert window.end.astimezone(zone).date() == day + timedelta(days=1)
    assert window.end.astimezone(zone).time() == time.min
    middle: Final = datetime.combine(day, time(12), zone).astimezone(timezone.utc)
    assert window.start <= middle < window.end
