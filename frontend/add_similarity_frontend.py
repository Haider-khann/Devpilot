with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add similarity card before the Test Prediction card
old = "            <div class=\"card\">\n                <div class=\"card-title\" style=\"margin-bottom:8px;\">Test Prediction</div>"
new = """            <div class="card">
                <div class="card-header"><div><div class="card-title">Code Similarity Detector</div><div class="card-subtitle">TF-IDF based duplicate detection</div></div></div>
                <textarea id="similarityCode1" placeholder="Paste first code sample..." style="margin-bottom:8px;"></textarea>
                <textarea id="similarityCode2" placeholder="Paste second code sample..."></textarea>
                <button onclick="checkSimilarity()" style="margin-top:8px;">Check Similarity</button>
                <div id="similarityResult"></div>
            </div>
            <div class="card">
                <div class="card-title" style="margin-bottom:8px;">Test Prediction</div>"""

content = content.replace(old, new)

# Add checkSimilarity function
old_func = "        async function predictLanguage() {"
new_func = """        async function checkSimilarity() {
            const code1 = document.getElementById('similarityCode1').value;
            const code2 = document.getElementById('similarityCode2').value;
            const div = document.getElementById('similarityResult');
            if (!code1.trim() || !code2.trim()) { div.innerHTML = '<p style="color:var(--text-secondary);margin-top:8px;">Paste both code samples.</p>'; return; }
            try {
                const res = await fetch(API + '/api/ml/similarity', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({code1, code2})});
                const data = await res.json();
                const sim = data.similarity;
                const color = sim > 60 ? 'var(--danger)' : sim > 30 ? 'var(--warning)' : 'var(--success)';
                const label = sim > 60 ? 'Duplicate detected!' : sim > 30 ? 'Somewhat similar' : 'Different code';
                div.innerHTML = '<div style="margin-top:8px;padding:12px;background:var(--surface-hover);border-radius:6px;font-size:13px;text-align:center;"><div style="font-size:24px;font-weight:600;color:' + color + ';">' + sim + '%</div><div style="margin-top:4px;">' + label + '</div></div>';
            } catch(e) { div.innerHTML = '<p style="color:var(--danger);margin-top:8px;">Failed.</p>'; }
        }
        
        async function predictLanguage() {"""

content = content.replace(old_func, new_func)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Similarity detector added to frontend!")