from dataclasses import dataclass

@dataclass
class Prompt:
    '''
    A pair of strings consisting of a question and an answer that are found
    on dating profiles
    '''
    question: str
    answer: str

    def to_dict(self) -> dict:
        """Convert prompt to dictionary format"""
        return {
            "question": self.question,
            "answer": self.answer
        }