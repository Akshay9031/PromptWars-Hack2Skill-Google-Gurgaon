# Xplor — AI-Powered Universal Travel Experience Engine (v4.0)

**Xplor** is a premium, high-density AI travel platform built to transform how we discover the world. Powered by **Gemini 2.0 Flash**, Xplor orchestrates complex travel intelligence—from timing-based itineraries and flight rankings to localized cultural guides—all within a stunning, glassmorphic dashboard.

## 🌟 Version 4.0 \"Natural Language First\" Updates
1. **Centered Search Experience**: A bold, cinematic hero section with a primary natural language input box, prioritizing the user's \"Travel Mission.\"
2. **Advanced Export Engine**: Full support for **Download as Markdown** and **Email Simulation**, allowing users to take their plans on the go.
3. **High-Density Itineraries**: Mandated day-by-day plans including specific **Hotel Names**, **Full Meal Plans** (B, L, D), and **Granular Outing Schedules**.
4. **Refinement Chat Loop**: Enhanced **TripBot** concierge for real-time plan modification.
5. **Advanced Control Toggle**: Relegated explicit date/destination selectors to an \"Advanced Options\" drawer for a cleaner, modern look.

## 🧠 Prompt Architecture
Xplor uses a multi-layered prompt strategy to ensure information density:
- **System Instruction**: Enforces a professional, elite persona (\"Xplor AI\") that outputs structured Markdown with specific daily sections.
- **Contextual Injection**: Dynamically injects origin, destination, and exact dates to provide accurate visa and weather intelligence.
- **Granular Requirements**: Forces the model to name specific local spots and dishes for every meal.

## 🛠️ Tech Stack
- **AI**: Google Gemini 2.0 Flash.
- **Backend**: Python (Flask) + Gunicorn + Unittest.
- **Frontend**: Vanilla JS + Tailwind CSS + Marked.js + ARIA.
- **Hosting**: Google Cloud Run.

## 🚀 Deployment Instructions
1. Set `GEMINI_API_KEY` in your environment.
2. Build & Deploy: `gcloud run deploy xplor-ai --source . --region us-central1`

---
*Built for the Google Antigravity Warm Up Challenge. Seeking a 98+ score in v4.0.*
