async function loadVenues() {
    try {
        const res = await fetch('/api/venues');
        const data = await res.json();
        const container = document.getElementById('venue-grid');
        
        container.innerHTML = data.map(v => `
            <div class="card">
                <h3>${v.name}</h3>
                <p style="background:#ffebee; color:#c62828; display:inline-block; padding:2px 10px; border-radius:10px; font-size:0.8em; font-weight:bold;">${v.category}</p>
                <p style="font-style:italic; color:#555; margin-top:15px;">"${v.vibe || 'No description yet'}"</p>
            </div>
        `).join('');
    } catch (err) {
        console.error("Connection Error:", err);
    }
}

async function askAI() {
    const input = document.getElementById('ai-input');
    const box = document.getElementById('chat-box');
    const message = input.value.trim();
    
    if (!message) return;

    // Show User Message
    box.innerHTML += `<div style="text-align:right;"><span style="background:#eee; padding:8px; border-radius:10px; display:inline-block;">${message}</span></div>`;
    input.value = '';

    try {
        // Matches your __init__.py prefix: /api
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        
        // Show AI Response
        box.innerHTML += `<div style="text-align:left;"><span style="background:#ffebee; padding:8px; border-radius:10px; border-left:3px solid #E70013; display:inline-block;">${data.reply}</span></div>`;
        box.scrollTop = box.scrollHeight;
    } catch (err) {
        box.innerHTML += `<div style="color:red; font-size:0.8em; text-align:center;">Guide is currently offline.</div>`;
    }
}

loadVenues();