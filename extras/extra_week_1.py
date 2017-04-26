"""
Plots fizz_buzz returns to demonstrate capability of matplotlib.    
"""
import matplotlib.pyplot as plt
from fizz_buzz import fizz_buzz
   
    
if __name__ == "__main__":
    # map, lambda, enumerate, plotting
        
    nums = []
    fizz = []
    buzz = []
    fizzbuzz = []
    for i in range(1,31):
        val = fizz_buzz(i)
        if val == "fizzbuzz":
            fizzbuzz.append(i)
        elif val == "fizz":
            fizz.append(i)
        elif val == "buzz":
            buzz.append(i)
        else:
            nums.append(i)
    
                
    plt.scatter(nums, nums, c='g')
    plt.scatter(fizz, fizz, c='r')
    plt.scatter(buzz, buzz, c='b')
    plt.scatter(fizzbuzz, fizzbuzz, c='y')
    
    import matplotlib as mpl
    import numpy as np
    
    cmap = mpl.cm.rainbow(np.linspace(0,1,4))
    plt.scatter(nums, nums, c=cmap[0])
    plt.scatter(fizz, fizz, c=cmap[1])
    plt.scatter(buzz, buzz, c=cmap[2])
    plt.scatter(fizzbuzz, fizzbuzz, c=cmap[3])
    
    