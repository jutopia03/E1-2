"""프로그램 시작 지점. `python main.py`로 실행한다."""

from quiz_game import QuizGame


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()