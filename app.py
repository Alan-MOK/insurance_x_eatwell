import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import fsolve
import hmac




def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

# Main Streamlit app starts here
st.write("Here goes your normal Streamlit app...2")
st.button("Click me")





# def page_config():
#     img = 'https://reimage.cfo-ai.com/assets/images/icon/powered_logo.svg'
#     st.set_page_config(
#         "INSURANCE x EATWELL",
#         # img,
#         initial_sidebar_state="expanded",
#         layout="wide",
#     )
# page_config()


def add_commas(number):
    # Convert the number to a string
    num_str = str(number)
    
    # Split the number into integer and decimal parts (if applicable)
    integer_part, decimal_part = num_str.split(".") if "." in num_str else (num_str, "")
    
    # Add commas to the integer part
    integer_with_commas = ""
    for i, digit in enumerate(reversed(integer_part)):
        if i > 0 and i % 3 == 0:
            integer_with_commas = "," + integer_with_commas
        integer_with_commas = digit + integer_with_commas
    
    # If there is a decimal part, add it back to the formatted integer part
    formatted_number = integer_with_commas + ("." + decimal_part if decimal_part else "")
    
    return formatted_number

# the UI of the front end
# part 1 side bar
# part 2 the main display page

# Side bar
with st.sidebar:
    st.title("Your Plan Options")

    # Insurance Type
    insurance_type_s = st.selectbox(
        "Please Select an Insurance Type",
        ("Life Only", "Cancer Only", "Serious Illness Only", "Accident Rate")
    )
    if insurance_type_s == 'Life Only':
        insurance_type = 1/140
    elif insurance_type_s == 'Cancer Only':
        insurance_type = 0.01
    elif insurance_type_s == 'Serious Illness Only':
        insurance_type = 0.02
    else:
        insurance_type = 0.001
    # st.write('The current number is ', insurance_type)
    st.title(" ")

    # Insurance Amount
    insurance_amount_s = st.select_slider(
        "Insurance Amount",
        options = ['100k', '500k', '1m','2m','5m'],
    )
    if insurance_amount_s == '100k':
        insurance_amount = 100000
    elif insurance_amount_s == '500k':
        insurance_amount = 500000
    elif insurance_amount_s == '1m':
        insurance_amount = 1000000
    elif insurance_amount_s == '2m':
        insurance_amount = 2000000
    else:
        insurance_amount = 5000000
    # st.write('The current number is ', insurance_amount)
    st.title(" ")

    # Payment  options
    payment_opt_s = st.selectbox(
        "Please Select a Payment Options",
        ("Single Payment", "10 Years", "15 Years", "20 Years")
    )
    if payment_opt_s == 'Single Payment':
        payment_opt = 1
    elif payment_opt_s == '10 Years':
        payment_opt = 10
    elif payment_opt_s == '15 Years':
        payment_opt = 15
    else:
        payment_opt = 20
    # st.write('The current number is ', payment_opt)
    st.title(" ")

    # Maturity Term
    min_value = max(11, payment_opt)
    maturity_term = st.select_slider(
        "Maturity Term (year)",
        options = np.arange(min_value, 51),
        value = 20
    )
    # st.write('The current number is ', maturity_term)
    st.title(" ")

    # health improvement
    health_improvement = st.select_slider(
        "Health Improvement (0%, 100%])",
        options = np.arange(0, 101, 5),
        value = 30
    )
    # st.write('The current number is ', health_improvement)
    health_improvement = health_improvement/100
    st.title(" ")


    st.title("Personal info")
    annual_salary = st.number_input(
        "Your Annual Salary    (step: 1000)", 
        min_value = 100000,
        value = 179900, 
        step = 1000
        )
    st.write('The current number is  $', add_commas(annual_salary))



'''
    # INSURANCE DEMO:
'''

# initiate some value
fixed_income_asset_coupon = 0.05
high_alpha_asset_mean = 0.12
max_DD = 0.3
discount_rate = 0.03
RoPfactor = 4
fixed_income_portion = 0.75
high_alpha_portion = 0.25
profit_share = 0.5



# Create the first column from 1 to 20
column_1 = list(range(1, 21))

# Create the second column based on the condition
column_2 = [1 if x <= payment_opt else 0 for x in column_1]

# Create the third column based on the condition
column_3 = [(1+fixed_income_asset_coupon)**(maturity_term + 1 - x) for x in column_1]

# Create the forth column based on the condition
column_4 = [max(1, (1+high_alpha_asset_mean)**(maturity_term + 1 - x) * (1 - max_DD)) for x in column_1]

# Create the fifth column using the specified formula
column_5 = [0.5 * x + 0.5 * y for x, y in zip(column_3, column_4)]

# Create the sixth column using the specified formula
margin = 0.4
PVannuity = (1 - (1 / (1 + discount_rate)**maturity_term))/(discount_rate/(1+discount_rate))
insurance_risk = insurance_type * PVannuity * insurance_amount * (1+margin)
prem_payment_PV = (1 - (1 / (1+discount_rate)**payment_opt))/(discount_rate/(1+discount_rate))
risk_prem = insurance_risk/prem_payment_PV
column_6 = [risk_prem * x * y for x, y in zip(column_2, column_5)]

