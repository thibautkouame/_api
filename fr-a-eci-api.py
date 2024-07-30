from flask import Flask, request, jsonify
import random
import difflib

app = Flask(__name__)

# Dictionnaires de traduction avec regroupement de synonymes
translations_fr_to_dyu = {
    ("bonjour", "hey", "salut"): ["a ni sogôman"],
    "merci": ["anitcher"],
    "Bonsoir": ["aniouhoula"],
    "Comment vas-tu ?": ["i ka kene wâ?"],
    # Ajoutez plus de traductions ici
}

translations_dyu_to_fr = {
    "a ni sogôman": ["Bonjour", "Salut"],
    "aniouhoula": ["Bonsoir"],
    "anitcher": ["Merci"],
    "i ka kene wa?": ["Comment vas-tu ?"],
    # Ajoutez plus de traductions ici
}

translations_fr_to_agni = {
   ("bonjour", "hey", "salut"): ["Agni ohoo"],
    "merci": ["mohoau"],
    "Bonsoir": ["agni ohoo"],
    "Comment vas-tu ?": ["ahoun ti sè ?"],
    # Ajoutez plus de traductions ici
}

translations_agni_to_fr = {
    "Agni ohoo": ["Bonjour", "Salut"],
    "mohoau": ["Merci"],
    "ahoun ti sè ?": ["Comment vas-tu ?"],
    # Ajoutez plus de traductions ici
}

translations_agni_to_dyu = {
    "Agni ohoo": ["a ni sogôman"],
    "mohoau": ["anitcher"],
    "ahoun ti sè ?": ["i ka kene wa?"],
    # Ajoutez plus de traductions ici
}

translations_dyu_to_agni = {
    "a ni sogôman": ["Agni ohoo"],
    "mohoau": ["anitcher"],
    "i ka kene wa?": ["ahoun ti sè ?"],
    # Ajoutez plus de traductions ici
}

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    source = data.get('source')
    target = data.get('target')

    def get_best_match(dictionary, text):
        all_keys = [key for key_group in dictionary.keys() for key in (key_group if isinstance(key_group, tuple) else (key_group,))]
        closest_matches = difflib.get_close_matches(text.lower(), all_keys, n=1, cutoff=0.5)
        if closest_matches:
            best_match = closest_matches[0]
            for key, values in dictionary.items():
                if best_match in (key if isinstance(key, tuple) else (key,)):
                    return random.choice(values)
        return "Traduction non trouvée"

    if source == 'fr' and target == 'dyu':
        translated_text = get_best_match(translations_fr_to_dyu, text)
    elif source == 'dyu' and target == 'fr':
        translated_text = get_best_match(translations_dyu_to_fr, text)
    elif source == 'fr' and target == 'agni':
        translated_text = get_best_match(translations_fr_to_agni, text)
    elif source == 'agni' and target == 'fr':
        translated_text = get_best_match(translations_agni_to_fr, text)
    elif source == 'agni' and target == 'dyu':
        translated_text = get_best_match(translations_agni_to_dyu, text)
    elif source == 'dyu' and target == 'agni':
        translated_text = get_best_match(translations_dyu_to_agni, text)
    else:
        return jsonify({'error': 'Langue source ou cible non supportée'}), 400
    
    return jsonify({'translatedText': translated_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
