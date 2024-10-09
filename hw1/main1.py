class NFA:
    def __init__(self, start_state, end_state, transitions):
        self.start_state = start_state
        self.end_state = end_state
        self.transitions = transitions  # list of (from_state, to_state, symbol) tuples

# Helper function to generate unique state numbers
def new_state():
    new_state.counter += 1
    return new_state.counter
new_state.counter = -1

# Convert regular expression to postfix using the Shunting Yard algorithm
def regex_to_postfix(regex):
    precedence = {'+': 1, '.': 2, '*': 3}
    output = []
    operators = []

    for char in regex:
        if char == '0' or char == '1':  # operands
            output.append(char)
        elif char == '(':
            operators.append(char)
        elif char == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # remove '('
        elif char in precedence:
            while operators and operators[-1] != '(' and precedence[operators[-1]] >= precedence[char]:
                output.append(operators.pop())
            operators.append(char)
        elif char == '*':
            output.append(char)

    while operators:
        output.append(operators.pop())

    return ''.join(output)

# Build NFA from postfix regular expression
def build_nfa_from_postfix(postfix):
    stack = []

    for char in postfix:
        if char == '0' or char == '1':  # operand
            start = new_state()
            end = new_state()
            transitions = [(start, end, char)]
            stack.append(NFA(start, end, transitions))

        elif char == '.':  # concatenation
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            transitions = nfa1.transitions + nfa2.transitions
            transitions.append((nfa1.end_state, nfa2.start_state, 'e'))  # epsilon transition
            stack.append(NFA(nfa1.start_state, nfa2.end_state, transitions))

        elif char == '+':  # alternation
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = new_state()
            end = new_state()
            transitions = nfa1.transitions + nfa2.transitions
            transitions.append((start, nfa1.start_state, 'e'))  # epsilon transition to nfa1
            transitions.append((start, nfa2.start_state, 'e'))  # epsilon transition to nfa2
            transitions.append((nfa1.end_state, end, 'e'))      # epsilon transition from nfa1 to end
            transitions.append((nfa2.end_state, end, 'e'))      # epsilon transition from nfa2 to end
            stack.append(NFA(start, end, transitions))

        elif char == '*':  # Kleene star
            nfa = stack.pop()
            start = new_state()
            end = new_state()
            transitions = nfa.transitions
            transitions.append((start, nfa.start_state, 'e'))  # epsilon transition to NFA
            transitions.append((nfa.end_state, start, 'e'))    # epsilon transition back to start
            transitions.append((start, end, 'e'))              # epsilon transition to new end
            transitions.append((nfa.end_state, end, 'e'))      # epsilon transition from NFA to end
            stack.append(NFA(start, end, transitions))

    return stack.pop()

# Output the NFA
def print_nfa(nfa):
    states = set()
    for transition in nfa.transitions:
        states.add(transition[0])
        states.add(transition[1])

    n = len(states)
    m = len(nfa.transitions)
    print(f"{n} {m} {nfa.start_state} {nfa.end_state}")
    for t in nfa.transitions:
        print(f"{t[0]} {t[1]} {t[2]}")

# Main function to parse input and run the program
def main():
    # Read input
    l = int(input())
    regex = input().strip()

    # Convert regex to postfix form
    postfix = regex_to_postfix(regex)

    # Build NFA from postfix regex
    nfa = build_nfa_from_postfix(postfix)

    # Output the NFA
    print_nfa(nfa)

if __name__ == "__main__":
    main()
