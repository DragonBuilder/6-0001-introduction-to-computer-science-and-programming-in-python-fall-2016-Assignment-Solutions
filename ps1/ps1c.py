# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 18:04:12 2018

@author: White Dragon
"""
          
            
def calc_savings_needed():
    """
    Asks the Annual salary, the portion of the salary the person intends to save
    and the total cost of the house and the semi annual raise on the salary as decimal
    and prints of the number of months it would take for the person to be able to 
    save enough for the down payment , which in this case is harcoded to 25%.
    
    """
    annual_salary_real = float(input("Starting Salary: "))
    #portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
    total_cost = 1000000#float(input("Enter the cost of your dream home: "))
    semi_annual_raise = .07#float(input("Enter the semi annual raise as decimal: "))
    portion_down_payment = .25
    current_savings = 0
    r = .04;
    monthly_salary = annual_salary_real / 12    
    
    months = 36
    epsilon = 100
    low = 0.0
    high = 1.0
    guess = (low + high) / 2.0
    num_guesses = 0
    breaked = False
    
    while(abs(current_savings - total_cost*portion_down_payment) > epsilon):
        if(guess == 1.0):
            breaked = True
            break
        #print("new guess: ",guess)
        annual_salary = annual_salary_real
        monthly_salary = annual_salary/12
        num_guesses += 1 
        
        month = 0
        current_savings = 0
        while( month < months):
            
            current_savings += (current_savings * r /12) + (guess * monthly_salary)
            month += 1
            if ((month % 6) == 0):
                annual_salary += annual_salary * semi_annual_raise
                monthly_salary = annual_salary / 12
                 
        if(abs(current_savings - (total_cost*portion_down_payment)) > epsilon):
            #print("current_savings: ",current_savings)
            if(current_savings < (total_cost*portion_down_payment)):
                low = guess
            else:
                high = guess
            guess = (low + high) / 2.0
            
    if(breaked):
        print("It is not possible to pay down payment in 3 years.")
    else:         
        print("Best savings rate: ", guess)
        print("Steps in bisection search: ", num_guesses)
        
        
                
        
#    print("Number of Months: ", months)
    
calc_savings_needed()