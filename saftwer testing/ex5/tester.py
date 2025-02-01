import csv
import subprocess
from pprint import pprint

with open('data.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    tests = [{'car': row["car"], 'abs': row["ABS"], 'esp': row["ESP"], 'fcw': row["FCW"], 'ldw': row["LDW"],
              'expected': row["Expected"]} for row in csv_reader]

for i, test in enumerate(tests):
    command = ['car_pricing.exe']

    command.append('--car')
    command.append(test['car'])

    if test['abs'].lower() == 'true':
        command.append("--abs")
    if test['esp'].lower() == 'true':
        command.append("--esp")
    if test['fcw'].lower() == 'true':
        command.append("--fcw")
    if test['ldw'].lower() == 'true':
        command.append("--ldw")

    test_result = subprocess.check_output(command, shell=True)
    test_result = test_result.strip().decode('utf_8')

    if float(test['expected']) == float(test_result):
        print(f"Test {i} Result: PASS (got {test_result}, expected {test['expected']})")
    else:
        print(f"Test {i} Result: FAIL (got {test_result}, expected {test['expected']})")
