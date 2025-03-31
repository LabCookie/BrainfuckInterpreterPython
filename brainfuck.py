# Name:Brainfuck Interpreter Python
# Original Date: 2022/09/17
# Fork Date: 2025/03/30
# Repository: https://github.com/BaseMax/BrainfuckInterpreterPython
# Author: Max Base
# Fork Author: Labcookie

# CHANGELOG
# - "+" sets the cell to 0 if it's at 255
# - "-" sets the cell to 255 if it's at 0
# - ">" sets the cell pointer to 0 if it's at 30,000
# - "<" sets the cell pointer to 30,000 if it's at 0
# - Implemented multi-line support
# - New two arguments: stdin and size, if size empty, it'll be 30,000 by default
# - "," logic has been changed


import sys
#from time import sleep

def brainfuck(input,stdin="",size=30*1000,ignoreloopifzero=False):
    # >	Move the pointer to the right
    # <	Move the pointer to the left
    # +	Increment the memory cell at the pointer
    # -	Decrement the memory cell at the pointer
    # .	Output the character signified by the cell at the pointer
    # ,	Input a character and store it in the cell at the pointer
    # [	Jump past the matching ] if the cell at the pointer is 0
    # ]	Jump back to the matching [ if the cell at the pointer is nonzero

    # initialize memory
    memory = [0] * size
    loopstack = []
    # initialize pointer
    pointer = 0
    # initialize output
    output = ""

    # All characters other than ><+-.,[] should be considered comments and ignored. But, see extensions below.

    # loop through input
    i = 0
    while i < len(input):
        # print("i: {}, input[i]: {}, memory: {}, pointer: {}".format(i, input[i], memory, pointer))
        # >	Move the pointer to the right
        if input[i] == ">":
            pointer = ((pointer+1) % len(memory)) # Allows user to go to cell 0 if user is already at the end
        # <	Move the pointer to the left
        elif input[i] == "<":
            pointer = ((pointer+len(memory)-1) % len(memory)) # Allows user to go to the last cell if user is already at the beginning
        # +	Increment the memory cell at the pointer
        elif input[i] == "+":
            memory[pointer] = (memory[pointer]+1) % 256
        # -	Decrement the memory cell at the pointer
        elif input[i] == "-":
            memory[pointer] = (memory[pointer]+255) % 256
        # .	Output the character signified by the cell at the pointer
        elif input[i] == ".":
            output += chr(memory[pointer])
        # ,	Input a character and store it in the cell at the pointer
        elif input[i] == ",":
            if pointer < len(stdin):
                memory[pointer] += ord(stdin[pointer]) # Fixed logic
        elif input[i] == "[":
            if (memory[pointer]>0 or not ignoreloopifzero): 
                loopstack.append(i)
            else:
                while input[i] != "]":
                    i += 1
        elif input[i] == "]":
            if memory[pointer] > 0:
                i = loopstack[-1]-1
            else:
                loopstack.pop()
        else:
            pass
        i += 1
        #sleep(0.01)

    #print(memory)
    return output

# init
### dcode
# input1 = "++++++++ [>++++++++++++>+++++++++++++<<-] >++++. -. >+++++++. <+. +."
### fibunacci
# input2 = "+++++++++++>+>>>>++++++++++++++++++++++++++++++++++++++++++++>++++++++++++++++++++++++++++++++<<<<<<[>[>>>>>>+>+<<<<<<<-]>>>>>>>[<<<<<<<+>>>>>>>-]<[>++++++++++[-<-[>>+>+<<<-]>>>[<<<+>>>-]+<[>[-]<[-]]>[<<[>>>+<<<-]>>[-]]<<]>>>[>>+>+<<<-]>>>[<<<+>>>-]+<[>[-]<[-]]>[<<+>>[-]]<<<<<<<]>>>>>[++++++++++++++++++++++++++++++++++++++++++++++++.[-]]++++++++++<[->-<]>++++++++++++++++++++++++++++++++++++++++++++++++.[-]<<<<<<<<<<<<[>>>+>+<<<<-]>>>>[<<<<+>>>>-]<-[>>.>.<<<[-]]<<[>>+>+<<<-]>>>[<<<+>>>-]<<[<+>-]>[<+>-]<<<-]"
### test
# input3 = "+++[>+++++<-]"
### hello world (with deep comments)
# input4 = """
# +++++ +++++             initialize counter (cell #0) to 10
# [                       use loop to set the next four cells to 70/100/30/10
#     > +++++ ++              add  7 to cell #1
#     > +++++ +++++           add 10 to cell #2 
#     > +++                   add  3 to cell #3
#     > +                     add  1 to cell #4
#     <<<< -                  decrement counter (cell #0)
# ]                   
# > ++ .                  print 'H'
# > + .                   print 'e'
# +++++ ++ .              print 'l'
# .                       print 'l'
# +++ .                   print 'o'
# > ++ .                  print ' '
# << +++++ +++++ +++++ .  print 'W'
# > .                     print 'o'
# +++ .                   print 'r'
# ----- - .               print 'l'
# ----- --- .             print 'd'
# > + .                   print '!'
# > .                     print '\n'
# """
### hello world
# input5 = """
# >++++++++[<+++++++++>-]<.
# >++++[<+++++++>-]<+.
# +++++++..
# +++.
# >>++++++[<+++++++>-]<++.
# ------------.
# >++++++[<+++++++++>-]<+.
# <.
# +++.
# ------.
# --------.
# >>>++++[<++++++++>-]<+.
# """

if __name__ == "__main__":
    if len(sys.argv) > 1:
        #brainfuck("++++++[>+<-]",size=32)
        with open(sys.argv[1], 'r') as file:
            print(brainfuck("".join(file.readlines()),sys.argv[2] if len(sys.argv) > 2 else "",int(sys.argv[3]) if len(sys.argv) > 3 else 30*1000,bool(sys.argv[4]) if len(sys.argv) > 4 else False)) # Implemented multi-line support and stdin support
    else:
        print("Usage: py brainfuck.py *[file] [stdin] [size]")
        print("*: required")
