"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.pc = 0
        self.reg = [0] * 8
        self.fl = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
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
        #elif op == "SUB": etc
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
        # Instructions Decoded from LS8-spec
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        
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

            if IR == LDI:
                # LDI: register immediate. Set the value of a register to an integer
                # Now put value in correct register
                print("LDI runs first")
                self.reg[operand_a] = operand_b
                # used both, so advance by 3 to start at next correct value
                # op_a will be 1 ahead from current pos, op_b 2
                self.pc += 3

            if IR == PRN:
                # PRN: register pseudo-instruction
                # print numeric value stored in given register
                print(self.reg[operand_a])
                self.pc += 2
