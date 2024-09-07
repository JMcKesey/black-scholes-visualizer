import streamlit as st
import yfinance as yf
from blackscholes import BlackScholes

# configuring default settings of the page
st.set_page_config(
    page_title='Black-Scholes Pricer', 
    page_icon='📈', 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items=None,
)

# session state
if 'disabled' not in st.session_state:
    st.session_state.disabled = False

# giving the page a title
st.title("📈 Black-Scholes :grey[Model]")

# Intializing two columns with a 2 to 8 size ratio
col1, col2= st.columns([2, 8])

with col1:
    st.header("🔢 Inputs")

    # inputs
    S = st.number_input("Price of the underlying", min_value=0.01, value=100.00)
    K = st.number_input("Strike Price", min_value=0.01, value=100.00)
    T = st.number_input("Time to expiry (Years)", min_value=0.01, value=2.00)
    vol = st.number_input("Volatility", min_value=0.01, value=0.05)
    r = st.number_input("Risk-free rate", 
                        min_value=0.01, 
                        value=0.05,
                        disabled=st.session_state.disabled,
                        )

    # toggle button to use us treasury yields
    on = st.toggle("Realistic Risk-free rate", 
                   key="disabled",
                   help="realistic risk-free rate uses US 3 month yields")

    if on:
        treasury_bill = yf.Ticker("^IRX")
        data = treasury_bill.history()
        last_quote = data['Close'].iloc[-1]
        r = last_quote / 100

    st.divider()

    st.header("🔥 Heatmap inputs")

    # inputs
    purchase_price = st.number_input("Purchase Price", min_value=0.00, value=100.00)    
    S_min = st.number_input("Minimum price of they underlying", min_value=0.00, value=50.00)
    S_max = st.number_input("Maximum price of they underlying", min_value=0.00, value=150.00)

    vol_min = st.slider("Minimum volatility", 
                        min_value=0.01, max_value=1.00, step=0.01)
    vol_max = st.slider("Maximum volatility",
                        min_value=0.01, max_value=1.00, step=0.01)

with col2:
    # make instances of our BlackScholes class
    BS_call = BlackScholes(S, K, T, r, vol, option_type="call")
    BS_put = BlackScholes(S, K, T, r, vol, option_type="put")

    # Calculate call and put prices
    call_price = BS_call.calculate_price()
    put_price = BS_put.calculate_price()

    # Calculate deltas by comparing with purchase price
    call_delta = call_price - purchase_price
    put_delta = put_price - purchase_price

    st.header("🌌Black-Scholes Pricing Model",
            help="the delta corresponds to the purchase price of the call/put")

    # Custom CSS for borders and conditional delta coloring
    st.markdown(f"""
        <style>
        .metric-container-call {{ 
            border-radius: 7px;
            padding: 10px;
            margin-bottom: 10px;
            text-align: center;
            background-color: #9edb6b;
        }}
        .metric-container-put {{
            border-radius: 7px;
            padding: 10px;
            margin-bottom: 10px;
            text-align: center;
            background-color: #ed6666;
        }}
        .metric-label {{
            font-weight: bold;
        }}
        .metric-value {{
            font-size: 24px;
        }}
        .metric-delta {{
            font-size: 18px;
        }}
        .delta-positive {{
            color: green;
        }}
        .delta-negative {{
            color: red;
        }}
        </style>
        <div class="metric-container-call">
            <div class="metric-label">CALL Value</div>
            <div class="metric-value">{call_price: .2f}</div>
            <div class="metric-delta {'delta-positive' if call_delta >= 0 else 'delta-negative'}">{call_delta: .2f}</div>
        </div>
        <div class="metric-container-put">
            <div class="metric-label">PUT Value</div>
            <div class="metric-value">{put_price: .2f}</div>
            <div class="metric-delta {'delta-positive' if put_delta >= 0 else 'delta-negative'}">{put_delta: .2f}</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.header("💵 PnL HeatMap",
              help="The values within the map correpsond the the ($) PnL per option excercised")

    col21, col22 = st.columns(2)
    with col21:
        call_fig = BS_call.generate_plot(S_min, S_max, vol_min, vol_max, purchase_price=purchase_price)
        st.pyplot(call_fig)
    with col22:
        put_fig = BS_put.generate_plot(S_min, S_max, vol_min, vol_max, purchase_price=purchase_price)
        st.pyplot(put_fig)
    

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
padding-top: 10px;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: inline; text-align: center;' href="https://www.linkedin.com/in/jmckesey/" target="_blank">Jonathan D. McKesey</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)