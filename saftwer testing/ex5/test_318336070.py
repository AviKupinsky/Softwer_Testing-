""" Example functions for Unit Test Class"""

import os
import sys
import json
import random
import datetime


import fastapi.exceptions
import pytest
from fastapi.testclient import TestClient
from fastapi import status as http_status


# Makes it easier to run in students' Windows's laptops, with no need to set path vars
sys.path.append(os.path.dirname(os.path.abspath(__name__)))
import main
import extra

# Client that gives us access to a dummy server for HTTP tests
client = None


# ---------------------------------------------------------------------------
# Setup and Teardown functions.
# These are examples of the functions used by pytest to prepare and dismantle
#   the entire test suite, or to prepare and dismantle each one of the tests.
#   You can, for example, setup services, states, or other operating environments.
# Advanced usage: You can also have setup/teardown functions for specific tests,
#   or for specific groups of tests.
#
# To see the output of the setup/teardown functions, run pytest with the argument:
#   --capture=no (as in pytest -v --capture=no)
# ---------------------------------------------------------------------------
def setup_module(module):
    print("\n==> THIS WILL HAPPEN *before all* THE TESTS BEGIN")
    # For example, copy test data into the test suite
    # For example, set a dummy server running (like the TestClient)
    print("==> START!")

    global client
    client = TestClient(main.app)


def teardown_module(module):
    print("\n==> THIS WILL HAPPEN *after all* THE TESTS END")
    # For example, delete test files and output files
    print("==> FINISH!")

    global client
    client = None


def setup_function():
    print("\n--> This will happen BEFORE each one of the tests begin")
    # For example, cleanup temp files
    # For example, get information on resources available


def teardown_function():
    print("\n--> This will happen AFTER each one of the tests ends")
    # For example, release handles


# ---------------------------------------------------------------------------
# TEST 1: Transform a text to lowercase. Simple!
# Amounts to 1 test in the total unit tests
# ---------------------------------------------------------------------------
def test_lower_ABCD():
    r = main.lower("ABCD")
    j = json.loads(r.body)
    assert r.status_code == 200
    assert j["res"] == "abcd"


# ---------------------------------------------------------------------------
# TEST 2: Tests can be longer and/or consist of many checks.
#   Note this is a metamorphic test, we don't care about the actual strength
#       of the password or of the results of the first test. We just want the
#       tests to be consistent.
# Amounts to 1 test in the total unit tests
# ---------------------------------------------------------------------------
def test_password_length_score():
    password = "".join(random.choices("abcXYZ123!@#", k=20))

    while len(password) >= 1:
        r_large = main.password_strength(password)
        j_large = json.loads(r_large.body)

        password = password[:-1]
        r_small = main.password_strength(password)
        j_small = json.loads(r_small.body)

        assert 200 == r_large.status_code
        assert 200 == r_small.status_code
        assert j_large["res"] >= j_small["res"]


# ---------------------------------------------------------------------------
# TEST 3: Transform to uppercase a number of strings. Still simple, notice how
#   the framework allows to perform one test on multiple variables without
#   repeating the test.
# Amounts to 7 tests in the total unit tests
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "test,expected",
    [
        ("", ""),
        ("a", "A"),
        ("q3q5q7q10", "Q3Q5Q7Q10"),
        ("2q4q6q8q11q14q17q20q", "2Q4Q6Q8Q11Q14Q17Q20Q"),
        ("q3q5q7q10q13q16q19q22q25q", "Q3Q5Q7Q10Q13Q16Q19Q22Q25Q"),
        ("3", "3"),
        ("abc#$%def", "ABC#$%DEF"),
    ],
    ids=[
        "empty",
        "single letter",
        "10 chars",
        "20 chars",
        "long string",
        "digit",
        "special chars",
    ],
)
def test_upper_many(test, expected):
    r = main.upper(test)
    j = json.loads(r.body)
    assert r.status_code == 200
    assert j["res"] == expected


# ---------------------------------------------------------------------------
# TEST 4: T-Tweak has our tweak functions (units) running on top of a web server
#   that has specific configurations to deal with the user input (so it's another unit).
#   Luckily fastapi let's us separate that unit as well with a dummy server.
# Amounts to 1 test in the total unit tests
# ---------------------------------------------------------------------------
def test_upper_rest_within_bv():
    r = client.get("upper/word")
    assert 200 == r.status_code
    assert "WORD" == r.json()["res"]


# ---------------------------------------------------------------------------
# TEST 5: Using the dummy server, for negative tests.
# Amounts to 1 test in the total unit tests
# 404: Page not found
# 422: Unprocessable Entity
# ---------------------------------------------------------------------------
def test_upper_rest_outside_bv():
    r = client.get("upper")
    assert 404 == r.status_code
    r = client.get("upper/-3-5-7-9-12-15-18-21-")
    assert 422 == r.status_code


