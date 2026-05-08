import os
import json
from flask import Flask, render_template, request, Response, stream_with_context
from google import genai
from google.genai import types
from dotenv import load_dotenv

from datetime import datetime
import re

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'trekly-secret-key')

# Initialize Gemini Client
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)

def sanitize_input(text):
    if not text: return ""
    # Remove potentially malicious scripts or excessive special characters
    return re.sub(r'[<>/{}\[\]]', '', text)[:500]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_itinerary():
    try:
        data = request.json
        
        # --- ROBUST VALIDATION (Edge Cases) ---
        dest = sanitize_input(data.get('destination'))
        if not dest or len(dest) < 2:
            return {"error": "Invalid destination provided."}, 400

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        try:
            d1 = datetime.strptime(start_date, '%Y-%m-%d')
            d2 = datetime.strptime(end_date, '%Y-%m-%d')
            if d2 < d1:
                return {"error": "End date cannot be before start date."}, 400
            if d1 < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                # We'll allow past dates for planning, but flag it as a warning in prompt
                is_past = True
            else:
                is_past = False
        except:
            return {"error": "Invalid date format."}, 400

        # --- DATA CLEANING ---
        origin = sanitize_input(data.get('home_country', 'New Delhi, India'))
        days = int(data.get('duration', 1))
        travelers = sanitize_input(data.get('group_type', '2'))
        budget = data.get('budget', 'Mid-Range')
        style = data.get('travel_style', 'Cultural')
        persona = data.get('persona', 'Family')
        description = sanitize_input(data.get('trip_description', ''))
        interests = data.get('interests', 'General')
        requests = data.get('special_requests', 'None')

        # Construct the Powerful Xplor AI Prompt
        prompt = f\"\"\"
        You are Xplor AI, the world's most advanced travel experience engine. 
        Your mission is to craft a cinematic, high-density travel plan for a journey from {origin} to {dest}.

        USER SPECIFICATIONS:
        - Destination: {dest}
        - Origin: {origin}
        - Travel Window: {start_date} to {end_date} ({days} days)
        - Group Size: {travelers} passengers
        - Budget Level: {budget}
        - Style: {style}
        - Interests: {interests}
        - Trip Persona: {persona}
        - Core Request: {description}

        PERSONA LOGIC:
        - If Persona is 'Work': Focus on high-speed Wi-Fi, meeting spaces, proximity to business hubs, and efficient transport.
        - If Persona is 'Family': Focus on safety, kids' activities, spacious stays, and family-friendly dining.
        - If Persona is 'Friends': Focus on nightlife, group activities, social dining, and vibrant areas.
        - If Persona is 'Solo': Focus on social hostels or boutique stays, safety, and immersive local experiences.

        STRUCTURE YOUR RESPONSE IN THESE EXACT SECTIONS WITH HEADINGS:

        ## 🌍 The Overview
        Vivid vibe check of {dest}. Include: weather advisory for {start_date} specifically, visa/passport requirements for a traveler from {origin}, and estimated travel time.

        ## 📅 The Daily Timeline
        For the travel window of {start_date} to {end_date}, provide a day-by-day breakdown:
        - **Timing-based Schedule**: (e.g., 09:00 AM - Activity)
        - **Top Attractions**: Brief, punchy descriptions.
        - **Estimated Costs**: Cost per activity in USD.
        - **Transport**: How to get between spots.
        - **Local Eats**: Breakfast, Lunch, and Dinner recommendations.

        ## 🏨 Stay Curations
        Suggest 5 specific accommodation options in {dest} for {travelers} guests. 
        Categorize by: **Budget / Mid-range / Luxury**.
        For each: Hotel name, price per night, star rating, amenities, distance from center, Pros/Cons.

        ## ✈️ Flight Intelligence
        Rank 3 hypothetical flight options from {origin} to {dest}.
        Rank by: **Cheapest, Fastest, and Best Value**.
        Include: Airline, times, layovers, baggage policy, and estimated price. Flag red-eyes clearly.

        ## 🍱 Local Guide Insights
        - 5 Must-try local dishes and where to find them.
        - 3 Hidden gems tourists miss.
        - Top 3 local markets or shopping spots.
        - Cultural Dos and Don'ts.

        ## 💰 Budget Breakdown
        Provide a daily spend allocation for: Accommodation, Food, Transport, Activities, and Emergency Fund.
        Flag if the total budget is realistic for {dest}.

        ## 🧳 Packing Essentials
        Specific items based on the season and {style} style.

        ## 🤖 TripBot Assistant
        Travel safety, local laws, and currency tips.
        
        PRACTICAL TRAVEL TIP: (End with one unique, high-value tip).

        TONE: Friendly, professional, elite, and conversational.
        \"\"\"

        def generate():
            try:
                stream = client.models.generate_content_stream(
                    model=\"gemini-2.0-flash\",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=8192,
                        system_instruction=\"You are Xplor AI. You respond with highly detailed, opinionated, and structured travel intelligence in Markdown.\"
                    ),
                )
                for chunk in stream:
                    if chunk.text:
                        payload = json.dumps({\"chunk\": chunk.text})
                        yield f\"data: {payload}\\n\\n\"
                
                yield f\"data: {json.dumps({'done': True})}\n\n"

            except Exception as e:
                error_payload = json.dumps({\"error\": str(e)})
                yield f\"data: {error_payload}\\n\\n\"

    except Exception as e:
        return {\"error\": str(e)}, 500

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        destination = data.get('destination', 'the destination')
        
        prompt = f\"You are TripBot, an elite travel concierge. The user is asking about {destination}. Respond to their question concisely and helpfully: {user_message}\"
        
        response = client.models.generate_content(
            model=\"gemini-2.0-flash\",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=500,
                system_instruction=\"You are TripBot. Be helpful, concise, and professional. Use emojis sparingly.\"
            ),
        )
        return {\"response\": response.text}
    except Exception as e:
        return {\"error\": str(e)}, 500

if __name__ == \"__main__\":
    app.run(debug=True, port=5001, threaded=True)
