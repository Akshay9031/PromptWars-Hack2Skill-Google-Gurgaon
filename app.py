import os
import json
from flask import Flask, render_template, request, Response, stream_with_context
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'trekly-secret-key')

# Initialize Gemini Client
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_itinerary():
    data = request.json
    
    # Extract parameters
    dest = data.get('destination')
    origin = data.get('home_country', 'New Delhi, India')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    days = data.get('duration')
    travelers = data.get('group_type', '2')
    budget = data.get('budget', 'Mid-Range')
    style = data.get('travel_style', 'Cultural')
    interests = data.get('interests', 'General')
    requests = data.get('special_requests', 'None')

    # Construct the Powerful Xplor AI Prompt
    prompt = f"""
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
    - Special Requests: {requests}

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
    """

    def generate():
        try:
            stream = client.models.generate_content_stream(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=8192,
                    system_instruction="You are Vayage AI. You respond with highly detailed, opinionated, and structured travel intelligence in Markdown."
                ),
            )
            for chunk in stream:
                if chunk.text:
                    payload = json.dumps({"chunk": chunk.text})
                    yield f"data: {payload}\n\n"
            
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            error_payload = json.dumps({"error": str(e)})
            yield f"data: {error_payload}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True, port=5001, threaded=True)
