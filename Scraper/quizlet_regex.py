import re
from orderedset import OrderedSet

question_pattern = "^(?!\n\s*[Aa].*\n*\s*.*\n*\s*[Bb][\w\s\W]*$).*"

choice_patterns = ["\n\s*[Aa][.\s\n]+.*\n*\s*[Bb]",
                   "\n\s*[Bb][.\s\n]+.*\n*\s*[Cc]",
                   "\n\s*[Cc][.\s\n]+.*\n*\s*[Dd]",
                   "\n\s*[Dd][.\s\n]+.*\s*\n*",
                   "\n\s*[Ee][.\s]+.*\s*\n*"]

strip_patterns = ["[ABCDEabcde][\.\)]+.*", "[ABCDEabcde].*"]

answer_pattern = "^(?![ABCDEabcde]{1}\.*\s*$).*"

expl_pattern = "\n([\w\s\n\W]*)"


def get_question_mc(question):
    matchObject = re.search(question_pattern, question, flags=0)
    if matchObject:
        return matchObject.group(0)


def get_choices_mc(question):
    choices_raw = []
    choices = OrderedSet()
    for pattern in choice_patterns:
        matchObject = re.search(pattern, question, flags=0)
        if matchObject:
            match = matchObject.group(0)
            choices_raw.append(match[1:])

    for i in range(len(choices_raw)):
        matchObject = re.search(strip_patterns[0],
                                choices_raw[i],
                                flags=0)
        if matchObject:
            choices.add(matchObject.group(0)[3:].strip())
        else:
            matchObject = re.search(strip_patterns[1],
                                    choices_raw[i],
                                    flags=0)
            if matchObject:
                choices.add(matchObject.group(0)[1:].strip())

    return list(choices)


def get_answer_mc(definition):
    matchObject = re.search(answer_pattern, definition, flags=0)
    if matchObject:
        return matchObject.group(0).strip()


def get_expl_mc(definition):
    matchObject = re.search(expl_pattern, definition, flags=0)
    if matchObject:
        if matchObject.group(1):
            return matchObject.group(1).strip()
    else:
        return ''


def get_question_id(question):
    q, a = question['term'], question['definition']
    q_mc = all(re.search(p, q, flags=0) for p in choice_patterns[:1])
    a_mc = all(re.search(p, a, flags=0) for p in choice_patterns[:1])

    if not (q_mc or a_mc):
        return q, a
    else:
        return None, None
