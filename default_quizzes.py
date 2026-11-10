"""state.json이 없거나 손상됐을 때 사용하는 기본 퀴즈 데이터 (주제: Python/프로그래밍 기초)."""

from quiz import Quiz


def create_default_quizzes():
    """기본 퀴즈 목록을 Quiz 객체의 리스트로 만들어 반환한다."""
    return [
        Quiz(
            "Python에서 3.0 의 자료형(type)은?",
            ["int", "str", "float", "bool"],
            3,
        ),
        Quiz(
            "a = [10, 20, 30] 일 때, a[-1] 의 값은?",
            ["10", "30", "-1", "IndexError 발생"],
            2,
        ),
        Quiz(
            "다음 중 한 번 만든 뒤 내용을 바꿀 수 없는(immutable) 자료형은?",
            ["list", "dict", "set", "tuple"],
            4,
        ),
        Quiz(
            "7 // 2 의 결과는?",
            ["3", "3.5", "4", "1"],
            1,
        ),
        Quiz(
            "함수 안에서 값을 호출한 쪽으로 돌려줄 때 사용하는 키워드는?",
            ["break", "return", "pass", "continue"],
            2,
        ),
        Quiz(
            'd = {"a": 1} 일 때, "a" in d 의 결과는?',
            ["True", "False", "1", "KeyError 발생"],
            1,
        ),
        Quiz(
            "bool(\"\") (빈 문자열을 bool로 변환)의 결과는?",
            ["True", "False", "None", "ValueError 발생"],
            2,
        ),
        Quiz(
            "Git에서 변경한 파일을 다음 커밋에 포함되도록 스테이징하는 명령어는?",
            ["git commit", "git push", "git add", "git init"],
            3,
        ),
    ]