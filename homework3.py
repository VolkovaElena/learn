#!/usr/bin/env python3.5
import re


def validate(word):
    result = []
    for char in word:
        if re.match(r"^[a-z]+$", char.lower()):
            result.append(char)
    return "".join(result)


def work(search, words):
    s = validate(search)
    if not s:
        return []
    result = []
    for word in words:
        w = validate(word).lower()
        if w.startswith(s.lower()):
            result.append(word)
            if len(result) >= 5:
                break

    return result


if __name__ == "__main__":
    text = ["airplane", "airport", "apple", "ball", "AI123", "aiwater", "a2i20", "$home", "item", "ice", "aid", "cat0",
            "aim"]
    print(work("12ai", text))
