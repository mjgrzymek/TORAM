
def execute(code, input_gen):
    ram = {}
    labels = {}
    code = code.splitlines()
    code = [line[:line.find('#')] if '#' in line else line for line in code]
    code = [line.split() for line in code if line.split()]
    for i, line in enumerate(code):
        if ':' in line[0]:
            labels[ line[0][:line[0].find(':')] ] = i
    i = 0
    while i < len(code):
        line = code[i]
        if ':' not in line[0]:
            instruction = line[0]
            if instruction == 'halt': break
            elif instruction[0] == 'j':
                label = line[1]
                doJump = False
                if instruction == 'jump':
                    doJump = True
                elif instruction == 'jgtz':
                    doJump = ram[0] > 0
                elif instruction == 'jzero':
                    doJump = ram[0] == 0
                
                if doJump:
                    i= labels[label]
            else:
                operandum = line[1]

                if instruction in ('store', 'read'):
                    if operandum[0] == '^':
                        target = ram[int(operandum[1:])]
                    else:
                        target = int(operandum)

                    if instruction == 'store':
                        ram[target]=ram[0]
                    elif instruction == 'read':
                        ram[target]=next(input_gen)
                    else:
                        print('instruction', instruction, "isn't valid")
                else:
                    if operandum[0] == '=':
                        operandum_value = int(operandum[1:])
                    elif operandum[0] == '^':
                        operandum_value = ram[ram[int(operandum[1:])]]
                    else:
                        operandum_value = ram[int(operandum)]

                    if instruction == 'write':
                        print('>>',operandum_value)
                    elif instruction == 'load':
                        ram[0] = operandum_value
                    elif instruction == 'add':
                        ram[0] += operandum_value
                    elif instruction == 'sub':
                        ram[0] -= operandum_value
                    elif instruction == 'mult':
                        ram[0] *= operandum_value
                    elif instruction == 'div':
                        ram[0] //= operandum_value
                    else:
                        print('instruction', instruction, "isn't valid")
        i+=1
    print('Execution succesfully finished')
