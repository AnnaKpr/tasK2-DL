import array


class MyBigInt:
    def __init__(self):
        # 'I' specifies an unsigned integer (32-bit) array
        self.data = array.array('I')

    def setHex(self, hex_string):
        # Convert the hexadecimal string to an array of unsigned integers
        self.data = array.array(
            'I', [int(hex_string[i:i + 8], 16) for i in range(2, len(hex_string), 8)])

    def getHex(self):
        # Convert the array of unsigned integers back to a hexadecimal string
        hex_string = '0x'
        for block in self.data:
            hex_string += format(block, '08x')
        return hex_string

    def setDecimal(self, decimal_string):
        # Convert the decimal string to an array of unsigned integers
        self.data = array.array('I', [int(decimal_string)])

    def getDecimal(self):
        # Convert the array of unsigned integers to a decimal string
        return str(self.data[0])

    def XOR(self, other):
        # Bitwise exclusive OR with another MyBigInt object
        xor_data = array.array(
            'I', [a ^ b for a, b in zip(self.data, other.data)])
        self.data = xor_data

    def OR(self, other):
        # Bitwise OR with another MyBigInt object
        or_data = array.array(
            'I', [a | b for a, b in zip(self.data, other.data)])
        self.data = or_data

    def AND(self, other):
        # Bitwise AND with another MyBigInt object
        and_data = array.array(
            'I', [a & b for a, b in zip(self.data, other.data)])
        self.data = and_data

    def shiftR(self, n):
        # Right shift by n bits
        for i in range(n):
            self.data.pop(0)
            self.data.append(0)

    def shiftL(self, n):
        # Left shift by n bits
        for i in range(n):
            self.data.pop()
            self.data.insert(0, 0)

    def INV(self):
        # Bitwise inversion for a signed integer
        self.data = ~self.data & 0xFFFFFFFF  # Mask to 32 bits


numberA = MyBigInt()
numberA.data = 0x12345678  # Set the value

# Perform the bitwise inversion
numberA.data = ~numberA.data & 0xFFFFFFFF  # Mask to 32 bits

# Print the result in hexadecimal
print("INV result:", hex(numberA.data)[2:])


numberA = MyBigInt()
numberB = MyBigInt()
numberA.setHex(
    "0x51bf608414ad5726a3c1bec098f77b1b54ffb2787f8d528a74c1d7fde6470ea4")
numberB.setHex(
    "0x403db8ad88a3932a0b7e8189aed9eeffb8121dfac05c3512fdb396dd73f6331c")
numberA.XOR(numberB)
print("XOR result:", numberA.getHex())


# Create two MyBigInt objects
numberA = MyBigInt()
numberB = MyBigInt()

# Set values for numberA and numberB using hexadecimal representation
numberA.setHex("e035c6cfa42609b998b883bc1699df885cef74e2b2cc372eb8fa7e7")
numberB.setHex("5072f028943e0fd5fab3273782de14b1011741bd0c5cd6ba6474330")

# Perform the bitwise OR operation
numberA.OR(numberB)
# Should print the OR result in hexadecimal
print("OR result:", numberA.getHex())

# Reset numberA
numberA.setHex("e035c6cfa42609b998b883bc1699df885cef74e2b2cc372eb8fa7e7")

# Perform the bitwise AND operation
numberA.AND(numberB)
# Should print the AND result in hexadecimal
print("AND result:", numberA.getHex())

# Reset numberA
numberA.setHex("e035c6cfa42609b998b883bc1699df885cef74e2b2cc372eb8fa7e7")

# Perform the right shift operation
numberA.shiftR(2)
# Should print the right shift result in hexadecimal
print("shiftR result:", numberA.getHex())

# Reset numberA
numberA.setHex("e035c6cfa42609b998b883bc1699df885cef74e2b2cc372eb8fa7e7")

# Perform the left shift operation
numberA.shiftL(2)
# Should print the left shift result in hexadecimal
print("shiftL result:", numberA.getHex())
