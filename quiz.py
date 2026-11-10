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