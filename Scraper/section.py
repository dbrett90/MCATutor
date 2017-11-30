class Section:

    """A section with questions pertaining to a subject."""

    def __init__(self, subject, questions):
        self._subject = subject
        self._questions = questions

    def subject(self):
        return self._subject

    def questions(self):
        return self._questions
