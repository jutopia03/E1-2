"""퀴즈 게임 전체 흐름(메뉴 표시, 입력 처리, 기능 실행, 저장/불러오기)을 관리하는 모듈."""
import random
import json
from pathlib import Path

from default_quizzes import create_default_quizzes
from quiz import Quiz

LINE = "=" * 40
# 실행 위치(현재 폴더)와 상관없이 항상 이 파일이 있는 폴더(프로젝트 루트)의 state.json을 사용한다.
STATE_FILE = Path(__file__).resolve().parent / "state.json"


class QuizGame:
    """메뉴를 보여주고, 사용자의 선택에 따라 각 기능을 실행하는 클래스."""

    MENU_ITEMS = ("퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료")

    def __init__(self):
        self.quizzes = create_default_quizzes()  # Quiz 객체들의 리스트
        self.best_score = None    # 최고 점수 (100점 만점 환산). 아직 안 풀었으면 None
        self.best_correct = None  # 최고 점수를 냈을 때 맞힌 문제 수
        self.best_total = None    # 최고 점수를 냈을 때 푼 문제 수

    # ------------------------------------------------------------------
    # 메인 루프 / 메뉴
    # ------------------------------------------------------------------
    def run(self):
        """프로그램의 메인 루프. '종료'를 고르거나 입력이 중단될 때까지 반복한다."""
        self.load_state()
        try:
            while True:
                self.show_menu()
                choice = self.read_number("선택: ", 1, len(self.MENU_ITEMS))
                if choice == len(self.MENU_ITEMS):
                    self.save_state()
                    print("👋 게임을 종료합니다.")
                    break
                self.handle_choice(choice)
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C(KeyboardInterrupt) 또는 입력 스트림 종료(EOFError) 시 비정상 종료 방지
            print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
            self.save_state()

    def show_menu(self):
        """메뉴 화면을 출력한다."""
        print()
        print(LINE)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        for number, item in enumerate(self.MENU_ITEMS, start=1):
            print(f"{number}. {item}")
        print(LINE)

    def handle_choice(self, choice):
        """선택한 메뉴 번호에 맞는 기능을 실행한다."""
        if choice == 1:
            self.play_quiz()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.show_quiz_list()
        elif choice == 4:
            print("\n🚧 점수 확인 기능은 준비 중입니다.")

    # ------------------------------------------------------------------
    # 퀴즈 풀기
    # ------------------------------------------------------------------
    def play_quiz(self):
        """저장된 퀴즈를 차례로 출제하고 결과를 보여준다. 결과 (맞힌 수, 푼 수, 점수)를 반환한다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return None

                # 보너스: 풀 문제 수 선택 + 랜덤 출제
        count = self.read_number(f"몇 문제를 풀까요? (1-{len(self.quizzes)}): ", 1, len(self.quizzes))
        # random.sample: 원본 리스트는 그대로 두고, 무작위 순서로 count개를 뽑은 '새 리스트'를 만든다.
        selected = random.sample(self.quizzes, count)
        total = len(selected)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct = 0
        for number, quiz in enumerate(selected, start=1):
            print()
            print("-" * 40)
            quiz.display(number)
            user_answer = self.read_number(f"정답 입력 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                answer_text = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({answer_text}) 입니다.")

        score = self.calculate_score(correct, total)
        self.show_result(correct, total, score)
        return correct, total, score

    def calculate_score(self, correct, total):
        """맞힌 수를 100점 만점 점수로 환산한다. (소수점 이하 버림)"""
        return correct * 100 // total

    def show_result(self, correct, total, score):
        """퀴즈 결과를 출력한다."""
        print()
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print(LINE)
    # ------------------------------------------------------------------
    # 퀴즈 추가
    # ------------------------------------------------------------------
    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록하고 파일에 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.read_text("문제를 입력하세요: ")

        choices = []
        while len(choices) < Quiz.CHOICE_COUNT:
            choice = self.read_text(f"선택지 {len(choices) + 1}: ")
            if choice in choices:  # 같은 선택지가 두 번 들어가면 정답이 모호해진다
                print("⚠️ 이미 입력한 선택지입니다. 다른 내용을 입력하세요.")
                continue
            choices.append(choice)

        answer = self.read_number(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)

        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print("\n✅ 퀴즈가 추가되었습니다! (저장 완료)")
        else:
            print("\n✅ 퀴즈가 추가되었습니다. (파일 저장은 실패해 이번 실행 중에만 유지됩니다)")
    # ------------------------------------------------------------------
    # 퀴즈 목록
    # ------------------------------------------------------------------
    def show_quiz_list(self):
        """등록된 퀴즈의 문제 목록을 번호와 함께 출력한다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)
    # ------------------------------------------------------------------
    # 입력 처리
    # ------------------------------------------------------------------
    def read_number(self, prompt, min_value, max_value):
        """min_value~max_value 범위의 정수를 입력받을 때까지 반복해서 묻는다."""
        error_message = f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요."
        while True:
            raw = input(prompt).strip()  # 앞뒤 공백 제거
            if raw == "":
                print(f"⚠️ 입력이 비어 있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue
            try:
                number = int(raw)
            except ValueError:  # 'abc'처럼 숫자로 바꿀 수 없는 경우
                print(error_message)
                continue
            if not min_value <= number <= max_value:  # 범위 밖 숫자
                print(error_message)
                continue
            return number
    def read_text(self, prompt):
        """비어 있지 않은 문자열을 입력받을 때까지 반복해서 묻는다. 앞뒤 공백은 제거한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")
                continue
            return text

    # ------------------------------------------------------------------
    # 파일 저장 / 불러오기 (state.json)
    # ------------------------------------------------------------------
    def load_state(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다. 없거나 손상됐으면 기본 데이터를 사용한다."""
        if not STATE_FILE.exists():
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score, best_correct, best_total = self._parse_best(data)
        except (ValueError, KeyError, TypeError):
            # ValueError: JSON 문법 오류(JSONDecodeError), 인코딩 오류, Quiz.from_dict 검증 실패
            # KeyError: "quizzes" 키가 없음 / TypeError: 최상위가 dict가 아니거나 quizzes가 리스트가 아님
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈 데이터로 복구합니다.")
            self._reset_to_default()
            self.save_state()
            return
        except OSError:
            # 권한 문제 등으로 파일을 열 수 없는 경우
            print("⚠️ 저장 파일을 읽을 수 없어 기본 퀴즈로 시작합니다.")
            return

        self.quizzes = quizzes
        self.best_score = best_score
        self.best_correct = best_correct
        self.best_total = best_total
        score_text = "기록 없음" if best_score is None else f"{best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text})")

    def save_state(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장한다. 성공하면 True."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                # ensure_ascii=False: 한글을 \uXXXX가 아닌 그대로 저장 / indent=4: 사람이 읽기 쉽게
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("⚠️ 데이터를 저장하지 못했습니다.")
            return False
        return True

    def _parse_best(self, data):
        """최고 점수 관련 값 3개를 꺼내 검증한다. 형식이 잘못되면 ValueError."""
        best_score = data.get("best_score")
        best_correct = data.get("best_correct")
        best_total = data.get("best_total")
        if best_score is None:  # 아직 한 번도 안 푼 상태
            return None, None, None
        values = (best_score, best_correct, best_total)
        if any(isinstance(v, bool) or not isinstance(v, int) for v in values):
            raise ValueError("최고 점수 데이터는 정수여야 합니다.")
        if not (0 <= best_score <= 100 and 0 <= best_correct <= best_total and best_total >= 1):
            raise ValueError("최고 점수 데이터의 범위가 올바르지 않습니다.")
        return best_score, best_correct, best_total

    def _reset_to_default(self):
        """퀴즈와 점수를 기본 상태로 되돌린다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None