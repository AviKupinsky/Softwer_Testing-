#############################################################
# FILE : ex.1
# WRITER : Avi Kupinsky avikupinsky 318336070
# EXERCISE : softwareTesting  ex1 2023
#############################################################
import sys

TYPE = "Type"
LEGNTH = "Length"
VALUE = "value"
PIPE = "|"
UNDER_LINE = "_"
STRING = "String"
INTEGER = "Integer"
BIT = "bit"
STRING_TYPE = '1'
INTEGER_TYPE = '2'
ERROR_STRING_LEGNTH = "the string legnth dos not mach the number it was given"
ERROR_POWER_TWO = "the number that was given is not the power of 2"
ERROR_STRING_WITH_INTEGER = "the first column is string but in the third column is integer"
ERROR_INTEGER_WITH_STRING = "the first column is integer but in the third column is string"
ERROR_NOT_ENOUGH_BYTES = "the bytes that were given where not enough"
ERROR_NOT_CURRENT_PARAMETERS = "there wasn't the current amount of parameters per line"
ERROR_FIRST_COLUM = "there wasn't the 1 or 2 in the colum"

FIRST_COLUM = 0
SECOND_COLUM = 1
THIRD_COLUM = 2
NUMBER_IN_ROW = 3
BIT_LEGNTH = 8


def finding_legnth_columns(csv_file):
    """
    finding the legnth of the second and third columns
    :param csv_file: the csv file we are reading from
    :return: the max legnth of the columns
    """
    second_column_legnth = len(LEGNTH)
    third_column_legnth = len(VALUE)
    for line in csv_file:
        elements = line.split(',')
        if len(elements) != NUMBER_IN_ROW:
            sys.exit(ERROR_NOT_CURRENT_PARAMETERS)
        # if the first colum is a string
        if elements[FIRST_COLUM] == STRING_TYPE:
            second_column_legnth = first_colum_string(elements, second_column_legnth)
        elif elements[FIRST_COLUM] == INTEGER_TYPE:
            # if it's an integer
            second_column_legnth = first_colum_integer(elements, second_column_legnth)
        else:
            sys.exit(ERROR_FIRST_COLUM)
        third_column_legnth = max(third_column_legnth, len(elements[THIRD_COLUM].strip()))
    return second_column_legnth, third_column_legnth


def first_colum_string(elements, second_column_legnth):
    """
    checking that all the parameters are current if its a string
    :param elements: the elements of the scv file
    :param second_column_legnth: the current legnth of the second colum
    :return: the max legnth
    """
    # if the first colum said it's a sting but the third colum is a int
    if elements[THIRD_COLUM].strip().isnumeric():
        sys.exit(ERROR_STRING_WITH_INTEGER)
    # if the number of bites dos not mach
    elif len(elements[THIRD_COLUM].strip()) != int(elements[SECOND_COLUM]):
        sys.exit(ERROR_STRING_LEGNTH)
    return max(second_column_legnth, len(elements[SECOND_COLUM]))


def first_colum_integer(elements, second_column_legnth):
    """
    checking that all the parameters are current if it's a integer
    :param elements: the elements of the scv file
    :param second_column_legnth: the current legnth of the second colum
    :return: the max legnth
    """
    # if the first colum said it's a integer but the third colum is a string
    if not elements[THIRD_COLUM].strip().isnumeric():
        sys.exit(ERROR_INTEGER_WITH_STRING)
    bit_number = BIT_LEGNTH * int(elements[SECOND_COLUM])
    # checking that it is the power of 2
    check_power_two = bit_number and (not (bit_number & (bit_number - 1)))
    if not check_power_two:
        sys.exit(ERROR_POWER_TWO)
    elif bit_number < int(elements[THIRD_COLUM].strip()).bit_length():
        sys.exit(ERROR_NOT_ENOUGH_BYTES)
    return max(second_column_legnth, len(str(bit_number) + BIT))


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        x, y = finding_legnth_columns(f)
        f.close()
    print(PIPE + TYPE.ljust(len(INTEGER)) + PIPE + LEGNTH.ljust(x) + PIPE + VALUE.ljust(y) + PIPE)
    print(PIPE + UNDER_LINE*len(INTEGER) + PIPE + UNDER_LINE*x + PIPE + UNDER_LINE*y + PIPE)
    with open(sys.argv[1], 'r') as f:
        for line in f:
            elements = line.split(',')
            if elements[FIRST_COLUM] == STRING_TYPE:
                print(PIPE + STRING.ljust(len(INTEGER)) + PIPE + elements[SECOND_COLUM].ljust(x)
                      + PIPE + elements[THIRD_COLUM].strip().ljust(y) + PIPE)
            else:
                print(PIPE + INTEGER.ljust(len(STRING)) + PIPE
                      + (str(int(elements[SECOND_COLUM])*BIT_LEGNTH) + BIT).ljust(x)
                      + PIPE + elements[THIRD_COLUM].strip().ljust(y) + PIPE)
        f.close()