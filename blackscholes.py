import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

class BlackScholes:
    """
    A class for calculating the Black-Scholes option pricing model and visualizing 
    profit and loss (PnL) for various combinations of spot prices and volatilities.

    Attributes:
        S (float): The price of the underlying stock.
        K (float): The strike price of the option.
        T (float): The time to expiry (in years).
        r (float): The risk-free interest rate (as a decimal).
        vol (float): The volatility of the stock (as a decimal).
        option_type (str): The type of option, either 'call' or 'put'.
    """

    def __init__(self, S, K, T, r, vol, option_type):
        """
        Initializes the BlackScholes class with the given parameters.

        Args:
            S (float): Price of the underlying stock.
            K (float): Strike price.
            T (float): Time to expiration (in years).
            r (float): Risk-free interest rate (as a decimal).
            vol (float): Volatility of the stock (as a decimal).
            option_type (str): Either 'call' or 'put'.
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.vol = vol
        self.option_type = option_type

    def calculate_price(self):
        """
        Calculates the Black-Scholes price of the option.

        Returns:
            float: The calculated price of the option.
        """
        d1 = (math.log(self.S/self.K) + (self.r + 0.5 * self.vol**2)*self.T) / (self.vol * math.sqrt(self.T))
        d2 = d1 - (self.vol * math.sqrt(self.T))

        if self.option_type == 'call':
            price = self.S * norm.cdf(d1) - self.K * math.exp(-self.r * self.T) * norm.cdf(d2)
        if self.option_type == 'put':
            price = self.K * math.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
        return price
    
    def generate_plot(self, S_min, S_max, vol_min, vol_max, purchase_price):
        """
        Generates a heatmap showing the profit and loss (PnL) for different 
        combinations of spot prices and volatilities.

        Args:
            S_min (float): Minimum value of the underlying stock price range.
            S_max (float): Maximum value of the underlying stock price range.
            vol_min (float): Minimum value of the volatility range.
            vol_max (float): Maximum value of the volatility range.
            purchase_price (float): The price at which the option was purchased.

        Returns:
            plt.figure: The generated heatmap figure.
        """
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