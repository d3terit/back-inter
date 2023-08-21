from flask import Flask, request, jsonify
import json
import spacy
from spellchecker import SpellChecker

app = Flask(__name__)

# Carga el modelo de lenguaje de spaCy en español
nlp = spacy.load("es_core_news_sm")
spell = SpellChecker(language='es')

# Diccionario de palabras disponibles
available_words = {
    "hola": "hola",
    "nombre": "nombre",
    "a": "a",
    "b": "b",
    "c": "c",
    "d": "d",
    "e": "e",
    "f": "f",
    "g": "g",
    "h": "h",
    "i": "i",
    "j": "j",
    "k": "k",
    "l": "l",
    "ll": "ll",
    "m": "m",
    "n": "n",
    "ñ": "ñ",
    "o": "o",
    "p": "p",
    "q": "q",
    "r": "r",
    "rr": "rr",
    "s": "s",
    "t": "t",
    "u": "u",
    "v": "v",
    "w": "w",
    "x": "x",
    "y": "y",
    "z": "z",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9"
}

not_active_words = {
    "es": "es",
    "la": "la",
    "los": "los",
    "de": "de",
}

def translate_to_array(sign_language_phrase):
    doc = nlp(sign_language_phrase)
    translated_array = []

    corrected_tokens = [{
                        "idx":token.idx,
                        "token":token,
                        "text":spell.correction(token.text.lower())} 
                for token in doc]

    cleaned_tokens = [item for item in corrected_tokens if not item['token'].is_punct]

    for item in cleaned_tokens:
        if item["text"] in available_words:
            translated_array.append({"ref":item["idx"],"sing":available_words[item["text"]]})
        else:
            if item["text"] in not_active_words: 
                continue
            for char in item["text"]:
                if char in available_words:
                    translated_array.append({"ref":item["idx"],"sing":available_words[char]})
    return json.dumps(translated_array)


@app.route("/")
def hello_world():
    return "funcionando"
    

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        input_phrase = data.get("phrase", "")
        if input_phrase:
            translated_result = translate_to_array(input_phrase)
            return jsonify({"result": translated_result}), 200
        else:
            return jsonify({"error": "No input phrase provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
