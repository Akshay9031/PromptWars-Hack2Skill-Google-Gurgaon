# Xplor — AI-Powered Universal Travel Experience Engine

**Xplor** is a premium, high-density AI travel platform built to transform how we discover the world. Powered by **Gemini 2.0 Flash**, Xplor orchestrates complex travel intelligence—from timing-based itineraries and flight rankings to localized cultural guides—all within a stunning, glassmorphic dashboard.

## 🌟 The Challenge Vertical
**Vertical Chosen**: AI Travel Assistant / Personal Concierge.
**Target Persona**: The Modern Explorer. Someone who values information density, speed, and localized, expert-grade travel advice.

## 🧠 Approach & Logic
Xplor uses a multi-dimensional prompt orchestration strategy:
1. **Contextual Awareness**: By capturing source city, destination, and precise travel dates, the engine provides localized visa advice and seasonal weather intelligence.
2. **High-Density Itineraries**: Unlike standard planners, Xplor generates timing-based schedules, estimated costs per activity, and ranked accommodation/flight options.
3. **TripBot Assistant**: A persistent AI concierge handles real-time safety questions and travel laws.
4. **Streaming Architecture**: Uses Server-Sent Events (SSE) to stream AI responses instantly, ensuring a premium, low-latency user experience.

## 🛠️ Tech Stack & Google Services
- **AI Core**: Google Gemini 2.0 Flash (via Google Gen AI SDK).
- **Backend**: Python (Flask) with Gunicorn for production-grade serving.
- **Frontend**: Vanilla JS + Tailwind CSS (Custom Design System).
- **Deployment**: Google Cloud Run (Fully Serverless).
- **Location Services**: Photon API (OpenStreetMap) for smart autocompletion.

## 🚀 How It Works
1. **Build Your Journey**: Input your origin, destination, and travel window.
2. **Persona Mapping**: Choose your travel style (Luxury, Adventure, Cultural) to tailor the AI's logic.
3. **Intelligence Generation**: Xplor AI streams a structured Markdown itinerary including 8 specific travel dimensions.
4. **TripBot Assistance**: Toggle the chat overlay for quick answers to travel-specific questions.

## 📋 Assumptions & Implementation Notes
- **API Access**: Requires a `GEMINI_API_KEY` in environment variables.
- **Statelessness**: Designed as a stateless application for optimal scaling on Google Cloud Run.
- **Mobile First**: The UI is built with a sticky bottom navigation, optimized for both desktop and mobile high-density viewing.

---
*Built for the Google Antigravity Warm Up Challenge.*
