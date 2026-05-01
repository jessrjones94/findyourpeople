from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
from db.database import get_db, init_db, record_page_view, get_page_view_counts

website_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Mount static files
static_dir = os.path.join(website_dir, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

HTML_INDEX = """<!DOCTYPE html>
<html>
<head>
    <title>Structured Social Connection | Neurodivergent Pilot Program</title>
    <link rel="stylesheet" href="/static/style.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f9f7f4;
            color: #3d3d3d;
            line-height: 1.6;
            padding: 20px;
        }
        .container {
            max-width: 720px;
            margin: 0 auto;
            background: #fff;
            padding: 48px 40px;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        h1 {
            color: #6b7c6b;
            margin-bottom: 8px;
            font-size: 1.8em;
        }
        .subtitle {
            color: #888;
            margin-bottom: 36px;
            font-size: 1.05em;
        }
        p {
            margin: 14px 0;
        }
        .hero {
            text-align: center;
            padding: 20px 0 36px;
            border-bottom: 2px solid #f0ebe6;
            margin-bottom: 32px;
        }
        .hero h1 {
            font-size: 2em;
            color: #6b7c6b;
        }
        .hero .subtitle {
            font-size: 1.15em;
            max-width: 520px;
            margin: 12px auto 24px;
        }
        .cta-btn {
            display: inline-block;
            padding: 14px 32px;
            background: #8b6b8b;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1.05em;
            transition: background 0.2s, transform 0.1s;
            margin: 8px 4px;
        }
        .cta-btn:hover {
            background: #7a5a7a;
            transform: translateY(-1px);
        }
        .cta-btn.secondary {
            background: #6b7c6b;
        }
        .cta-btn.secondary:hover {
            background: #5a6a5a;
        }
        .section {
            margin: 28px 0;
            padding: 20px;
            background: #faf8f5;
            border-radius: 10px;
        }
        .section h2 {
            color: #8b6b8b;
            margin-top: 0;
            font-size: 1.15em;
        }
        .section ul {
            margin: 12px 0;
            padding-left: 24px;
        }
        .section li {
            margin: 8px 0;
            line-height: 1.5;
        }
        .features-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
            margin: 16px 0;
        }
        .feature {
            background: #f0ebe6;
            padding: 14px;
            border-radius: 8px;
        }
        .feature strong {
            color: #6b7c6b;
        }
        .privacy-note {
            margin-top: 32px;
            padding: 14px;
            background: #f0ebe6;
            border-radius: 8px;
            font-size: 0.85em;
            color: #777;
            text-align: center;
        }
        .footer {
            text-align: center;
            margin-top: 32px;
            font-size: 0.85em;
            color: #aaa;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>Structured Social Connection</h1>
            <p class="subtitle">A low-pressure, guided space for real connection — without overwhelm, awkwardness, or pressure to perform.</p>
            <a href="/form" class="cta-btn">Join Pilot Interest List</a>
            <a href="/about" class="cta-btn secondary">Learn More</a>
        </div>

        <div class="section">
            <h2>What This Is</h2>
            <p>A small, structured social experience for neurodivergent young adults and adults seeking friendship, confidence, and authentic connection in a predictable, supportive environment.</p>
        </div>

        <div class="section">
            <h2>Who It's For</h2>
            <ul>
                <li>Neurodivergent adults who want connection without overwhelm</li>
                <li>People who prefer smaller groups</li>
                <li>Those who feel more comfortable with structure</li>
                <li>Adults who benefit from clear expectations and shared activities</li>
            </ul>
        </div>

        <div class="section">
            <h2>What Makes It Different</h2>
            <div class="features-grid">
                <div class="feature"><strong>4–6 people max</strong><br>Small, intimate group</div>
                <div class="feature"><strong>Clear structure</strong><br>Predictable start, flow, and end</div>
                <div class="feature"><strong>Shared activities</strong><br>Not forced small talk</div>
                <div class="feature"><strong>Optional participation</strong><br>No pressure to share or talk</div>
                <div class="feature"><strong>Sensory-aware</strong><br>Low-stimulation environment</div>
                <div class="feature"><strong>Step away option</strong><br>Breaks built in</div>
            </div>
        </div>

        <div class="section">
            <h2>The Pilot Group</h2>
            <p>A first-round, small-group experience designed to create comfort, reduce isolation, and support genuine connection. Think: guided hangouts with light structure, not therapy or a social skills class.</p>
        </div>

        <div class="section">
            <h2>What It's NOT</h2>
            <ul>
                <li>Not therapy or clinical services</li>
                <li>Not a high-support care program</li>
                <li>Not a dating-only group (friendship first)</li>
                <li>Not a chaotic meetup</li>
            </ul>
        </div>

        <div style="text-align: center; margin-top: 32px;">
            <a href="/form" class="cta-btn">Join Pilot Interest List ✨</a>
        </div>

        <div class="privacy-note">
            🔒 This is not therapy, counseling, or medical care. This is a community-based social support program.
        </div>

        <div class="footer">
            Questions? <a href="/contact">Contact us</a> or <a href="/form">fill out the interest form</a> and we'll follow up.
        </div>
    </div>
    <script>fetch("/track",{method:"POST",body:new URLSearchParams({page:location.pathname}),headers:{"Content-Type":"application/x-www-form-urlencoded"}}).catch(()=>{});</script>
</body>
</html>"""

HTML_FORM = open(os.path.join(website_dir, "templates", "form.html")).read()

HTML_SUCCESS = """<!DOCTYPE html>
<html>
<head>
    <title>Submitted!</title>
    <link rel="stylesheet" href="/static/style.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f9f7f4;
            color: #3d3d3d;
            padding: 20px;
        }
        .container {
            max-width: 560px;
            margin: 60px auto;
            background: #fff;
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        h1 {
            color: #6b7c6b;
            font-size: 1.8em;
        }
        p {
            color: #666;
            margin: 16px 0;
        }
        .emoji {
            font-size: 3em;
            margin-bottom: 12px;
        }
        .cta-btn {
            display: inline-block;
            margin: 8px 4px;
            padding: 12px 28px;
            background: #8b6b8b;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
        }
        .cta-btn:hover {
            background: #7a5a7a;
        }
        .next-steps {
            margin-top: 28px;
            padding: 20px;
            background: #f0ebe6;
            border-radius: 10px;
            text-align: left;
        }
        .next-steps h3 {
            color: #8b6b8b;
            margin-top: 0;
        }
        .next-steps ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .next-steps li {
            margin: 8px 0;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">✨</div>
        <h1>You're on the list!</h1>
        <p>Thank you for your interest. We'll review your responses and follow up soon.</p>

        <div class="next-steps">
            <h3>What happens next?</h3>
            <ul>
                <li>We review your submission to find the best fit for the pilot group</li>
                <li>If there's a good match, we'll reach out within the next 1–2 weeks</li>
                <li>The first pilot group is small (4–6 people) and intentionally curated</li>
                <li>No pressure — if it's not the right fit for the first round, we'll keep you in mind</li>
            </ul>
        </div>

        <a href="/" class="cta-btn">Back to Home</a>
    </div>
    <script>fetch("/track",{method:"POST",body:new URLSearchParams({page:location.pathname}),headers:{"Content-Type":"application/x-www-form-urlencoded"}}).catch(()=>{});</script>
</body>
</html>"""

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_INDEX

@app.get("/form", response_class=HTMLResponse)
def form_page():
    return HTML_FORM

@app.post("/submit")
def submit(
    name: str = Form(...),
    age: str = Form(""),
    self_or_other: str = Form(""),
    preferred_contact: str = Form(""),
    support_needs: str = Form(""),
    support_needs_description: str = Form(""),
    social_challenges: str = Form(""),
    comfortable_with: str = Form(""),
    overwhelming_things: str = Form(""),
    goals: str = Form(""),
    primary_focus: str = Form(""),
    step_away_important: str = Form(""),
    comfort_helpers: str = Form(""),
    availability: str = Form(""),
    anything_else: str = Form("")
):
    with get_db() as conn:
        conn.execute(
            """INSERT INTO submissions (
                name, age, self_or_other, preferred_contact,
                support_needs, support_needs_description, social_challenges,
                comfortable_with, overwhelming_things,
                goals, primary_focus,
                step_away_important, comfort_helpers,
                availability, anything_else
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                name, age, self_or_other, preferred_contact,
                support_needs, support_needs_description, social_challenges,
                comfortable_with, overwhelming_things,
                goals, primary_focus,
                step_away_important, comfort_helpers,
                availability, anything_else
            )
        )
        conn.commit()
    return RedirectResponse(url="/success", status_code=303)

@app.get("/success", response_class=HTMLResponse)
def success():
    return HTML_SUCCESS

@app.get("/about", response_class=HTMLResponse)
def about():
    path = os.path.join(website_dir, "templates", "about.html")
    return HTMLResponse(open(path).read())

@app.get("/faq", response_class=HTMLResponse)
def faq():
    path = os.path.join(website_dir, "templates", "faq.html")
    return HTMLResponse(open(path).read())

@app.get("/pilot", response_class=HTMLResponse)
def pilot():
    path = os.path.join(website_dir, "templates", "pilot.html")
    return HTMLResponse(open(path).read())

@app.get("/contact", response_class=HTMLResponse)
def contact():
    path = os.path.join(website_dir, "templates", "contact.html")
    return HTMLResponse(open(path).read())

@app.get("/submissions")
def submissions():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM submissions ORDER BY submitted_at DESC").fetchall()
    return {"submissions": [dict(row) for row in rows]}

@app.post("/submissions/{submission_id}/delete")
def delete_submission(submission_id: int):
    with get_db() as conn:
        conn.execute("DELETE FROM submissions WHERE id = ?", (submission_id,))
        conn.commit()
    return {"deleted": submission_id}

@app.get("/health")
def health():
    return {"status": "ok", "db": "connected"}

# --- Page view tracking (unnoticeable, no UI impact) ---
@app.post("/track")
def track_page(page: str = Form(...)):
    """Lightweight endpoint to record a page view. Called by tiny inline JS."""
    record_page_view(page)
    return {"ok": True}

@app.get("/stats")
def stats():
    """Page view counts — for your own reference, not shown publicly."""
    counts = get_page_view_counts()
    total = sum(counts.values())
    return {"total": total, "pages": counts}
