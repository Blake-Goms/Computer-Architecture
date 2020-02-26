"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.fl = 0
        self.sp = 3

    def load(self):
        """Load a program into memory."""
        #Get File name
        print(sys.argv)
        # grab the second file path
        filename = sys.argv[1]
        address = 0

        with open(filename) as f:
            for line in f:
                l = line.split("#")
                l[0] = l[0].strip()

                if l[0] == '':
                    continue
                # convert string l[0] to int
                # convert int binary to binary code
                # value = int(bin(binary), 2)
                # binary = int(l[0])
                # print(int(bin(binary), 2))
                value = int(l[0], 2)
                self.ram[address] = value
                print("In ram, printed:", bin(self.ram[address]))
                address += 1

    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MDR_value, MDR_address):
        self.ram[MDR_address] = MDR_value
        return self.ram[MDR_address]

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        # Set flag register
        self.reg[self.fl] = 0
        # Set Stack Pointer
        self.reg[self.sp] = 244
        # Instructions Decoded from LS8-spec
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101
        
        while running or self.pc < len(self.ram):
            # IR comes from readme. needs to read mem address stored in PC and store result in IR
            IR = self.ram_read(self.pc)
            #  op_a needs to read next byte after PC
            operand_a = self.ram_read(self.pc + 1)
            #  op_b needs to read next 2 bytes after PC
            operand_b = self.ram_read(self.pc + 2)
            # print('Running ---', IR)                
            if IR == HLT:
                print("HALT")
                running = False
                sys.exit(0)

            elif IR == LDI:
                print("LDI =>", bin(IR))
                # LDI: register immediate. Set the value of a register to an integer
                # Now put value in correct register
                self.reg[operand_a] = operand_b
                # used both, so advance by 3 to start at next correct value
                # op_a will be 1 ahead from current pos, op_b 2
                self.pc += 3

            elif IR == PRN:
                print("PRN =>", bin(IR))
                # PRN: register pseudo-instruction
                # print numeric value stored in given register
                print(self.reg[operand_a])
                # print("reg", self.reg)
                # print("PC", self.pc)
                self.pc += 2

            elif IR == MUL:
                print("MUL =>", bin(IR))
                # instruction handled by the ALU.
                # Multiply the values in two registers together and store the result in registerA.
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
                
                
            elif IR == POP:
                print("POP =>", bin(IR))
                # Get the value at top of the stack thats in the SP register
                value = self.ram[self.reg[self.sp]]
                # Put that value in current selected register
                self.reg[operand_a] = value
                # don't forget to increment register/sp
                self.reg[self.sp] += 1
                self.pc += 2
            elif IR == PUSH:
                print("PUSH =>", bin(IR))
                # FIRST DECREMENT stack pointer
                self.reg[self.sp] -= 1
                # look in and get the register op_a
                value = self.reg[operand_a]
                # add to ram at current spot of the stack
                self.ram[self.reg[self.sp]] = value
                self.pc += 2               
                
            # else: 
            #     print("------------------")
            #     print("PC", self.pc)
            #     print("reg", self.reg)
            #     print("op_a", operand_a)
            #     print("op_b", operand_b)
            #     print("------------------")