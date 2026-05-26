import random
import sys
import io

# Windows 터미널 UTF-8 출력 설정
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")


def generate_secret():
    """서로 다른 3자리 숫자를 랜덤으로 생성 (0 포함, 첫 자리 0 불가)"""
    digits = list(range(10))
    first = random.choice(digits[1:])  # 첫 자리는 1~9
    digits.remove(first)
    rest = random.sample(digits, 2)
    return [first] + rest


def get_hint(secret, guess):
    """스트라이크/볼/아웃 계산"""
    strikes = sum(s == g for s, g in zip(secret, guess))
    balls = sum(g in secret for g in guess) - strikes
    return strikes, balls


def parse_input(user_input):
    """입력값 검증 및 파싱. 유효하면 int 리스트, 아니면 None 반환"""
    user_input = user_input.strip()
    if len(user_input) != 3 or not user_input.isdigit():
        return None
    digits = [int(c) for c in user_input]
    if len(set(digits)) != 3:  # 중복 숫자 불가
        return None
    if digits[0] == 0:  # 첫 자리 0 불가
        return None
    return digits


def play():
    print("=" * 40)
    print("       ⚾  숫자 야구 게임  ⚾")
    print("=" * 40)
    print("서로 다른 세 자리 숫자를 맞춰보세요!")
    print("  스트라이크(S): 숫자와 자리 모두 일치")
    print("  볼(B)        : 숫자는 있지만 자리 다름")
    print("  아웃(OUT)    : 숫자가 하나도 없음")
    print("  3S = 정답! 🎉")
    print("-" * 40)

    secret = generate_secret()
    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        remaining = max_attempts - attempts
        try:
            user_input = input(f"[{attempts + 1}/{max_attempts}] 숫자 입력 (남은 기회: {remaining}): ")
        except (EOFError, KeyboardInterrupt):
            print("\n\n게임을 종료합니다. 👋")
            return

        guess = parse_input(user_input)
        if guess is None:
            print("  ⚠  서로 다른 세 자리 숫자를 입력해주세요. (예: 123)")
            continue

        attempts += 1
        strikes, balls = get_hint(secret, guess)

        if strikes == 3:
            print(f"\n🎉 정답! {attempts}번 만에 맞췄습니다!")
            break

        if strikes == 0 and balls == 0:
            print(f"  → 아웃(OUT)")
        else:
            result_parts = []
            if strikes:
                result_parts.append(f"{strikes}S")
            if balls:
                result_parts.append(f"{balls}B")
            print(f"  → {' '.join(result_parts)}")
    else:
        answer = "".join(map(str, secret))
        print(f"\n💀 기회를 모두 사용했습니다. 정답은 [{answer}] 이었습니다.")

    print("-" * 40)
    again = input("다시 하시겠습니까? (y/n): ").strip().lower()
    if again == "y":
        print()
        play()
    else:
        print("플레이해 주셔서 감사합니다! 👋")


if __name__ == "__main__":
    play()
