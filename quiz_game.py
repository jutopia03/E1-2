"""퀴즈 게임 전체 흐름(메뉴 표시, 입력 처리, 기능 실행)을 관리하는 모듈."""
from default_quizzes import create_default_quizzes

LINE = "=" * 40


class QuizGame:
    """메뉴를 보여주고, 사용자의 선택에 따라 각 기능을 실행하는 클래스."""

    MENU_ITEMS = ("퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료")

    def __init__(self):
        self.quizzes = create_default_quizzes()  # Quiz 객체들의 리스트

    def run(self):
        """프로그램의 메인 루프. '종료'를 고르거나 입력이 중단될 때까지 반복한다."""
        try:
            while True:
                self.show_menu()
                choice = self.read_number("선택: ", 1, len(self.MENU_ITEMS))
                if choice == len(self.MENU_ITEMS):
                    print("👋 게임을 종료합니다.")
                    break
                self.handle_choice(choice)
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C(KeyboardInterrupt) 또는 입력 스트림 종료(EOFError) 시 비정상 종료 방지
            print("\n\n⚠️ 입력이 중단되어 프로그램을 안전하게 종료합니다.")

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
            print("\n🚧 퀴즈 풀기 기능은 준비 중입니다.")
        elif choice == 2:
            print("\n🚧 퀴즈 추가 기능은 준비 중입니다.")
        elif choice == 3:
            print("\n🚧 퀴즈 목록 기능은 준비 중입니다.")
        elif choice == 4:
            print("\n🚧 점수 확인 기능은 준비 중입니다.")

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