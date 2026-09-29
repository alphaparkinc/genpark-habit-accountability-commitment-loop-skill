from client import HabitAccountabilityLoop
import time

loop = HabitAccountabilityLoop()
now = time.time()

# Register habit with partner
loop.register_habit("HABIT_CODING", "Deep Work Sprint (2h)", target_days_per_week=5, accountability_partner="Team_Peer")

# Check in today
res = loop.checkin("HABIT_CODING", now)
print(f"Checkin recorded! Current Streak: {res['streak']} days")

# Evaluate tomorrow
eval_tomorrow = loop.evaluate_accountability("HABIT_CODING", now + 86400)
print(f"Tomorrow's Status: [Needs Nudge: {eval_tomorrow['needs_nudge']}] {eval_tomorrow['message']}")
