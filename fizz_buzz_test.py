from fizz_buzz import fizz_buzz

if __name__ == "__main__":    
    assert fizz_buzz(2) == "2"
    assert fizz_buzz(4) == "4"
    assert fizz_buzz(149) == "149"
    assert fizz_buzz(-2) == "-2"
    
    assert fizz_buzz(3) == "fizz"
    assert fizz_buzz(6) == "fizz"
    assert fizz_buzz(81) == "fizz"
    
    assert fizz_buzz(5) == "buzz"
    assert fizz_buzz(10) == "buzz"
    assert fizz_buzz(1000) == "buzz"
    
    assert fizz_buzz(15) == "fizzbuzz"
    assert fizz_buzz(45) == "fizzbuzz"
    assert fizz_buzz(1515) == "fizzbuzz"
    
    assert fizz_buzz(4, 4, 6) == "fizz"
    assert fizz_buzz(8, 4, 6) == "fizz"
    assert fizz_buzz(64, 4, 6) == "fizz"
    
    assert fizz_buzz(6, 4, 6) == "buzz"
    assert fizz_buzz(6, 4, 6) == "buzz"
    assert fizz_buzz(18, 4, 6) == "buzz"
    assert fizz_buzz(54, 4, 6) == "buzz"
        
    assert fizz_buzz(12, 4, 6) == "fizzbuzz"
    assert fizz_buzz(24, 4, 6) == "fizzbuzz"
    assert fizz_buzz(144, 4, 6) == "fizzbuzz"
    