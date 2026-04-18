def add(numbers):
    if numbers == "":
        return 0

    delimiter = None
    body = numbers
    if numbers.startswith("//"):
        delimiter, body = _parse_header(numbers)

    tokens, separator_errors = _tokenize(body, delimiter)
    negatives = [str(number) for number in tokens if number < 0]
    errors = []
    if negatives:
        errors.append(f"Negative number(s) not allowed: {', '.join(negatives)}")
    errors.extend(separator_errors)
    if errors:
        raise ValueError("\n".join(errors))

    return sum(number for number in tokens if number <= 1000)


def _parse_header(numbers):
    header, body = numbers[2:].split("\n", 1)
    return header, body


def _tokenize(body, delimiter):
    tokens = []
    errors = []
    current = []
    index = 0
    length = len(body)

    while index < length:
        if delimiter and body.startswith(delimiter, index):
            _append_token(tokens, current, errors, "Number expected but EOF found.")
            current = []
            index += len(delimiter)
            continue

        char = body[index]
        if delimiter is None and char in {",", "\n"}:
            _append_token(tokens, current, errors, "Number expected but EOF found.")
            current = []
            index += 1
            continue

        if delimiter is not None and char in {",", "\n"}:
            errors.append(
                f"'{delimiter}' expected but '{char}' found at position {index}."
            )
            _append_token(tokens, current, errors, "Number expected but EOF found.")
            current = []
            index += 1
            continue

        current.append(char)
        index += 1

    _append_token(tokens, current, errors, "Number expected but EOF found.")
    return tokens, errors


def _append_token(tokens, current, errors, empty_token_message):
    if not current:
        errors.append(empty_token_message)
        return

    tokens.append(int("".join(current)))