# Create the seventh column using the specified formula
column_7 = [risk_prem * x for x in column_2]

# Create the eigth column using the specified formula
column_8 = [(RoPfactor - 1) * x for x in column_7]

# Create the ninth column using the specified formula
column_9 = [fixed_income_portion * x for x in column_8]

# Create the tenth column using the specified formula
column_10 = [high_alpha_portion * x for x in column_8]

# Create the 11 column using the specified formula
column_11 = [x * y for x, y in zip(column_3, column_9)]

# Create the 12 column using the specified formula
column_12 = [x * y for x, y in zip(column_4, column_10)]

# Create the 13 column using the specified formula
column_13 = [x + y for x, y in zip(column_11, column_12)]

goal_seek = 1.4
terminal_bonus =0.2
# Define the equation
def goalseek_cell(goal_seek):

    column_14 = [risk_prem * (goal_seek-1) for _ in range(len(column_1))]
    column_15 = [x * y for x, y in zip(column_3, column_14)]
    sum_FV = sum(column_15)
    return risk_prem * goal_seek * payment_opt * (1+terminal_bonus) - sum_FV
# Use fsolve to find the root of the equation (where equation(x) equals the target value)
goal_seek = fsolve(goalseek_cell, 0)[0]  # Start the search from initial guess x=0



# Define the equation
def goalseek_cell_2(RoPfactor):

    column_8 = [(RoPfactor - 1) * x for x in column_7]
    column_9 = [fixed_income_portion * x for x in column_8]
    column_10 = [high_alpha_portion * x for x in column_8]
    column_11 = [x * y for x, y in zip(column_3, column_9)]
    column_12 = [x * y for x, y in zip(column_4, column_10)]
    column_13 = [x + y for x, y in zip(column_11, column_12)]
    sum_income_FV = sum(column_11)
    
    return sum_income_FV/(risk_prem*RoPfactor*payment_opt)
# Use fsolve to find the root of the equation (where equation(x) equals the target value)
RoPfactor = fsolve(lambda x: goalseek_cell_2(x) - 1, 4)[0]  # Start the search from initial guess x=0


# Create the 8-14 column using the specified formula
column_8 = [(RoPfactor - 1) * x for x in column_7]
column_9 = [fixed_income_portion * x for x in column_8]
column_10 = [high_alpha_portion * x for x in column_8]
column_11 = [x * y for x, y in zip(column_3, column_9)]
column_12 = [x * y for x, y in zip(column_4, column_10)]
column_13 = [x + y for x, y in zip(column_11, column_12)]
column_14 = [risk_prem * (goal_seek-1) for _ in range(len(column_1))]
column_15 = [x * y for x, y in zip(column_3, column_14)]
ROP = pd.DataFrame(
    {
    'index': column_1,
    'prem_pmt_optn': column_2,
    'Income': column_3,
    "High Alpha": column_4,
    'column_5':column_5,
    'column_6': column_6,
    'Risk_Premium': column_7,
    'Premium_Invested': column_8,
    'Fixed_Income': column_9,
    'high_alpha_portion': column_10,
    "Expected Future Value Fixed-Inc": column_11,
    'Expected Future Value High-Alpha': column_12,
    'column_13': column_13,
    'Fixed Income': column_14,
    'Future Value': column_15
}
)

final_premium = int(risk_prem*RoPfactor*100)/100

# main diplay page
main_display, tab_concept, RoP_Table, other_metric= st.tabs(["Main Display", "Concept", 'RoP Table', 'Others'])

