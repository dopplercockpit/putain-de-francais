from datetime import datetime, timedelta

def next_due(ease: float, interval: int, quality: int):
    # Basic SM-2 rules
    ease = max(1.3, ease + (-0.8 + 0.28*quality - 0.02*quality*quality))
    if quality < 3:
        return ease, 1
    if interval == 0:
        interval = 1
    elif interval == 1:
        interval = 6
    else:
        interval = int(round(interval * ease))
    return ease, interval

def schedule_from(now: datetime, ease: float, interval: int, quality: int):
    ease, interval = next_due(ease, interval, quality)
    return ease, interval, now + timedelta(days=interval)

