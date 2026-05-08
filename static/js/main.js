/* ============================================================
   Vayage — main.js v4.1
   State Management & Refined Transitions
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Element References ──────────────────────────────────── */
  const form = document.getElementById('travel-form');
  const submitBtn = document.getElementById('submit-btn');
  const btnText = document.getElementById('btn-text');
  const btnLoader = document.getElementById('btn-loader');
  
  const heroSection = document.getElementById('hero-section');
  const resultsSection = document.getElementById('results-section');
  const mainNav = document.getElementById('main-nav');
  
  const itineraryOutput = document.getElementById('itinerary-output');
  const resultDest = document.getElementById('result-destination');
  const resultDuration = document.getElementById('result-duration');
  const liveStreamText = document.getElementById('live-stream-text');
  
  const destinationInput = document.getElementById('destination');
  const tripDescription = document.getElementById('trip_description');
  const toggleAdvanced = document.getElementById('toggle-advanced');
  const advancedOptions = document.getElementById('advanced-options');
  const toggleIcon = document.getElementById('toggle-icon');
  const backBtn = document.getElementById('back-to-search');

  /* ── State Transitions ──────────────────────────────────── */
  function showResultsPage() {
    heroSection.classList.add('fade-out');
    setTimeout(() => {
      heroSection.style.display = 'none';
      resultsSection.classList.add('active');
      mainNav.classList.add('hidden'); // Hide bottom nav on results
    }, 500);
  }

  function showSearchPage() {
    resultsSection.classList.remove('active');
    setTimeout(() => {
      heroSection.style.display = 'flex';
      setTimeout(() => {
        heroSection.classList.remove('fade-out');
        mainNav.classList.remove('hidden');
      }, 50);
    }, 500);
  }

  backBtn.addEventListener('click', showSearchPage);

  /* ── Advanced Options Toggle ────────────────────────────── */
  toggleAdvanced.addEventListener('click', () => {
    advancedOptions.classList.toggle('hidden');
    toggleIcon.style.transform = advancedOptions.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';
  });

  /* ── Persona Button Logic ────────────────────────────────── */
  const personaBtns = document.querySelectorAll('.persona-btn');
  const personaInput = document.getElementById('selected_persona');
  personaBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      personaBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      personaInput.value = btn.dataset.persona;
    });
  });

  /* ── TripBot Chat Logic ──────────────────────────────────── */
  const chatTrigger = document.getElementById('chat-trigger');
  const chatOverlay = document.getElementById('tripbot-overlay');
  const closeChat = document.getElementById('close-chat');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');
  const chatSubmit = document.getElementById('chat-submit');

  chatTrigger.addEventListener('click', (e) => { e.preventDefault(); chatOverlay.classList.toggle('hidden'); });
  closeChat.addEventListener('click', () => chatOverlay.classList.add('hidden'));

  async function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    appendChatMessage('User', message);
    chatInput.value = '';
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, destination: destinationInput.value || "the trip" })
      });
      const data = await response.json();
      if (data.response) appendChatMessage('TripBot', data.response);
    } catch (err) { appendChatMessage('TripBot', "Error connecting..."); }
  }

  function appendChatMessage(sender, text) {
    const msgDiv = document.createElement('div');
    const isBot = sender === 'TripBot';
    msgDiv.className = isBot ? "bg-white/5 p-3 rounded-xl text-slate-300" : "bg-[#E94560]/10 p-3 rounded-xl text-white self-end text-right";
    msgDiv.innerHTML = `<strong>${sender}:</strong><br/>${text}`;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  chatSubmit.addEventListener('click', sendChatMessage);
  chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendChatMessage(); });

  /* ── Export ────────────────────────────────────────────── */
  let currentItineraryText = "";
  document.getElementById('download-btn').addEventListener('click', () => {
    const blob = new Blob([currentItineraryText], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Xplor_Plan_${destinationInput.value || 'Trip'}.md`;
    a.click();
  });

  /* ── Core: SSE Streaming ─────────────────────────────────── */
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = tripDescription.value.trim();
    if (!description && !destinationInput.value) { alert("Please describe your trip!"); return; }

    showResultsPage();
    itineraryOutput.innerHTML = "";
    liveStreamText.textContent = "";
    document.getElementById('live-stream-box').classList.remove('hidden');
    
    submitBtn.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          destination: destinationInput.value || "Custom Trip",
          home_country: document.getElementById('home_country').value,
          start_date: document.getElementById('start_date').value || new Date().toISOString().split('T')[0],
          end_date: document.getElementById('end_date').value || new Date(Date.now() + 86400000 * 5).toISOString().split('T')[0],
          group_type: document.getElementById('group_type').value,
          budget: document.getElementById('budget').value,
          trip_description: description,
          persona: personaInput.value
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulated = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));
            if (data.chunk) {
              accumulated += data.chunk;
              liveStreamText.textContent = accumulated;
              liveStreamText.scrollTop = liveStreamText.scrollHeight;
            }
          }
        }
      }

      currentItineraryText = accumulated;
      document.getElementById('live-stream-box').classList.add('hidden');
      itineraryOutput.innerHTML = `<div class=\"glass-card p-8 markdown-body shadow-2xl\">${marked.parse(accumulated)}</div>`;
      
      resultDest.textContent = destinationInput.value || \"Bespoke Journey\";
      resultDuration.textContent = \"AI-Engineered Itinerary v4.1\";

    } catch (err) {
      alert(\"Something went wrong. Please try again.\");
      showSearchPage();
    } finally {
      submitBtn.disabled = false;
      btnText.classList.remove('hidden');
      btnLoader.classList.add('hidden');
    }
  });
});
