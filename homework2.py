def convert_string(data):
    result = []
    for word in data.split(" "):
        result_word = []
        for i, c in enumerate(word):
            if i % 2 == 0:
                result_word.append(c.upper())
            else:
                result_word.append(c.lower())
        result.append("".join(result_word))
    return " ".join(result)


def main():
    print(convert_string(data="String"))
    print(convert_string(data="Weird string case"))


if __name__ == "__main__":
    main()
