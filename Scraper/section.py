class Section:

    """A passage and questions pertaining to it."""

    def __init__(self, passage, questions):
        self._passage = passage
        self._questions = questions

    def passage(self):
        return self._passage

    def questions(self):
        return self._questions
