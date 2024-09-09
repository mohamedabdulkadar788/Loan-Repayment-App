import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

st.title('Mortage Repayments Calculator:')

st.write('### Input Data')
col1, col2 = st.columns(2)
home_value = col1.number_input('Home Value', min_value=0, value=500000)
deposit = col1.number_input('Deposit', min_value=0, value=100000)
interest_rate = col2.number_input('Interest Rate(%)', min_value=0.0, value=5.5)
loan_term = col2.number_input('Loan Term(years)', min_value=1, value=30)

#Formulas
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate/100)/12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount*(monthly_interest_rate*(1+monthly_interest_rate)**number_of_payments)/
    ((1+monthly_interest_rate)**number_of_payments-1)
)

total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write('### Repayments')
col1, col2, col3 = st.columns(3)
col1.metric(label='Monthly_Repayments', value=f'${monthly_payment:,.2f}')
col2.metric(label='Total_Repayments', value=f'${total_payments:,.0f}')
col3.metric(label='Total_Interest', value=f'${total_interest:,.0f}')

# creating a dataframe with the payment schedule:

schedule = []
remaining_balance = loan_amount

import math

for i in range(1,number_of_payments+1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i/12) #calc year into loan
    schedule.append([
        i, monthly_payment, principal_payment, interest_payment, remaining_balance, year
    ])
    
#Dataframe:

df = pd.DataFrame(schedule, columns=['Month', 'Payment', 'Principal', 'Interest', 'Remaining Balance', 'Year'])

st.write('### payment schedule')
payments_df = df[['Year', 'Remaining Balance']].groupby('Year').min()
st.line_chart(payments_df)

