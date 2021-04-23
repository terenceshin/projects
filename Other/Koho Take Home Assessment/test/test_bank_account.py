import json
import os, sys
sys.path.append(os.path.dirname(os.path.abspath("main.py")))
import main

# Test 1: Results against output
def test_one():
    with open("results.txt") as f1:
        with open("output.txt") as f2:
            assert f1.read() == f2.read()

# Test 2: Check that transaction that exceeds daily limit is rejected
def test_two():

    test_input_2 = [{"id": "1", "customer_id": "1234", "load_amount": "$1000", "time": "2018-01-01T00:00:00Z" }, { "id": "2", "customer_id": "1234", "load_amount": "$4000.01", "time": "2018-01-01T00:00:00Z" }]
    
    open('test_output.txt', 'w').close()
    test_input_2 = main.main(test_input_2, "test_output.txt", text_file=False)
    
    with open("test_output.txt") as f1:
        with open("test/test_2.txt") as f2: 
            assert f1.read() == f2.read()

# Test 3: Check that transaction that exceed daily transactions is rejected
def test_three():

    test_input_3 = [{"id": "5", "customer_id": "1234", "load_amount": "$1", "time": "2019-01-01T00:00:00Z" }
                  , { "id": "6", "customer_id": "1234", "load_amount": "$1", "time": "2019-01-01T00:00:00Z" }
                  , { "id": "7", "customer_id": "1234", "load_amount": "$1", "time": "2019-01-01T00:00:00Z" }
                  , { "id": "8", "customer_id": "1234", "load_amount": "$1", "time": "2019-01-01T00:00:00Z" }]
    
    open('test_output.txt', 'w').close()
    test_input_3 = main.main(test_input_3, "test_output.txt", text_file=False)
    
    with open("test_output.txt") as f1:
        with open("test/test_3.txt") as f2: 
            assert f1.read() == f2.read()

# Test 4: Check that transaction that exceed weekly limit is rejected
def test_four():

    test_input_4 = [{"id": "20", "customer_id": "1234", "load_amount": "$5000", "time": "2021-04-20T00:00:00Z" }
                  , { "id": "21", "customer_id": "1234", "load_amount": "$5000", "time": "2021-04-21T00:00:00Z" }
                  , { "id": "22", "customer_id": "1234", "load_amount": "$5000", "time": "2021-04-22T00:00:00Z" }
                  , { "id": "23", "customer_id": "1234", "load_amount": "$5000", "time": "2021-04-23T00:00:00Z" }
                  , { "id": "24", "customer_id": "1234", "load_amount": "$5000", "time": "2021-04-24T00:00:00Z" }]
    
    open('test_output.txt', 'w').close()
    test_input_4 = main.main(test_input_4, "test_output.txt", text_file=False)
    
    with open("test_output.txt") as f1:
        with open("test/test_4.txt") as f2: 
            assert f1.read() == f2.read()

# Test 5: Check that duplicate ID is rejected, given that first one passed
def test_five():

    test_input_5 = [{"id": "50", "customer_id": "1235", "load_amount": "$1000", "time": "2021-04-20T00:00:00Z" }
                  , { "id": "50", "customer_id": "1235", "load_amount": "$500", "time": "2021-04-21T00:00:00Z" }]
    
    open('test_output.txt', 'w').close()
    test_input_5 = main.main(test_input_5, "test_output.txt", text_file=False)
    
    with open("test_output.txt") as f1:
        with open("test/test_5.txt") as f2: 
            assert f1.read() == f2.read()

# Test 6: Check that duplicate ID is rejected, even if the first one was rejected
def test_six():

    test_input_6 = [{"id": "60", "customer_id": "1237", "load_amount": "$7000", "time": "2021-04-20T00:00:00Z" }
                  , { "id": "60", "customer_id": "1237", "load_amount": "$500", "time": "2021-04-21T00:00:00Z" }]
    
    open('test_output.txt', 'w').close()
    test_input_6 = main.main(test_input_6, "test_output.txt", text_file=False)
    
    with open("test_output.txt") as f1:
        with open("test/test_6.txt") as f2: 
            assert f1.read() == f2.read()

# Test 7: Check to make sure transaction passes after a failed transaction (once new week starts)
def test_seven():

    test_input_7 = [{"id": "70", "customer_id": "7", "load_amount": "$5000", "time": "2021-04-20T00:00:00Z" }
                  , { "id": "71", "customer_id": "7", "load_amount": "$5000", "time": "2021-04-21T00:00:00Z" }
                  , { "id": "72", "customer_id": "7", "load_amount": "$5000", "time": "2021-04-22T00:00:00Z" }
                  , { "id": "73", "customer_id": "7", "load_amount": "$5000", "time": "2021-04-23T00:00:00Z" }
                  , { "id": "74", "customer_id": "7", "load_amount": "$5000", "time": "2021-04-24T00:00:00Z" }
                  , { "id": "75", "customer_id": "7", "load_amount": "$5000", "time": "2021-04-28T00:00:00Z" }]
    
    open('test_output.txt', 'w').close()
    test_input_7 = main.main(test_input_7, "test_output.txt", text_file=False)
    
    with open("test_output.txt") as f1:
        with open("test/test_7.txt") as f2: 
            assert f1.read() == f2.read()