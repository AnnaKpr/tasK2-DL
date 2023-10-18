
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


number = MyBigInt()

# Test 1: Hexadecimal to Decimal Conversion
number.setHex("0x12345678")
assert number.getDecimal() == "305419896"  # Verify the conversion to decimal

# Test 2: Decimal to Hexadecimal Conversion
number.setDecimal("1234567890")
assert number.getHex() == "0x499602d2"  # Verify the conversion to hexadecimal


# Test 3: Changing a value and retesting
number.setHex("0xabcdef01")
assert number.getDecimal() == "2882400001"  # Verify the updated decimal value
assert number.getHex() == "0xabcdef01"  # Verify the updated hexadecimal value

print("All test cases passed!")
