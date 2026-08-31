"""
GA4 event tracking for StudentGPA AI.
"""

import requests
import streamlit as st


GA_MEASUREMENT_ID = st.secrets["GA_MEASUREMENT_ID"]
GA_API_SECRET = st.secrets["GA_API_SECRET"]


def track_event(event_name: str, params: dict | None = None) -> None:

    params = params or {}

    url = (
        "https://www.google-analytics.com/mp/collect"
        f"?measurement_id={GA_MEASUREMENT_ID}"
        f"&api_secret={GA_API_SECRET}"
    )

    payload = {
        "client_id": "studentgpa_streamlit",
        "events": [
            {
                "name": event_name,
                "params": {
                    **params,
                    "engagement_time_msec": 100
                }
            }
        ]
    }

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=5
        )

        if response.status_code >= 400:

            print(
                f"GA4 tracking failed: "
                f"{response.status_code} "
                f"{response.text}"
            )

    except Exception as e:

        print(
            f"GA4 tracking error: {e}"
        )
