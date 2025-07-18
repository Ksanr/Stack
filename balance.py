from stack import Stack

CLOSE_BRACKETS = {')': '(', '}': '{', ']': '['}

def check_balance(s: str) -> str:
    """
    проверка баланса
    :param s: проверяемая строка скобок
    :return: статус Сбалансировано, Несбалансированно
    """
    stack1 = Stack()
    for ch in s:

        if ch in CLOSE_BRACKETS:
            open_bracket = stack1.pop()
            if open_bracket != CLOSE_BRACKETS[ch]:
                return 'Несбалансированно'
        else:
            stack1.push(ch)
    return ('Несбалансированно', 'Сбалансировано')[stack1.is_empty()]

if __name__ == '__main__':
    print(check_balance(input()))
