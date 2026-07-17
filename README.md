# Personal Finance & Wealth Planning System

## Overview:

The Personal Finance & Wealth Planning System is a Streamlit-based web application designed to help users better manage their finances. The application provides tools for budgeting, debt management, savings planning, investment profiling, and personalized financial recommendations.

The current version focuses on financial planning through rule-based analytics and recommendations, with future versions planned to incorporate machine learning and predictive analytics.

### Features

#### Budget Dashboard
    - Tracks monthly income and expenses
    - Calculates remaining cash flow
    - Displays savings rate
    - Visualizes spending patterns

#### Debt Planner  
    - Records debt balances and interest rates
    - Estimates debt repayment timelines
    - Provides debt management recommendations

#### Savings Goals Planner  
    - Tracks savings goals and progress
    - Calculates required monthly contributions
    - Evaluates whether users are on track to achieve their goals

#### Investment Profile Assessment  
    - Determines an investor's risk profile
    - Categorizes users as Conservative, Moderate, or Aggressive investors
    - Provides educational investment allocation suggestions

#### Financial Advisor
    - Combines information from the other modules
    - Generates personalized financial recommendations
    - Stores financial profile information for future analysis

### Current Recommendation Engine
The current version uses rule-based decision logic to generate recommendations based on factors such as:
- Savings rate
- Debt balance
- Debt interest rate
- Emergency fund coverage
- Investor profile

This serves as the foundation for future machine learning enhancements

### Technologies Used
- Python
- Streamlit
- SQLite
- Pandas
- Numpy
- Matplotlib


### Project Structure
pages/  
├── Budget_Dashboard.py  
├── Debt_Planner.py  
├── Savings_Goals.py  
├── Investment_Profile.py  
└── AI_Advisor.py 

src/   
├── calculations.py  
├── recommendations.py  
├── database.py  
├── visualizations.py  
└── ml_models.py 

### Screenshots
Screenshots of the application can be found in the images/ directory

### Installation

1. Clone the repository
2. Install the required dependencies:
   1. "pip install -r requirements.txt"
3. Launch the application
   1. "streamlit run 🏠_Home.py"


### Future Improvements
#### Planned enhancements include:
- Financial health scoring
- Spending behavior classification
- Expense forecasting
- Savings goal prediction
- Machine learning-based financial risk assessment
- Enhanced data visualization
- User Authentication and Profile management

### Disclaimer
This application is intended for educational and informational purposes only and should not be considered financial advice