# ---------------------------------------------------------------------------
# TEST 6: Functions with complex dependencies may require us to work around the
#   complexity by controlling some of the environment.
#   This is not always possible and not always effective.
# Amounts to 1 tests in the total unit tests
# ---------------------------------------------------------------------------
def test_random_naive():
    extra.reset_random(0)
    r = main.rand_str(4)
    j = json.loads(r.body)

    assert r.status_code == 200
    assert j["res"] == "2yW4"

    r = main.rand_str(15)
    j = json.loads(r.body)

    assert r.status_code == 200
    assert j["res"] == "Acq9GFz6Y1t9EwL"


# ---------------------------------------------------------------------------
# TEST 7: For functions with complex dependencies.
#   We can create a stub of the dependencies, replacing it with a fake function
#       of our own. Then we have full control.
# Amounts to 1 tests in the total unit tests
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "length",
    [1, 10, 20, 50],
)
def test_random_unit(monkeypatch, length):
    monkeypatch.setattr(main.extra, "get_rand_char", lambda: "t")
    r = main.rand_str(length)
    j = json.loads(r.body)
    assert r.status_code == 200
    assert j["res"] == "t" * length


# ---------------------------------------------------------------------------
# TEST 8: T-Tweak functions also throw exceptions when something is not right
#   (for example, when we need to send a different HTTP status). We have to
#   test that too! Unit Test frameworks allow the test to expect a specific
#   Exception. Useful, uh?
# 409: Conflict
# Amounts to 1 test in the total unit tests
# ---------------------------------------------------------------------------
def test_with_exception():
    # 'raises' checks that the exception is raised
    with pytest.raises(fastapi.exceptions.HTTPException) as exc:
        main.substring("course 67778", 3, 2)
    assert http_status.HTTP_409_CONFLICT == exc.value.status_code


# ---------------------------------------------------------------------------
# TEST 9: Unit test frameworks allow setting conditions to skip tests.
#   Sometimes a test may be suitable for a platform but not another, for a version
#   but not another, etc.
# Amounts to 1 test in the total unit tests
# ---------------------------------------------------------------------------
@pytest.mark.skipif(fastapi.__version__ > "0.95", reason="requires fastapi <= 0.95")
def test_root_status():
    r = client.get("/")
    assert "Operational" == r.json()["res"]


# ---------------------------------------------------------------------------
# TEST 10: test_password_ec
# Automate the tests for equivalence classes of password function. The list of equivalence
#   partitions and sample values is given in the exercise document.
# The tests will reach 100% statement coverage of the password_strength function (line 323-369).
#   Hint: You will need to use:
#   - direct calls to main.password_stregth in order to receive scores for all examples
# ---------------------------------------------------------------------------
def test_password_ec():
    RES = "res"

    empty_password = ""
    r = main.password_strength(empty_password)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 0

    length_between_zero_two_password = "1"
    r = main.password_strength(length_between_zero_two_password)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 0

    length_over_twenty = "Too-L0ng-4-the-allowed-input-length"
    r = main.password_strength(length_over_twenty)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 10

    root_password = "root"
    r = main.password_strength(root_password)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 0


    password_password = "password"
    r = main.password_strength(password_password)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 0

    password_password = "admin"
    r = main.password_strength(password_password)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 0

    length_password_two_twelve_lower_upper_number = "G00dShort"
    r = main.password_strength(length_password_two_twelve_lower_upper_number)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 7

    length_password_same_char = "gggggggg"
    r = main.password_strength(length_password_same_char)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 0

    length_password_four_twelve_without_uppercase = "gfs98ased"
    r = main.password_strength(length_password_four_twelve_without_uppercase)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 5

    length_password_four_twelve_without_lowercase = "NOT1LOWCASE"
    r = main.password_strength(length_password_four_twelve_without_lowercase)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 7

    length_password_four_twelve_without_digits = "noDIGIT"
    r = main.password_strength(length_password_four_twelve_without_digits)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 3

    length_password_six_twelve_only_lower = "lowcaseonly"
    r = main.password_strength(length_password_six_twelve_only_lower)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 5

    length_password_six_twelve_only_upper = "UPCASEONLY"
    r = main.password_strength(length_password_six_twelve_only_upper)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 4

    length_password_six_twelve_only_digit = "1234567"
    r = main.password_strength(length_password_six_twelve_only_digit)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 1

    length_password_six_twelve_special_chars_only = "%@#$^&*"
    r = main.password_strength(length_password_six_twelve_special_chars_only)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 0

    length_password_over_twelve_lower_upper_number = "L0ng-And-G00d"
    r = main.password_strength(length_password_over_twelve_lower_upper_number)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 10.

    length_password_over_twelve_same_char = "aaaaaaaaaaaaaaaaaa"
    r = main.password_strength(length_password_over_twelve_same_char)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 0

    length_password_over_twelve_no_uppercase = "l0ngbutnouppercase"
    r = main.password_strength(length_password_over_twelve_no_uppercase)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 8

    length_password_over_twelve_no_lowercase = "LONG1BUTNOLOWCASE"
    r = main.password_strength(length_password_over_twelve_no_lowercase)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 8

    length_password_over_twelve_no_digits = "LongButNotOneDigit"
    r = main.password_strength(length_password_over_twelve_no_digits)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 8

    length_password_over_twelve_only_lowercase = "longbutonlylowecase"
    r = main.password_strength(length_password_over_twelve_only_lowercase)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 6

    length_password_over_twelve_only_uppercace = "LONGBUTONLYUPCASE"
    r = main.password_strength(length_password_over_twelve_only_uppercace)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 6

    length_password_over_twelve_only_digits = "12345678901234"
    r = main.password_strength(length_password_over_twelve_only_digits)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 6

    length_password_over_twelve_only_spacial_charts = "%@#$%$%$%$%$%$%$"
    r = main.password_strength(length_password_over_twelve_only_spacial_charts)
    j = json.loads(r.body)
    assert 200 == r.status_code
    assert j[RES] == 4


