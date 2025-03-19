# Black-Scholes Pricer

![Black-Scholes Pricer](https://img.shields.io/badge/streamlit-v1.0.0-blue)

## Description

The **Black-Scholes Pricer** is a web application that allows users to calculate the prices of call and put options using the Black-Scholes model. This application provides an interactive interface for inputting parameters, visualizing option prices, and generating profit and loss heatmaps. It utilizes the yfinance library to fetch real-time US Treasury yields for a realistic risk-free rate.

## Features

- **Interactive Input**: Users can input parameters such as the underlying price, strike price, time to expiry, volatility, and risk-free rate.
- **Realistic Risk-Free Rate**: Option to use real-time US Treasury yields.
- **Visualizations**: Generates profit and loss (PnL) heatmaps for both call and put options.
- **Responsive Design**: The application is designed to be responsive and user-friendly across various devices.

## Installation

To set up the Black-Scholes Pricer, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/black-scholes-pricer.git
   cd black-scholes-pricer

2. **Create a virtual environment**(optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate

3. **Install the required dependencies:**
   ```bash
    streamlit
    yfinance
    matplotlib
    seaborn
    scipy
    numpy
    shut

## Usage
To run the application, use the following command in your terminal
  ```bash
  streamlit run app.py
