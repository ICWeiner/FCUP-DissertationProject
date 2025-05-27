#!/usr/bin/env python3
import sys

if len(sys.argv) != 4:
    print("Usage: script.py num1 num2 num3")
    sys.exit(1)

try:
    numbers = [float(arg) for arg in sys.argv[1:4]]
    avg = sum(numbers) / 3
    print(f"{avg:.6f}")
except ValueError:
    print("Error: all arguments must be numbers.")
    sys.exit(1)
