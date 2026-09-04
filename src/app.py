from datetime import UTC, date, datetime

from dateutil.relativedelta import relativedelta
from flask import Flask, Response, render_template, request

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
# CONFIG — edit everything in this section, nothing else needed.
# ─────────────────────────────────────────────────────────────

TO_NAME = "Anna"
FROM_NAME = "Vlad"
INVITE_MESSAGE = "I've been meaning to ask you out properly. Pick a day that works, then what you're in the mood for."
ACTIVITIES = [
    {"id": "dinner", "label": "Dinner"},
    {"id": "walk", "label": "Afternoon walk"},
    {"id": "movie", "label": "Movie night"},
    {"id": "drinks", "label": "Drinks"},
    {"id": "surprise", "label": "Surprise me"},
]


def confirmation_message(chosen_date: str, activity_label: str, note: str) -> str:
    d = date.fromisoformat(chosen_date)
    pretty_date = f"{d.strftime('%A, %B')} {d.day}"
    base = f"{pretty_date} it is — {activity_label.lower()}."
    if note:
        base += f" Note: \u201c{note}\u201d"
    return base


def date_bounds() -> tuple[date, date]:
    """Compute min/max allowed dates fresh on every call, so they never go stale."""
    today = datetime.now(tz=UTC).date()
    return today, today + relativedelta(months=1)


@app.route("/")
def index() -> str:
    min_date, max_date = date_bounds()
    return render_template(
        "main/index.html",
        to_name=TO_NAME,
        from_name=FROM_NAME,
        message=INVITE_MESSAGE,
        activities=ACTIVITIES,
        min_date=min_date.isoformat(),
        max_date=max_date.isoformat(),
    )


@app.post("/choose")
def choose() -> str:
    chosen_date = (request.form.get("date") or "").strip()
    activity_id = request.form.get("activity")
    note = (request.form.get("note") or "").strip()

    activity = next(a for a in ACTIVITIES if a["id"] == activity_id)

    reply = confirmation_message(chosen_date, activity["label"], note)

    return render_template(
        "main/confirmation.html",
        to_name=TO_NAME,
        from_name=FROM_NAME,
        reply=reply,
    )


@app.route("/favicon.ico")
def favicon() -> Response:
    return app.send_static_file("img/favicon.ico")


if __name__ == "__main__":
    app.run()
