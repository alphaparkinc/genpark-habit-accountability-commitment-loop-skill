"""Habit Accountability Commitment Loop.
100% Python Standard Library.
"""

class HabitAccountabilityLoop:
    """Maintains behavioral commitment loops and proactive accountability check-ins."""
    def __init__(self):
        self.habits = {}

    def register_habit(self, habit_id, title, target_days_per_week=5, accountability_partner=None):
        self.habits[habit_id] = {
            "title": title,
            "target": target_days_per_week,
            "partner": accountability_partner,
            "checkins": set(),
            "streak": 0
        }

    def checkin(self, habit_id, day_epoch):
        if habit_id not in self.habits:
            raise KeyError(f"Habit {habit_id} not found")
        day_key = int(day_epoch // 86400)
        h = self.habits[habit_id]
        if day_key not in h["checkins"]:
            h["checkins"].add(day_key)
            h["streak"] += 1
        return {"habit_id": habit_id, "streak": h["streak"], "total_checkins": len(h["checkins"])}

    def evaluate_accountability(self, habit_id, current_day_epoch):
        h = self.habits[habit_id]
        current_day = int(current_day_epoch // 86400)
        checked_today = current_day in h["checkins"]
        needs_nudge = not checked_today
        message = f"Hey, checking in on '{h['title']}'! Have you completed it today?" if needs_nudge else "Goal completed today!"
        return {
            "habit_id": habit_id,
            "needs_nudge": needs_nudge,
            "accountability_partner": h["partner"],
            "message": message
        }
