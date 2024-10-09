from collections import defaultdict, deque

# Helper function to compute the epsilon closure of a set of states
def epsilon_closure(nfa, states):
    closure = set(states)
    queue = deque(states)
    
    while queue:
        state = queue.popleft()
        for (src, dest, symbol) in nfa["transitions"]:
            if src == state and symbol == 'e' and dest not in closure:
                closure.add(dest)
                queue.append(dest)
    
    return closure

# Function to simulate the NFA on an input string
def simulate_nfa(nfa, input_string):
    # Start with the epsilon closure of the initial state
    current_states = epsilon_closure(nfa, [nfa["start_state"]])
    
    # Process each character in the input string
    for char in input_string:
        next_states = set()
        for state in current_states:
            for (src, dest, symbol) in nfa["transitions"]:
                if src == state and symbol == char:
                    next_states.add(dest)
        
        # Move to the epsilon closure of the new set of states
        current_states = epsilon_closure(nfa, next_states)
    
    # Check if any of the current states is a final state
    return nfa["final_state"] in current_states

# Main function to parse input and run the NFA simulation
def main():
    # Read the input string
    l = int(input())
    input_string = input().strip()

    # Read the NFA description
    nfa = {}
    nfa["num_states"], nfa["num_transitions"], nfa["start_state"], nfa["final_state"] = map(int, input().split())
    
    nfa["transitions"] = []
    for _ in range(nfa["num_transitions"]):
        src, dest, symbol = input().split()
        src = int(src)
        dest = int(dest)
        nfa["transitions"].append((src, dest, symbol))

    # Simulate the NFA with the input string
    if simulate_nfa(nfa, input_string):
        print("yes")
    else:
        print("no")

if __name__ == "__main__":
    main()