#!/usr/bin/env python3
"""
New submission alert script.
Only fires when there are new submissions since last check.
Sends Telegram message with the new submission details.
"""
import os
import json
import urllib.request

SITE_URL = "https://findyourpeople.onrender.com"
STATE_FILE = "/home/jess/website/reports/.traffic_state.json"


def get_submissions():
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
    return {"last_count": 0, "last_ids": []}


def main():
    state = load_state()
    all_subs = get_submissions()
    last_ids = set(state.get("last_ids", []))
    current_ids = {s['id'] for s in all_subs}
    new_ids = current_ids - last_ids

    if not new_ids:
        print("No new submissions")
        return

    # Find the new submissions
    new_subs = [s for s in all_subs if s['id'] in new_ids]

    goal_labels = {
        "making_friends": "Making friends",
        "social_confidence": "Social confidence",
        "practicing_conversation": "Practicing conversation",
        "eventually_dating": "Eventually dating",
        "other": "Other",
    }

    lines = ["🆕 New submission(s)!"]
    for s in new_subs:
        notes = (s.get("anything_else") or "")[:100]
        lines.append("")
        lines.append(f"👤 {s.get('name')}, {s.get('age')} ({s.get('self_or_other', 'self')})")
        lines.append(f"   Goal: {goal_labels.get(s.get('primary_focus'), 'N/A')}")
        lines.append(f"   Support: {s.get('support_needs', 'N/A')}")
        lines.append(f"   Availability: {s.get('availability', 'N/A')}")
        if notes:
            lines.append(f"   \"{notes}\"")
        lines.append(f"   📧 {s.get('preferred_contact', 'N/A')}")

    message = "\n".join(lines)
    print(message)

    # Save updated state
    state["last_count"] = len(all_subs)
    state["last_ids"] = list(current_ids)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


if __name__ == "__main__":
    main()
