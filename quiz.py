"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제, 선택지 4개, 정답 번호(1~4)를 가진 퀴즈 한 문제."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer):
        # self는 '지금 만들어지고 있는 바로 그 객체'를 가리킨다.
        # self.xxx에 값을 넣으면 그 객체의 속성(attribute)으로 저장된다.
        self.question = question
        self.choices = list(choices)
        self.answer = answer  # 정답 번호 (1~4)

    def display(self, number=None):
        """문제와 선택지를 출력한다. number를 주면 [문제 N] 머리말을 붙인다."""
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True, 아니면 False를 반환한다."""
        return user_answer == self.answer
    def to_dict(self):
        """JSON으로 저장할 수 있도록 dict 형태로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """dict(JSON에서 읽은 값)로부터 Quiz 객체를 만든다. 형식이 잘못되면 ValueError."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터가 dict 형식이 아닙니다.")
        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")

        if not isinstance(question, str) or question.strip() == "":
            raise ValueError("문제(question)가 올바르지 않습니다.")
        if (
            not isinstance(choices, list)
            or len(choices) != cls.CHOICE_COUNT
            or not all(isinstance(c, str) and c.strip() for c in choices)
        ):
            raise ValueError("선택지(choices)는 비어 있지 않은 문자열 4개여야 합니다.")
        # bool은 int의 하위 타입이라 True가 1로 통과하지 않도록 따로 막는다.
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= cls.CHOICE_COUNT:
            raise ValueError("정답(answer)은 1~4 사이의 정수여야 합니다.")

        return cls(question, choices, answer)