# ---------------------------------------------------------------------------
# TEST 11: test_server_time
#   Test the weekday calculation of server_time function: It returns a string that
#       includes a weekday ("Mon", "Tue"...) that is calculated based on the result
#       of c. We want to know it calculates the weekday correctly,
#       without waiting 1 day between tests. You need to stub get_network_time.
#       In this implementation, test the function main.server_time() directly,
#           not through the TestClient.
#   Use parameters, a single function should result in 7 tests, one for
#       each of the 7 days of the week.
#   Hint: You will need to use:
#       - "parametrize" with the test and the expected result,
#       - "monkeypatch" to overwrite the function in "extra" that provides time info
#       - "pytest.raises" because the function works by throwing a 203 exception
#   203: Non-Authoritative Information
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("weekday, expected_result", [
    ("Mon", "Mon"),
    ("Tue", "Tue"),
    ("Wed", "Wed"),
    ("Thu", "Thu"),
    ("Fri", "Fri"),
    ("Sat", "Sat"),
    ("Sun", "Sun"),
])

def test_server_time(monkeypatch, weekday, expected_result):
    def mock_get_network_time():
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        target_weekday = weekdays.index(weekday)
        current_date = datetime.datetime.now().date()
        while current_date.weekday() != target_weekday:
            current_date += datetime.timedelta(days=1)
            if current_date.day == 1:  # If it's the first day of the month, increment the month
                current_date = current_date.replace(month=current_date.month + 1, day=1)
                if current_date.month == 1:  # If it's January, increment the year
                    current_date = current_date.replace(year=current_date.year + 1)
        target_datetime = datetime.datetime.combine(current_date, datetime.datetime.min.time())
        return target_datetime

    # Patch the get_network_time() function with the custom implementation
    monkeypatch.setattr(extra, "get_network_time", mock_get_network_time)

    # Test the server_time() function and assert the result
    with pytest.raises(fastapi.exceptions.HTTPException) as exc_info:
        main.server_time()
    assert http_status.HTTP_203_NON_AUTHORITATIVE_INFORMATION == exc_info.value.status_code
    assert exc_info.value.detail[:3] == expected_result


# ---------------------------------------------------------------------------
# TEST 12: test_server_time_client
#   Test the weekday calculation of the "/time" REST call. You still need to
#       stub get_network_time.
#       In this implementation, test through the TestClient for easier code flow,
#           not by calling main.server_time() directly.
#
#   Instead of parametrizing, use metamorphic tests: For today's date (you don't need
#       to know which date or day it is), test that whatever weekday it received, the
#       following days (try the next 100) are of a weekday that is appropriate.
#   Hint: You will need to use:
#       - "monkeypatch" to overwrite the function in "extra" that provides time info
#       - fastapi's "TestClient" to run the REST API via a client and avoid the exception.
#       - a large loop and a smart way to check the weekday
#   203: Non-Authoritative Information
# ---------------------------------------------------------------------------
def test_server_time_client(monkeypatch):
    def create_next_day_generator():
        current_date = datetime.datetime.now()
        def get_next_day():
            nonlocal current_date
            next_day = current_date
            current_date += datetime.timedelta(days=1)
            return next_day
        return get_next_day
    monkeypatch.setattr(extra, "get_network_time", create_next_day_generator())

    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    today = datetime.datetime.now().weekday()

    num_days_to_check = 100
    for i in range(num_days_to_check):
        # monkeypatch.setattr(extra, "get_network_time", mock_get_network_time())
        response = client.get("/time")
        checking_weekday = (today + i) % 7
        assert response.status_code == 203
        assert weekdays[checking_weekday] == response.json()["detail"][:3]



