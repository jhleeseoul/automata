# 파싱 테이블을 딕셔너리로 정의 (수정된 테이블 사용)
parsing_table = {
    'E': {
        '(': 'E->TB', 'a': 'E->TB', 'b': 'E->TB', 'c': 'E->TB', 'd': 'E->TB',
        'x': 'E->TB', 'y': 'E->TB', 'z': 'E->TB', '1': 'E->TB', '2': 'E->TB',
        '3': 'E->TB', '4': 'E->TB', '5': 'E->TB', '6': 'E->TB', '7': 'E->TB',
        '8': 'E->TB', '9': 'E->TB'
    },
    'B': {
        '+': 'B->+TB', '-': 'B->-TB', '#': 'B->e', ')': 'B->e'
    },
    'T': {
        '(': 'T->FC', 'a': 'T->FC', 'b': 'T->FC', 'c': 'T->FC', 'd': 'T->FC',
        'x': 'T->FC', 'y': 'T->FC', 'z': 'T->FC', '1': 'T->FC', '2': 'T->FC',
        '3': 'T->FC', '4': 'T->FC', '5': 'T->FC', '6': 'T->FC', '7': 'T->FC',
        '8': 'T->FC', '9': 'T->FC'
    },
    'C': {
        '*': 'C->*FC', '/': 'C->/FC', '#': 'C->e', ')': 'C->e', '+': 'C->e', '-': 'C->e'
    },
    'F': {
        '(': 'F->(E)', 'a': 'F->A', 'b': 'F->A', 'c': 'F->A', 'd': 'F->A',
        'x': 'F->A', 'y': 'F->A', 'z': 'F->A', '1': 'F->A', '2': 'F->A',
        '3': 'F->A', '4': 'F->A', '5': 'F->A', '6': 'F->A', '7': 'F->A',
        '8': 'F->A', '9': 'F->A'
    },
    'A': {
        'a': 'A->a', 'b': 'A->b', 'c': 'A->c', 'd': 'A->d',
        'x': 'A->x', 'y': 'A->y', 'z': 'A->z',
        '1': 'A->1', '2': 'A->2', '3': 'A->3', '4': 'A->4',
        '5': 'A->5', '6': 'A->6', '7': 'A->7', '8': 'A->8', '9': 'A->9'
    }
}



def parse_string(input_string):
    """주어진 입력 문자열을 파싱하여 파생 과정을 출력하는 함수"""
    input_string += '#'  # 입력의 끝을 나타내는 기호 추가
    stack = ['#', 'E']  # 초기 스택: 끝 기호와 시작 비터미널
    index = 0  # 입력 문자열의 현재 위치
    current_derivation = 'E'  # 현재 파생 상태
    derivation_steps = []  # 파생 과정을 저장할 리스트

    # 초기 상태 저장
    derivation_steps.append(current_derivation)

    # 스택이 빌 때까지 반복
    while stack:
        top = stack.pop()  # 스택의 상단 요소를 꺼냄
        current_char = input_string[index]  # 현재 입력 문자

        # 스택의 상단이 터미널이면 입력 문자와 비교
        if top == current_char:
            index += 1  # 입력의 다음 문자로 이동
            if current_char == '#':  # 입력이 끝났으면 성공적으로 수용
                for step in derivation_steps:
                    print(step)
                return
        # 스택의 상단이 비터미널인 경우 파싱 테이블 참조
        elif top in parsing_table and current_char in parsing_table[top]:
            rule = parsing_table[top][current_char]  # 적용할 규칙 가져오기
            _, expansion = rule.split('->')  # 규칙에서 확장 부분 분리

            # e(ε)는 출력하지 않음
            if expansion != 'e':
                current_derivation = current_derivation.replace(top, expansion, 1)  
            else:
                current_derivation = current_derivation.replace(top, '', 1)
            derivation_steps.append(f"=>{current_derivation}")

            # 확장된 비터미널을 스택에 푸시 (역순으로)
            for symbol in reversed(expansion):
                if symbol != 'e':  # ε는 스택에 추가하지 않음
                    stack.append(symbol)
        else:
            # 적용 가능한 규칙이 없을 경우
            print("reject")
            return

    # 입력이 끝나지 않거나 파싱이 완료되지 않은 경우
    print("reject")


# 표준 입력 처리
if __name__ == "__main__":
    n = int(input().strip())  # 첫 줄에서 입력 문자열의 길이 읽기 (사용되지 않음)
    input_string = input().strip()  # 두 번째 줄에서 실제 입력 문자열 읽기
    parse_string(input_string)  # 파싱 함수 호출
