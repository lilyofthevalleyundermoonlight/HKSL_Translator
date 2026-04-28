import os
import sys
import json
import re

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

with open(get_resource_path("data/dictionary.json"), "r", encoding="utf-8") as f:
    DICTIONARY = json.load(f)

BASE_STOPWORDS = {
    "a", "an", "the", "is", "am", "are", "was", "were",
    "to", "of", "in", "on", "at", "for", "and", "or",
    "but", "do", "does", "did", "be", "being", "been"
}

FALLBACK_MAP = {
    "she": "he",
    "her": "his",
    "hers": "his",
    "i": "myself",
    "me": "myself"
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_word(word):
    if word in DICTIONARY:
        return word

    if word.endswith("ies") and len(word) > 3:
        candidate = word[:-3] + "y"
        if candidate in DICTIONARY:
            return candidate

    if word.endswith("es") and len(word) > 2:
        candidate = word[:-2]
        if candidate in DICTIONARY:
            return candidate

    if word.endswith("s") and len(word) > 1:
        candidate = word[:-1]
        if candidate in DICTIONARY:
            return candidate

    if word.endswith("ing") and len(word) > 4:
        candidate = word[:-3]
        if candidate in DICTIONARY:
            return candidate

        candidate = word[:-3] + "e"
        if candidate in DICTIONARY:
            return candidate

        if len(word) >= 5 and word[-4] == word[-5]:
            candidate = word[:-4]
            if candidate in DICTIONARY:
                return candidate

    if word.endswith("ed") and len(word) > 3:
        candidate = word[:-2]
        if candidate in DICTIONARY:
            return candidate

        candidate = word[:-1]
        if candidate in DICTIONARY:
            return candidate

        candidate = word[:-2] + "e"
        if candidate in DICTIONARY:
            return candidate

        if len(word) >= 4 and word[-3] == word[-4]:
            candidate = word[:-3]
            if candidate in DICTIONARY:
                return candidate

    return word


def text_to_sign_info(text):
    text = clean_text(text)
    words = text.split()
    results = []

    phrase_keys = [key for key in DICTIONARY.keys() if " " in key]
    phrase_keys.sort(key=lambda x: len(x.split()), reverse=True)

    i = 0
    while i < len(words):
        matched = False

        for phrase in phrase_keys:
            phrase_words = phrase.split()
            n = len(phrase_words)

            if i + n <= len(words):
                chunk = " ".join(words[i:i+n])

                if chunk == phrase:
                    results.append(DICTIONARY[phrase])
                    i += n
                    matched = True
                    break

        if matched:
            continue

        single_word = words[i]

        if single_word in BASE_STOPWORDS:
            i += 1
            continue

        normalized = normalize_word(single_word)

        if normalized in DICTIONARY:
            results.append(DICTIONARY[normalized])

        elif single_word in FALLBACK_MAP:
            fallback = FALLBACK_MAP[single_word]

            if fallback in DICTIONARY:
                results.append(DICTIONARY[fallback])

        i += 1

    return results