# ---------------------------------------------------------------------------
# TEST 13: test_storage_db
#   Test the DB update function of the storage function: StateMachine.add_string()
#   You are looking to test that when "/storage/add?string=qwert" is called,
#       StateMachine.add_string() calls extra.update_db() correctly.
#   Checking that "/storage/query?index=1" is not enough, and it doesn't check
#       the extra.update_db() call.
#   Hint: You will need to use:
#       - "monkeypatch" to overwrite the update_db function in "extra".
#       - fastapi's "TestClient" to run the REST API via a client (it keeps the session alive).
#       - A function you invent that will mock update_db and update a flag for pass/fail (can be global)
# ---------------------------------------------------------------------------
db_update_called = False
def test_storage_db(monkeypatch):

    def check_update_db(a_db, value):
        global db_update_called
        try:
            if value is None:
                a_db.clear()
            else:
                a_db.append(value)
            db_update_called = True
        except:
            db_update_called = False

    monkeypatch.setattr(extra, "update_db", check_update_db)
    response = client.get("/storage/add?string=qwert")
    assert response.status_code == 200
    assert db_update_called is True





# ---------------------------------------------------------------------------
# TEST 14: Test the storage functions until it reaches 100% statement coverage.
#   That is, coverage of the "def storage" function and of all functions
#       within "class StateMachine" (lines 511-668).
#
#   Check coverage with the command "coverage run -m pytest", you can look at the functions
#       mentioned above with the HTML report: ("coverage html" and ".\htmlcov\index.html")
#   Hint: It is recommended to use:
#       - fastapi's "TestClient" to run the REST API via a client (it keeps the session alive).
# ---------------------------------------------------------------------------
def adding_five_words():
    response = client.get("/storage/add?string=first_word")
    response = client.get("/storage/add?string=second_word")
    response = client.get("/storage/add?string=third_word")
    response = client.get("/storage/add?string=forth_word")
    response = client.get("/storage/add?string=fifth_word")
    return response

def test_storage():
    # where in input mode but we did not add anything
    response = client.get("/storage/add")
    assert response.json()["res"] == "Ok"
    response = client.get("/storage/stop")
    assert response.json()["res"] == "Ok"

    # first example where we add a word clear it and then erase it
    response = client.get("/storage/add?string=first_word")
    assert response.json()["res"] == "Ok"
    assert response.status_code == http_status.HTTP_200_OK
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Input"
    response = client.get("/storage/clear")
    assert response.json()["res"] == "Ok"
    response = client.get("/storage/stop")
    assert response.json()["res"] == "Ok"
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "StandBy"

    # adding 5 words and checking that it finds all the words
    response = adding_five_words()
    assert response.json()["res"] == "Ok"
    response = client.get("/storage/query?index=1")
    assert response.json()["res"] == "first_word"
    response = client.get("/storage/query?index=2")
    assert response.json()["res"] == "second_word"
    response = client.get("/storage/query?index=3")
    assert response.json()["res"] == "third_word"
    response = client.get("/storage/query?index=4")
    assert response.json()["res"] == "forth_word"
    response = client.get("/storage/query?index=5")
    assert response.json()["res"] == "fifth_word"

    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Query"
    response = client.get("/storage/clear")
    assert response.json()["res"] == "Ok"
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Input"


    response = adding_five_words()
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Query"

    # adding to many values
    r = client.get("/storage/add?string=sorry_str")
    assert r.json()["res"] == "Error"
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Error"
    # reversing back to query postion
    r = client.get("/storage/sorry")
    assert r.json()["res"] == "Ok"
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Query"

    # index invalid
    response = client.get("/storage/query?index=6")
    assert response.json()["res"] == "Error"
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Error"
    response = client.get("/storage/clear")
    assert response.json()["res"] == "Ok"
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Input"

    response = adding_five_words()
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Query"
    response = client.get("/storage/stop")
    assert response.json()["res"] == "Ok"
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "StandBy"

    response = adding_five_words()
    response = client.get("/storage/query?index=6")
    assert response.json()["res"] == "Error"
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "Error"
    response = client.get("/storage/stop")
    assert response.json()["res"] == "Ok"
    response = client.get("/storage/state")
    assert response.json()["res"].split()[1][:-1] == "StandBy"





