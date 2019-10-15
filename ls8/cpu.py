"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [8] * 8
        self.pc = 0
        self.sp = 0xF4

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        try:
            with open(sys.argv[1]) as f:
                address = 0
                for line in f:
                    line_split = line.split("#")

                    num = line_split[0].strip()

                    try:
                        self.ram[address] = int(num, 2)
                        address += 1
                    except ValueError:
                        pass
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} Not Found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

        while running:

            IR = self.ram[self.pc]
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            
            
            # LDI: load "immediate", store a value in a register, or "set this register to this value".
            if IR == LDI:
                self.reg[op_a] = op_b
                self.pc += 3
            
            # PRN: a pseudo-instruction that prints the numeric value stored in a register.
            elif IR == PRN:
                print(self.reg[op_a])
                self.pc += 2

            elif IR == MUL:
                self.alu("MUL", op_a, op_b)
                self.pc += 3
            
            
            elif IR == HLT:
                running = False