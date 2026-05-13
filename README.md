# SmartVest

Python package for personalized investment advisory.
Built for FE520: Introduction to Python for Financial Applications, Spring 2026.

Vidhi Babariya (20033143) and Om Boghra (20033029)
Stevens Institute of Technology, Schaefer School of Science and Engineering

---

## What it does

SmartVest is for first-time investors who do not know where to start. You fill out a short questionnaire about your income, savings, debt, and goals. The app calculates your risk score, picks a portfolio that fits your profile, shows how your money could grow over time, and fetches live market data for every ticker it recommends. Each session is saved so you can come back and view past profiles.

---

## Setup

Python 3.10 or above is required.

```bash
git clone https://github.com/Vid-02/smartvest.git
cd smartvest
pip3 install -r requirements.txt
python3 main.py
```

---

## Project Structure

```
smartvest/
|
|-- main.py                   # runs the full pipeline
|-- requirements.txt          # dependencies
|-- README.md
|-- investor_profiles.csv     # created automatically on first run
|
|-- smartvest/
    |-- __init__.py           # package exports
    |-- profile.py            # questionnaire and financial ratios
    |-- risk.py               # risk scoring and classification
    |-- recommendation.py     # portfolio allocations and growth projections
    |-- analysis.py           # yfinance data, metrics, and charts
    |-- storage.py            # saves and loads investor sessions
```

---

## Modules

### profile.py

Collects 13 inputs from the user: name, age, employment status, annual income, monthly expenses, current savings, monthly investment, existing debt, number of dependents, investment horizon, goal, risk comfort level, and loss tolerance. All inputs are validated in a loop before being accepted.

After collection, four financial ratios are calculated:

| Ratio | Formula |
|---|---|
| Savings Rate | (Monthly Investment / Monthly Income) x 100 |
| Debt to Income | (Total Debt / Annual Income) x 100 |
| Emergency Fund Coverage | Current Savings / (Monthly Expenses x 6) |
| Investment Capacity | (Monthly Investment / Monthly Expenses) x 100 |

Author: Om Boghra

---

### risk.py

Calculates a risk score from 0 to 100 based on the investor profile and financial ratios, then places the user into one of three categories.

Scoring breakdown:

| Factor | Points |
|---|---|
| Age | +20 |
| Annual income | +20 |
| Current savings | +15 |
| Investment horizon | +15 |
| Risk comfort (rated 1 to 5) | +15 |
| Monthly investment | +10 |
| Loss tolerance (buy / hold / sell) | +10 |
| Emergency fund bonus | +5 |
| Savings rate bonus | +5 |
| Debt to income penalty | up to -15 |
| Dependents penalty | up to -10 |

Risk categories:

| Score | Category | Focus |
|---|---|---|
| 0 to 35 | Conservative | Capital preservation, bonds, dividend stocks |
| 36 to 65 | Moderate | Balanced mix of index funds, REITs, bonds |
| 66 to 100 | Aggressive | Growth ETFs, small cap stocks, emerging markets |

Author: Om Boghra

---

### recommendation.py

Takes the risk category and investment goal and returns a portfolio allocation with specific tickers, goal-specific advice, and a monthly breakdown showing how much goes into each asset.

Portfolio growth is projected using the compound interest formula with monthly contributions:

```
FV = P x [((1 + r)^n - 1) / r] + S0 x (1 + R)^T

P  = monthly investment
r  = monthly return rate (annual rate divided by 12)
n  = total months
S0 = current savings
R  = expected annual return
T  = investment horizon in years
```

Three scenarios are shown: base case, best case (plus one standard deviation), and worst case (minus one standard deviation).

The seven supported goals are: retirement, home, education, wealth, emergency, travel, and business.

Expected annual returns used:

| Category | Expected Return | Standard Deviation |
|---|---|---|
| Conservative | 4.5% | 5% |
| Moderate | 7.5% | 10% |
| Aggressive | 10.0% | 18% |

Author: Vidhi Babariya

---

### analysis.py

Fetches one year of daily adjusted closing prices for the recommended tickers using yfinance. For each ticker it calculates:

| Metric | How it is calculated |
|---|---|
| Total Return | (Last price - First price) / First price x 100 |
| Annualised Return | Geometric return scaled to one year |
| Volatility | Standard deviation of daily returns x sqrt(252) x 100 |
| Sharpe Ratio | (Annualised return - 4.5%) / Volatility |

Three charts are generated and saved as PNG files:

1. portfolio_allocation.png: pie chart of the recommended asset weights
2. historical_performance.png: one year of normalised price performance for all tickers, starting at 100
3. projected_growth.png: portfolio value over the investment horizon under all three scenarios

Author: Both

---

### storage.py

Saves each session to investor_profiles.csv. New rows are appended so no previous data is lost. At startup, the user can choose to view a table of all past sessions.

Author: Vidhi Babariya

---

## Packages

| Package | Used for |
|---|---|
| yfinance | Historical market data for recommended tickers |
| pandas | Handling price data and time series |
| numpy | Volatility, Sharpe Ratio, and projection calculations |
| matplotlib | All three charts |
| datetime | Timestamping saved profiles |
| csv, os | Reading and writing the profiles CSV file |

---

## Error Handling

All five modules use try-except blocks. Bad inputs, missing fields, division by zero, and file read or write failures are all caught and reported without stopping the program.

---

## Disclaimer

SmartVest is an educational project for FE520. It is not financial advice. All projections are estimates based on historical return assumptions. Speak to a licensed financial advisor before making any investment decisions.