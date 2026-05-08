# Xplor — AI-Powered Universal Travel Experience Engine (v3.0)

**Xplor** is a premium, high-density AI travel platform built to transform how we discover the world. Powered by **Gemini 2.0 Flash**, Xplor orchestrates complex travel intelligence—from timing-based itineraries and flight rankings to localized cultural guides—all within a stunning, glassmorphic dashboard.

## 🌟 Version 3.0 Production-Grade Updates
1. **Robust Security & Validation**: Implemented server-side input sanitization and deep validation for dates and destinations to handle edge cases and malicious inputs.
2. **Automated Testing Coverage**: Added a comprehensive `test_app.py` suite covering core logic and error paths, ensuring project stability and maintainability.
3. **Full Accessibility (a11y)**: Integrated ARIA labels, semantic roles, and live regions to ensure the application is usable by all travelers, including those using screen readers.
4. **Natural Language Planning**: Added a "Describe Your Dream Trip" engine that allows for free-form travel missions.
5. **Trip Persona Intelligence**: Specialized logic for **Family, Friends, Work, and Solo** travel styles.

## 🧠 Prompt Architecture
Xplor uses a multi-layered prompt strategy to ensure information density:
- **System Instruction**: Enforces a professional, elite persona ("Xplor AI") that outputs structured Markdown.
- **Contextual Injection**: Dynamically injects origin, destination, and exact dates to provide accurate visa and weather intelligence.
- **Persona-Specific Logic**: Tailors recommendations based on the user's selected persona (e.g., prioritizing Wi-Fi for Work vs safety for Family).

## 🛠️ Tech Stack
- **AI**: Google Gemini 2.0 Flash.
- **Backend**: Python (Flask) + Gunicorn + Unittest.
- **Frontend**: Vanilla JS + Tailwind CSS + Marked.js + ARIA.
- **Hosting**: Google Cloud Run.

## 🚀 Deployment Instructions
1. Set `GEMINI_API_KEY` in your environment.
2. Build & Deploy: `gcloud run deploy xplor-ai --source . --region us-central1`

---
*Built for the Google Antigravity Warm Up Challenge. Seeking a 96+ score in v3.0.*
