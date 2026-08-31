"""
ga_tracking.py

Reusable helper to fire custom GA4 events from a Streamlit app.

Setup:
1. Find your GA4 Measurement ID: GA4 Admin -> Data Streams -> your Web stream -> Measurement ID (looks like "G-XXXXXXXXXX").
2. Paste it into GA_MEASUREMENT_ID below.
3. Import track_event() and call it right after the action you want to log.
"""

import json
import streamlit.components.v1 as components

GA_MEASUREMENT_ID = "G-BLH8FSGHR1"  # <-- replace with your real Measurement ID


def track_event(event_name: str, params: dict | None = None) -> None:
    """
    Fires a custom GA4 event from the currently rendered Streamlit page.

    event_name: GA4 event name, e.g. "sign_up" or "gpa_calculated"
    params: optional dict of extra event parameters, e.g. {"method": "email"}

    Call this immediately after the action happens (e.g. right after a
    successful signup, or right after a GPA calculation completes), inside
    the same `if st.button(...)` / `if submitted:` block.
    """
    params = params or {}
    params_json = json.dumps(params)

    components.html(
        f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{ dataLayer.push(arguments); }}
          gtag('js', new Date());
          gtag('config', '{GA_MEASUREMENT_ID}');
          gtag('event', '{event_name}', {params_json});
        </script>
        """,
        height=0,
        width=0,
    )
