import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

class BlackScholes:
    def __init__(self, S, K, T, r, vol, option_type):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.vol = vol
        self.option_type = option_type

    def calculate_price(self):
        d1 = (math.log(self.S/self.K) + (self.r + 0.5 * self.vol**2)*T) / (self.vol * math.sqrt(self.T))
        d2 = d1 - (self.vol * math.sqrt(self.T))

        if self.option_type == 'call':
            price = self.S * norm.cdf(d1) - self.K * math.exp(-self.r * self.T) * norm.cdf(d2)
        if self.option_type == 'put':
            price = self.K * math.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
        return price
    
    def generate_plot(self, S_min, S_max, vol_min, vol_max, purchase_price):
        S_range=np.linspace(S_min, S_max, 10) # range of spot prices
        vol_range=np.linspace(vol_min, vol_max, 10) # range of volatilities

        pnl = np.zeros((len(vol_range), len(S_range)))

        # calculate pnl for each combination of spot and vol
        for i, self.vol in enumerate(vol_range):
            for j, self.S in enumerate(S_range):
                option_price=BlackScholes.calculate_price(self)
                pnl[i, j] = option_price - purchase_price

        # plotting pnl heatmap
        plt.figure(figsize=(8, 8))
        sns.heatmap(pnl, xticklabels=np.round(S_range, 2), yticklabels=np.round(vol_range, 2), 
                    annot=True,
                    fmt=".2f",
                    cmap="RdYlGn",
                    cbar=False,
                    center=0,
                    cbar_kws={'label': 'PnL'})
        plt.xlabel('Spot Price (S)')
        plt.ylabel('Volatility (vol)')
        plt.title(f'PnL Heat Map for {self.option_type.capitalize()} Option')
        return plt


# configuring default settings of the page
st.set_page_config(
    page_title='Black-Scholes Pricer', 
    page_icon='📈', 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items=None
)

st.title("📈 Black-Scholes :grey[Model]")

col1, col2= st.columns([2, 8])

with col1:
    st.header("🔢 Inputs")
    S = st.number_input("Price of the underlying", min_value=0.01, value=100.00)
    K = st.number_input("Strike Price", min_value=0.01, value=100.00)
    T = st.number_input("Time to expiry (Years)", min_value=0.01, value=2.00)
    r = st.number_input("Risk-free rate", min_value=0.01, value=0.05)
    vol = st.number_input("Volatility", min_value=0.01, value=0.05)

    st.divider()

    st.header("🔥 Heatmap inputs")

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

    st.header("🌌Black-Scholes Pricing Model")
    st.write("\* the delta corresponds to the purchase price of the call/put")

    # Custom CSS for borders and conditional delta coloring
    st.markdown(f"""
        <style>
        .metric-container {{
            border: 2px solid #000;
            border-radius: 7px;
            padding: 10px;
            margin-bottom: 10px;
            text-align: center;
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
        <div class="metric-container">
            <div class="metric-label">CALL Value</div>
            <div class="metric-value">{call_price: .2f}</div>
            <div class="metric-delta {'delta-positive' if call_delta >= 0 else 'delta-negative'}">{call_delta: .2f}</div>
        </div>
        <div class="metric-container">
            <div class="metric-label">PUT Value</div>
            <div class="metric-value">{put_price: .2f}</div>
            <div class="metric-delta {'delta-positive' if put_delta >= 0 else 'delta-negative'}">{put_delta: .2f}</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.header("💵 PnL HeatMap")
    st.write("The values in the heat map changed based off of user input")

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