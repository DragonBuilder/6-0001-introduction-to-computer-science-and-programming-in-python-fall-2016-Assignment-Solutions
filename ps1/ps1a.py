# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 17:02:52 2018

@author: White Dragon
"""

def calc_months():
     """
    Asks the Annual salary, the portion of the salary the person intends to save
    and the total cost of the house and prints of the number of months it would take 
    for the person to be able to save enough for the down payment , which in this case 
    is harcoded to 25%
    
    """
    annual_salary = float(input("Annual Salary: "))
    portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
    total_cost = float(input("Enter the cost of your dream home: "))
    portion_down_payment = .25
    current_savings = 0
    r = .04;
    monthly_salary = annual_salary / 12
    
    months = 0
    
    while(current_savings < total_cost * portion_down_payment):
        current_savings += (current_savings * r /12) + (portion_saved * monthly_salary)
        months += 1
        
    print("Number of Months: ", months)
    
calc_months()


