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
        
        # --- ROBUST VALIDATION & DEFAULTS ---
        dest = sanitize_input(data.get('destination'))
        if not dest or len(dest) < 2:
            dest = \"the location described\" # Let AI infer from description

        start_date = data.get('start_date') or datetime.now().strftime('%Y-%m-%d')
        end_date = data.get('end_date') or (datetime.now().replace(day=datetime.now().day + 4)).strftime('%Y-%m-%d')
        
        try:
            d1 = datetime.strptime(start_date, '%Y-%m-%d')
            d2 = datetime.strptime(end_date, '%Y-%m-%d')
            if d2 < d1:
                return {\"error\": \"End date cannot be before start date.\"}, 400
            days = (d2 - d1).days + 1
        except:
            days = 4 # Default fallback

        # --- DATA CLEANING ---
        origin = sanitize_input(data.get('home_country', 'New Delhi, India'))
        travelers = sanitize_input(data.get('group_type', '2'))
        budget = data.get('budget', 'Mid-Range')
        style = data.get('travel_style', 'Cultural')
        persona = data.get('persona', 'Family')
        description = sanitize_input(data.get('trip_description', ''))

        # Construct the Powerful Xplor AI Prompt
        prompt = f\"\"\"
        You are Xplor AI, the world's most advanced travel experience engine. 
        Your mission is to craft a cinematic, high-density travel plan.

        USER SPECIFICATIONS:
        - Description of Trip: {description}
        - Target Destination: {dest}
        - Travel Window: {start_date} to {end_date} ({days} days)
        - Group Size: {travelers} passengers
        - Budget Level: {budget}
        - Style: {style}
        - Persona: {persona}

        CORE REQUIREMENT: You MUST provide a complete, granular plan for EVERY SINGLE DAY. 
        Generic summaries are NOT allowed.

        STRUCTURE YOUR RESPONSE IN THESE EXACT SECTIONS:

        ## 🌍 The Mission Overview
        Vivid summary of the trip to {dest}. Weather forecast and travel advisory for {start_date}.

        ## 📅 Day-by-Day Master Plan
        For each day from {start_date} to {end_date}, you MUST include:
        - **🏨 Accommodation**: Name a specific high-quality hotel/stay matching the {budget} budget.
        - **🥣 Breakfast**: Specific dish and a highly-rated local spot.
        - **🏛️ Morning Outing**: Detailed activity with timing.
        - **🍱 Lunch**: Specific dish and a highly-rated local spot.
        - **🌳 Afternoon Outing**: Detailed activity with timing.
        - **🍷 Dinner**: Specific dish and a highly-rated local spot.
        - **✨ Evening Experience**: A unique local recommendation.

        ## ✈️ Flight Logistics
        Top 3 flight options from {origin} to {dest} (Cheapest, Fastest, Best Value).

        ## 🍱 Local Guide Insights
        Must-try dishes, hidden gems, and cultural etiquette.

        ## 💰 Financial Breakdown
        Estimated daily spend vs total budget.

        ## 🤖 TripBot Assistant
        Safety tips and local laws.
        
        PRACTICAL TRAVEL TIP: (End with one unique, high-value tip).

        TONE: Elite, professional, and immersive. Use Markdown tables for flights and costs.
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