with main_display:
    col1, col2= st.columns([4,6])
    font_size = 26
    with col1:
        st.markdown(f"<p style='font-size: {font_size}px; text-align: left;'>Calculated Annual Premium.</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: {font_size}px; text-align: left;'>Annual Premium ${add_commas(final_premium)}</p>", unsafe_allow_html=True)
        
        # if annual_salary == None:
        #     number_str = str(final_premium)
        #     decimal_index = number_str.index('.')
        #     digits_before_decimal = number_str[:decimal_index]
        #     num_digits_before_decimal = len(digits_before_decimal)
        #     annual_salary = int(final_premium/0.1 / 10**(num_digits_before_decimal-1)) * 10**(num_digits_before_decimal-1)


    with col2:
        prem_D_salary = final_premium/annual_salary
        prem_D_salary_plt = int(prem_D_salary*1000)/10
        if prem_D_salary >= 1:
            st.error(f"{prem_D_salary_plt}% of Annual Salary")
        else:
            st.subheader(f"{prem_D_salary_plt}% of Annual Salary")
    
    
        # # Sample data for the pie chart
        # labels = ['Annual Salary', 'Annual Premium']
        # values = [(annual_salary-final_premium),final_premium]  # Sample values for the categories

        # # Create a pie chart using Plotly with custom size
        # fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
        # fig.update_layout(height=500, width=500)  # Set custom height and width

        # # Display the pie chart using Streamlit
        # st.plotly_chart(fig)
    
    
    st.header(" ")
    st.header(" ")
    col1, col2= st.columns([4,6])
    with col1:
        Total_prem = int(risk_prem*RoPfactor*payment_opt)
        Total_prem_c = add_commas(Total_prem)
        st.markdown(f"<p style='font-size: {font_size}px; text-align: left;'>Total Premium: $ {Total_prem_c}</p>", unsafe_allow_html=True)

        RoP_Plus_investwell_bonus = int(ROP['Expected Future Value High-Alpha'].sum()+(risk_prem*payment_opt*RoPfactor))
        RoP_Plus_investwell_bonus_c = add_commas(RoP_Plus_investwell_bonus)
        st.markdown(f"<p style='font-size: {font_size}px; text-align: left;'>RoP Plus investwell bonus : $ {RoP_Plus_investwell_bonus_c}</p>", unsafe_allow_html=True)
                                                            
        After_Eatwell_Health_Factor = int(RoP_Plus_investwell_bonus + profit_share*insurance_risk*health_improvement*((1+fixed_income_asset_coupon)**maturity_term))
        After_Eatwell_Health_Factor_c = add_commas(After_Eatwell_Health_Factor)
        st.markdown(f"<p style='font-size: {font_size}px; text-align: left;'>After Eatwell Health Factor : $ {After_Eatwell_Health_Factor_c}</p>", unsafe_allow_html=True)

    with col2:
        # # Bar chart plot
        categories = ['Return of Premium', 'RoP Plus investwell', 'After Eatwell']
        values = [Total_prem, RoP_Plus_investwell_bonus, After_Eatwell_Health_Factor]

        # Create a bar chart using Plotly
        fig = go.Figure(data=[go.Bar(x=categories, y=values)])

        # Control the size of the chart
        fig.update_layout(
            height=800,  # Set the height of the chart
            title="Maturity Value",
            title_font=dict(size=28)
        )
        fig.update_xaxes(tickfont=dict(size=20))
        # Display the bar chart using Streamlit
        st.plotly_chart(fig, use_container_width=True, config={'responsive': True})



with tab_concept:
    st.markdown("**1. use a simple decrement model to determine the insurance risk factor**")
    point_1 = '''
    - the pure risk premium
    - given the coverage duration and insurance amount
    - given discount rate
    '''
    st.markdown(point_1)

    st.markdown("**2. use the fixed income assumption to determine the amount needed for the RoP**")
    point_2 = '''
    - given the fixed income investment income interest rate e.g. the infrastructure projects
    > coupon : 5%
    '''
    st.markdown(point_2)

    point_3 = '''
    - given also the anticipated expected return and variance of the high performance asset
    > mean 12%

    > variance: 18% - variance is highly correlated to potential draw-down / failure

    > max DD: 30% - maximum draw-down puts a margin for failure of the strategy
    '''
    st.markdown(point_3)
    
    point_4 = '''
    - calculate the multiple of risk premium needed to provide an RoP
    - calculate the mulitple of risk premium needed for the terminal bonus
    - assume that the premium is invested 50% in fixed income 50% high alpha
    '''
    st.markdown(point_4)

    st.markdown("**3. fixed income to high-alpha investments - regulatory pressures will ultimately determine what we can invest**")
    point_5 = '''
        > fixed income portion: 75% - these are the infrastructure projects with large cashflows
        high alpha portion		25%	- these are our investwell strategy
        '''
    st.markdown(point_5)

    point_6 = '''
        > high alpha portion: 25% - these are our investwell strategy
        '''
    st.markdown(point_6)



with RoP_Table:
    st.table(ROP)


with other_metric:
    st.subheader("all metric in ROP worksheet")
    st.write(f"RoP factor: {RoPfactor*100}%")
    # st.write(f"RoP factor goal seek: {goal_seek*100}%")
    st.write(f"Risk Premium: {add_commas(int(risk_prem))}")
    st.write(f'Fixed Income Asset: {add_commas(int(risk_prem*(goal_seek-1)))}')
    st.write(f"Final goal seek premium: {add_commas(final_premium)}")

    st.subheader(" ")
    st.subheader('All metric in the blue cell of Product setup')
    st.write(f"Premium: {add_commas(final_premium)}")
    high_alpha_FV = ROP['Expected Future Value High-Alpha'].sum()
    st.write(f'calculated bonus: {add_commas(int(high_alpha_FV))}')
    st.write(f'as percent of RoP: {int(high_alpha_FV/(risk_prem*RoPfactor*payment_opt)*100)}%')
    st.write(f"total maturity value: {add_commas(int(high_alpha_FV+(risk_prem*RoPfactor*payment_opt)))}")
    st.write(f"calculated premium: {add_commas(int(risk_prem*RoPfactor))}")
    st.write(f"a health factor bonus: {add_commas(int(profit_share*insurance_risk*health_improvement*((1+fixed_income_asset_coupon)**maturity_term)))}")
    st.write(f"likely maturity value: {add_commas(int(RoP_Plus_investwell_bonus + profit_share*insurance_risk*health_improvement*((1+fixed_income_asset_coupon)**maturity_term)))}")




 
