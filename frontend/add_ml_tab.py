with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add ML nav item
content = content.replace(
    '<div class="nav-item" data-page="ai" onclick="switchPage(\'ai\')"><span class="nav-icon">✦</span><span>AI Assistant</span></div>',
    '<div class="nav-item" data-page="ai" onclick="switchPage(\'ai\')"><span class="nav-icon">✦</span><span>AI Assistant</span></div>\n            <div class="nav-item" data-page="ml" onclick="switchPage(\'ml\')"><span class="nav-icon">◈</span><span>ML Models</span></div>'
)

# Add ML page before Contact page
content = content.replace(
    '<div class="page" id="page-contact">',
    '<div class="page" id="page-ml">\n            <h2 class="page-title">Machine Learning Models</h2>\n            <p class="page-subtitle">Custom-trained models for code intelligence</p>\n            <div class="card">\n                <div class="card-header"><div><div class="card-title">Language Classifier</div><div class="card-subtitle">Detects programming language from code structure</div></div><button onclick="trainModel()">Train Model</button></div>\n                <div id="mlTrainResult"></div>\n            </div>\n            <div class="card">\n                <div class="card-title" style="margin-bottom:8px;">Test Prediction</div>\n                <textarea id="mlTestInput" placeholder="Paste code to classify..."></textarea>\n                <button onclick="predictLanguage()" style="margin-top:8px;">Predict Language</button>\n                <div id="mlPredictResult"></div>\n            </div>\n        </div>\n        <div class="page" id="page-contact">'
)

# Add ML functions before loadRepos
content = content.replace(
    "        loadRepos(); loadStats();",
    """        async function trainModel() {
            const div = document.getElementById('mlTrainResult');
            div.innerHTML = '<p style="color:var(--text-secondary);">Training model...</p>';
            try {
                const res = await fetch(API + '/api/ml/train', {method:'POST'});
                const data = await res.json();
                div.innerHTML = '<div style="margin-top:8px;font-size:13px;"><div>Status: <strong style="color:var(--success);">' + data.status + '</strong></div><div>Accuracy: <strong>' + data.accuracy + '%</strong></div><div>Training Samples: ' + data.training_samples + '</div><div>Test Samples: ' + data.test_samples + '</div></div>';
            } catch(e) { div.innerHTML = '<p style="color:var(--danger);">Training failed.</p>'; }
        }
        
        async function predictLanguage() {
            const code = document.getElementById('mlTestInput').value;
            const div = document.getElementById('mlPredictResult');
            if (!code.trim()) return;
            try {
                const res = await fetch(API + '/api/ml/predict-language', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({code})});
                const data = await res.json();
                if (data.error) { div.innerHTML = '<p style="color:var(--danger);margin-top:8px;">' + data.error + '</p>'; return; }
                div.innerHTML = '<div style="margin-top:8px;padding:12px;background:var(--surface-hover);border-radius:6px;font-size:13px;"><div>Language: <strong>' + data.predicted_language + '</strong></div><div>Confidence: <strong>' + data.confidence + '%</strong></div></div>';
            } catch(e) { div.innerHTML = '<p style="color:var(--danger);margin-top:8px;">Prediction failed.</p>'; }
        }
        
        loadRepos(); loadStats();"""
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("ML tab added to frontend!")