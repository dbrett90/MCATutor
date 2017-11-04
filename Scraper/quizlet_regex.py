import re
from orderedset import OrderedSet


question_pattern = "^(?!\n[Aa].*\n[Bb][\w\s\W]*$).*"

choice_patterns = ["\n[Aa].*\n[Bb]",
                   "\n[Bb].*\n[Cc]",
                   "\n[Cc].*\n[Dd]",
                   "\n[Dd].*\n[Ee]",
                   "\n[Dd].*",
                   "\n[Ee].*"]

strip_patterns = ["[ABCDEabcde]\..*", "[ABCDEabcde].*"]

answer_pattern = "^(?![ABCDEabcde]{1}\.*\s*$).*"


def get_question(question):
    matchObject = re.search(question_pattern, question, flags=0)
    if matchObject:
        return matchObject.group(0)


def get_options(question):
    choices_raw = []
    choices = OrderedSet()
    for pattern in choice_patterns:
        matchObject = re.search(pattern, question, flags=0)
        if matchObject:
            match = matchObject.group(0)
            if match[-2] == '\n':
                choices_raw.append(match[1:-2])
            else:
                choices_raw.append(match[1:])

    for i in range(len(choices_raw)):
        matchObject = re.search(strip_patterns[0],
                                choices_raw[i],
                                flags=0)
        if matchObject:
            choices.add(matchObject.group(0)[3:])
        else:
            matchObject = re.search(strip_patterns[1],
                                    choices_raw[i],
                                    flags=0)
            if matchObject:
                choices.add(matchObject.group(0)[2:])

    return list(choices)


def get_answer(definition):
    matchObject = re.search(answer_pattern, definition, flags=0)
    if matchObject:
        return matchObject.group(0)
