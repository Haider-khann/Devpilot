with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add quality model section after language classifier
old = "            <div class=\"card\">\n                <div class=\"card-title\" style=\"margin-bottom:8px;\">Test Prediction</div>"
new = """            <div class="card">
                <div class="card-header"><div><div class="card-title">Quality Predictor</div><div class="card-subtitle">ML model that scores code quality</div></div><button onclick="trainQualityModel()">Train Quality Model</button></div>
                <div id="mlQualityTrainResult"></div>
            </div>
            <div class="card">
                <div class="card-title" style="margin-bottom:8px;">Test Quality</div>
                <textarea id="mlQualityInput" placeholder="Paste code to score quality..."></textarea>
                <button onclick="predictQuality()" style="margin-top:8px;">Predict Quality</button>
                <div id="mlQualityResult"></div>
            </div>
            <div class="card">
                <div class="card-title" style="margin-bottom:8px;">Test Prediction</div>"""

content = content.replace(old, new)

# Add quality functions
old_func = "        async function predictLanguage() {"
new_funcs = """        async function trainQualityModel() {
            const div = document.getElementById('mlQualityTrainResult');
            div.innerHTML = '<p style="color:var(--text-secondary);">Training...</p>';
            try {
                const res = await fetch(API + '/api/ml/train-quality', {method:'POST'});
                const data = await res.json();
                let featuresHtml = '';
                if (data.top_features) {
                    featuresHtml = '<div style="margin-top:8px;"><strong>Top Features:</strong><br>';
                    data.top_features.forEach(f => {
                        featuresHtml += f.feature + ': ' + f.importance + '%<br>';
                    });
                    featuresHtml += '</div>';
                }
                div.innerHTML = '<div style="font-size:13px;margin-top:8px;">Accuracy: <strong>' + data.accuracy + '%</strong>' + featuresHtml + '</div>';
            } catch(e) { div.innerHTML = '<p style="color:var(--danger);">Failed.</p>'; }
        }
        
        async function predictQuality() {
            const code = document.getElementById('mlQualityInput').value;
            const div = document.getElementById('mlQualityResult');
            if (!code.trim()) return;
            try {
                const res = await fetch(API + '/api/ml/predict-quality', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({code})});
                const data = await res.json();
                if (data.error) { div.innerHTML = '<p style="color:var(--danger);margin-top:8px;">' + data.error + '</p>'; return; }
                const score = data.quality_score;
                const color = score > 70 ? 'var(--success)' : score > 40 ? 'var(--warning)' : 'var(--danger)';
                div.innerHTML = '<div style="margin-top:8px;padding:12px;background:var(--surface-hover);border-radius:6px;font-size:13px;"><div>Quality Score: <strong style="color:' + color + ';">' + score + '/100</strong></div><div>Label: <strong>' + data.label + '</strong></div><div style="margin-top:4px;">' + data.recommendation + '</div></div>';
            } catch(e) { div.innerHTML = '<p style="color:var(--danger);margin-top:8px;">Failed.</p>'; }
        }
        
        async function predictLanguage() {"""

content = content.replace(old_func, new_funcs)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Quality model added to frontend!")