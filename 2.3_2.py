class BigInteger:
    def __init__(self, value=0):
        # Initialization of the object, possibly passing the value as a hexadecimal string.
        self.data = self.parse_hex(value)

    def parse_hex(self, hex_str):
        # Parsing a hexadecimal string into a list of unsigned integers.
        # You may need to add code to convert the string into numbers.
        result = []
        for i in range(0, len(hex_str), 8):
            hex_block = hex_str[i:i + 8]
            result.append(int(hex_block, 16))
        return result

    def to_hex_string(self):
        # Returning the number as a hexadecimal string.
        hex_str = ''
        for num in self.data:
            hex_str += f'{num:08x}'
        return hex_str

    def add(self, other):
        # Method for adding large numbers.
        result = []
        carry = 0

        for a, b in zip(self.data, other.data):
            total = a + b + carry
            result.append(total & 0xFFFFFFFF)  # Limit to 32 bits
            carry = total >> 32  # Calculate carry for the next block

        if carry > 0:
            result.append(carry)

        return BigInteger(result)

    def subtract(self, other):
        # Method for subtracting large numbers.
        result = []
        borrow = 0

        for a, b in zip(self.data, other.data):
            diff = a - b - borrow

            if diff < 0:
                diff += 0x100000000  # Adjust for borrow from the previous block
                borrow = 1
            else:
                borrow = 0

            result.append(diff)

        # Remove leading zero blocks
        while len(result) > 1 and result[-1] == 0:
            result.pop()

        return BigInteger(result)

    def multiply(self, other):
        # Метод для множення великих чисел.
        result = [0] * (len(self.data) + len(other.data))

        for i in range(len(self.data)):
            carry = 0
            for j in range(len(other.data)):
                product = self.data[i] * other.data[j] + result[i + j] + carry
                result[i + j] = product % 0x100000000
                carry = product // 0x100000000

            if carry > 0:
                result[i + len(other.data)] += carry

        return BigInteger(result)

    def divide(self, other):
        # Метод для ділення великих чисел.
        if other.is_zero():
            raise ValueError("Division by zero is not allowed")

        quotient = [0] * len(self.data)
        remainder = [0] * len(self.data)

        for i in range(len(self.data) - 1, -1, -1):
            shift_remainder_left(remainder)
            remainder[0] = self.data[i]

            while compare(remainder, other.data) >= 0:
                subtract(remainder, other.data)
                quotient[i] += 1

        return BigInteger(quotient)

    def powmod(self, exponent, modulus):
        # Метод для піднесення великого числа до ступеня за модулем.
        result = BigInteger([1])

        base = self % modulus  # Залишок від ділення бази на модуль

        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus

            base = (base * base) % modulus
            exponent //= 2

        return result

    def is_zero(self):
        # Перевірка, чи число дорівнює нулю.
        return len(self.data) == 1 and self.data[0] == 0

    def __mod__(self, modulus):
        # Перегрузка оператора % для обчислення залишку від ділення на модуль.
        if modulus.is_zero():
            raise ValueError("Modulus cannot be zero")

        remainder = [0] * len(self.data)

        for i in range(len(self.data) - 1, -1, -1):
            shift_remainder_left(remainder)
            remainder[0] = self.data[i]

            while compare(remainder, modulus.data) >= 0:
                subtract(remainder, modulus.data)

        return BigInteger(remainder)


def shift_remainder_left(remainder):
    for i in range(len(remainder) - 1, 0, -1):
        remainder[i] = remainder[i - 1]
    remainder[0] = 0


def compare(a, b):
    for i in range(len(a) - 1, -1, -1):
        if a[i] < b[i]:
            return -1
        elif a[i] > b[i]:
            return 1
    return 0


def subtract(a, b):
    borrow = 0
    for i in range(len(a)):
        difference = a[i] - b[i] - borrow
        if difference < 0:
            difference += 0x100000000
            borrow = 1
        else:
            borrow = 0
        a[i] = difference

    def karatsuba_multiply(self, other):
        if len(self.data) == 1 or len(other.data) == 1:
            # Базовий випадок: множення однорозрядних чисел.
            return self.multiply(other)

        n = max(len(self.data), len(other.data))
        half_n = n // 2

        a = self.data[:half_n]
        b = self.data[half_n:]
        c = other.data[:half_n]
        d = other.data[half_n:]

        ac = BigInteger(a).karatsuba_multiply(BigInteger(c))
        bd = BigInteger(b).karatsuba_multiply(BigInteger(d))
        abcd = (BigInteger(a) + b).karatsuba_multiply(BigInteger(c + d))

        ad_bc = abcd - ac - bd
        result = (ac << (2 * half_n)) + (ad_bc << half_n) + bd

        return result

    def dirichlet_divide(self, divisor):
        if divisor.is_zero():
            raise ValueError("Division by zero is not allowed")

        dividend = self.data
        divisor = divisor.data

        if len(divisor) == 1 and divisor[0] == 1:
            return self

        if compare(dividend, divisor) < 0:
            return BigInteger([0])

        quotient = [0] * len(dividend)
        remainder = [0] * len(dividend)

        for i in range(len(dividend) - 1, -1, -1):
            shift_remainder_left(remainder)
            remainder[0] = dividend[i]

            while compare(remainder, divisor) >= 0:
                subtract(remainder, divisor)
                quotient[i] += 1

        return BigInteger(quotient)
