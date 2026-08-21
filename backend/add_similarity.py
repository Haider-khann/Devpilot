with open('ml_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add TF-IDF import
content = content.replace("from sklearn.metrics import accuracy_score", "from sklearn.metrics import accuracy_score\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.metrics.pairwise import cosine_similarity")

# Add similarity methods before get_sample_training_data
old = "    def get_sample_training_data(self):"
new = """    def find_similar_code(self, code1, code2):
        \"\"\"Calculate similarity between two code snippets using TF-IDF.\"\"\"
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))
        try:
            tfidf = vectorizer.fit_transform([code1, code2])
            similarity = cosine_similarity(tfidf[0], tfidf[1])[0][0]
            return round(similarity * 100, 2)
        except:
            return 0.0
    
    def detect_duplicates(self, code_snippets):
        \"\"\"Find duplicate code among multiple snippets.\"\"\"
        if len(code_snippets) < 2:
            return []
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))
        tfidf = vectorizer.fit_transform(code_snippets)
        similarities = cosine_similarity(tfidf)
        duplicates = []
        for i in range(len(code_snippets)):
            for j in range(i+1, len(code_snippets)):
                sim = similarities[i][j] * 100
                if sim > 60:
                    duplicates.append({'index1': i, 'index2': j, 'similarity': round(sim, 2)})
        return duplicates
    
    def get_sample_training_data(self):"""

content = content.replace(old, new)

with open('ml_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Similarity detection added!")