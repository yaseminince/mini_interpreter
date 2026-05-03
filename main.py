from interpreter import Interpreter


RED = "\033[91m"    # red color for error messages
GREEN = "\033[92m"  # green color for successful output
CYAN = "\033[96m"
RESET = "\033[0m"   # resets the color back to normal


# prints the welcome banner when the program starts
def print_header():
    print("=======================================================================")
    print(f"{CYAN}                       ☁️   WELCOME TO CLOUD   ☁️         {RESET}")
    print("=======================================================================")
    print("Write your code line by line.")
    print("Type 'help' to see commands.")
    print("=======================================================================")
    print()


# prints the list of available commands
def print_help():
    print("Commands:")
    print("  run    -> run the current program")
    print("  clear  -> clear the whole program")
    print("  undo   -> remove the last entered line")
    print("  show   -> show the current program")
    print("  exit   -> close the interpreter")
    print("  help   -> show the commands menu")
    print()


# displays all entered lines with their line numbers
def print_program(lines):
    if not lines:
        print("\nNo code has been entered yet.\n")
        return

    print("\nCurrent program:")
    print("-----------------------------------------------------------------------")

    for i in range(len(lines)):
        print(f"{i+1:>2} | {lines[i]}")

    print("-----------------------------------------------------------------------")
    print()


# removes the last line the user entered
def undo_last_line(lines):
    if not lines:
        print("\nThere is no line to remove.\n")
        return

    removed_line = lines.pop() # removes and returns the last line
    print(f"\nRemoved last line: {removed_line}\n")


# deletes all entered lines
def clear_program(lines):
    lines.clear()
    print("\nProgram cleared. You can start writing again.\n")


# formats the result value for display based on its type
def format_result(result):
    if isinstance(result, bool):
        return "true" if result else "false"
    if isinstance(result, float) and result == int(result):
        return str(int(result))  # show 3.0 as 3
    return str(result)


# runs the program the user has typed so far
def run_program(lines):
    if not lines:
        print("\nEmpty program cannot be executed.\n")
        return

    print_program(lines)

    source_code = "\n".join(lines) # joins all lines into a single string

    print("Running program...\n")

    interpreter = Interpreter()
    result, error = interpreter.run("<stdin>", source_code)

    if error:
        print(f"{RED}[ERROR]{RESET}")
        print(error)
        lines.clear()
        print("\nProgram cleared because an error occurred. You can start a new program.")

    else:
        print(f"{GREEN}[OUTPUT]{RESET}")

        if result is not None:
            print(format_result(result))
        else:
            print("Program executed successfully.")

        lines.clear()
        print("\nProgram finished. You can start a new program.")

    print("\n" + "=======================================================================" + "\n")


# keeps the interpreter running until the user types exit
def main():
    lines = [] # holds each line of code the user types

    print_header()
    print_help()

    while True:
        
        line = input("☁️ >>> ").rstrip()
        
        command = line.strip().upper() # uppercase 

        if command == "":
            continue # ignore empty input

        if command == "EXIT":
            print("\nCiao :)")
            break

        elif command == "HELP":
            print_help()

        elif command == "SHOW":
            print_program(lines)

        elif command == "UNDO":
            undo_last_line(lines)

        elif command == "CLEAR":
            clear_program(lines)

        elif command == "RUN":
            run_program(lines)

        else:
            lines.append(line) # if not a command, save as a line of code


# ensures main() only runs when this file is executed directly
if __name__ == "__main__":
    main()

