#!/usr/bin/env python3
"""
Website traffic and form submission monitor.
Checks for new submissions from the live Render URL and reports stats every 15 minutes.
"""
import os
import json
import urllib.request
from datetime import datetime
from pathlib import Path

SITE_URL = "https://findyourpeople.onrender.com"
STATE_FILE = "/home/jess/website/reports/.traffic_state.json"
REPORT_DIR = "/home/jess/website/reports/reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def get_submissions():
    """Fetch submissions from the live Render site."""
    try:
        req = urllib.request.Request(
            f"{SITE_URL}/submissions",
            headers={"Accept": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("submissions", [])
    except Exception as e:
        print(f"Error fetching submissions: {e}")
        return []


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_count": 0, "last_check": None, "total_views": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def build_report(new_count, all_submissions):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Calculate stats
    total = len(all_submissions)
    self_referred = [s for s in all_submissions if s.get("self_or_other") == "self"]
    parent_referred = [s for s in all_submissions if s.get("self_or_other") in ("parent", "caregiver")]

    # Ages
    ages = {}
    for s in all_submissions:
        a = s.get("age", "unknown") or "unknown"
        try:
            group = f"{int(a)//5*5}s"
        except:
            group = "unknown"
        ages[group] = ages.get(group, 0) + 1

    # Goals breakdown
    goals = {}
    for s in all_submissions:
        g = s.get("primary_focus", "unknown") or "unknown"
        goals[g] = goals.get(g, 0) + 1

    # Availability
    availability = {"weekday_evenings": 0, "weekends": 0, "flexible": 0}
    for s in all_submissions:
        av = s.get("availability", "") or ""
        if "weekday" in av:
            availability["weekday_evenings"] += 1
        if "weekend" in av:
            availability["weekends"] += 1
        if "flexible" in av:
            availability["flexible"] += 1

    # New entries in this cycle
    new_entries = all_submissions[:new_count] if new_count > 0 else []

    report_lines = [
        "=" * 55,
        f"📊 WEBSITE TRAFFIC + SUBMISSION REPORT",
        f"⏰ Checked: {timestamp}",
        f"🌐 {SITE_URL}",
        f"📬 Total submissions: {total}",
        f"🆕 New since last check: {new_count}",
        "=" * 55,
        "",
        "--- SUBMISSION BREAKDOWN ---",
        f"  Self-referred:     {len(self_referred)}",
        f"  Parent/Caregiver:  {len(parent_referred)}",
        "",
        "--- AGE DISTRIBUTION ---",
    ]

    for age_group in sorted(ages.keys()):
        report_lines.append(f"  {age_group}: {ages[age_group]}")

    report_lines += [
        "",
        "--- GOALS ---",
    ]
    goal_labels = {
        "making_friends": "Making friends",
        "social_confidence": "Social confidence",
        "practicing_conversation": "Practicing conversation",
        "eventually_dating": "Eventually dating",
        "unknown": "Not specified"
    }
    for g, count in sorted(goals.items(), key=lambda x: -x[1]):
        report_lines.append(f"  {goal_labels.get(g, g)}: {count}")

    report_lines += [
        "",
        "--- AVAILABILITY ---",
        f"  Weekday evenings: {availability['weekday_evenings']}",
        f"  Weekends:         {availability['weekends']}",
        f"  Flexible:         {availability['flexible']}",
    ]

    if new_entries:
        report_lines += [
            "",
            "=" * 55,
            f"🆕 NEW SUBMISSIONS ({new_count})",
            "=" * 55,
        ]
        for s in new_entries:
            notes = (s.get("anything_else") or "")[:80]
            report_lines += [
                f"",
                f"  👤 {s.get('name')}, {s.get('age')} ({s.get('self_or_other', 'self')})",
                f"     Goal: {goal_labels.get(s.get('primary_focus'), 'N/A')}",
                f"     Support: {s.get('support_needs', 'N/A')}",
                f"     Availability: {s.get('availability', 'N/A')}",
                f"     \"{notes}\"",
                f"     📧 {s.get('preferred_contact', 'N/A')}",
            ]
    else:
        report_lines += [
            "",
            "✅ No new submissions since last check.",
        ]

    report_lines += [
        "",
        f"📁 State saved to: {STATE_FILE}",
    ]

    return "\n".join(report_lines)


def main():
    state = load_state()
    all_subs = get_submissions()
    total_now = len(all_subs)
    last_total = state.get("last_count", 0)
    new_count = total_now - last_total

    report = build_report(new_count, all_subs)
    print(report)

    # Save snapshot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = os.path.join(REPORT_DIR, f"traffic_{timestamp}.txt")
    with open(report_path, "w") as f:
        f.write(report)

    # Update state
    state["last_count"] = total_now
    state["last_check"] = datetime.now().isoformat()
    save_state(state)

    print(f"\n✅ Report saved: {report_path}")


if __name__ == "__main__":
    main()
