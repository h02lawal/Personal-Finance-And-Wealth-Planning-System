# Personal Finance & Wealth Planning System

## Overview:

The Personal Finance & Wealth Planning System is a Streamlit-based financial planning application designed to help users organize and evaluate different aspects of their personal finances.

The system allows users to manage financial profiles, analyze monthly budgets, track multiple debts and savings goals, assess investment risk tolerance, and receive educational financial recommendations based on their financial information.

Version 2.0 expands the original application by introducing persistent SQLite storage, multiple financial profiles, multiple debt and savings records, and a more comprehensive financial assessment system.

## Version 2.0 :

This version includes persistent financial profiles and database-backed financial planning

Major improvements include :
  - Persistent Financial Profiles
  - Ability to create and load existing profiles
  - Database-backed budget information
  - Support for multiple debts per profile
  - Debt-specific analysis based on debt type
  - Support for multiple savings goals
  - Savings target dates and progress calculations
  - Expanded investment risk assessment
  - Financial risk classification
  - Financial health scoring
  - AI advisor aggregation of budget, debt, savings, and investment information

### Features

#### Budget Dashboard
    - Tracks monthly income and expenses
    - Calculates remaining cash flow
    - Displays savings rate
    - Visualizes spending patterns
    - Recommends minimum savings

#### Debt Planner  
    - It supports different debt types (credit cards, car loans, student loans, personal loans, and other types of debt)
    - Records debt balances and interest rates
    - Estimates debt repayment timelines
    - Provides debt management recommendations
    - It also allows users save multiple debts

#### Savings Goals Planner  
    - Tracks savings goals and progress
    - Calculates required monthly contributions
    - Evaluates whether users are on track to achieve their goals
    - It allows users have multiple saving goals

#### Investment Profile Assessment  
    - Determines an investor's risk profile
    - Categorizes users as Conservative, Moderate, or Aggressive investors
    - Provides educational investment allocation suggestions
    - It checks Job stability, Income Stability, Spending risk

#### Financial Advisor
    - Combines information from the other modules
    - Generates personalized financial recommendations
    - Stores financial profile information for future analysis

### System Architecture
financial_profile/  
|
├──< Debts  
|
├──< Savings

## Database Design
This version uses SQLite for persistent storage

### Financial profile 
  - Here it stores general financial and investment assessment information
### Debts
  - It stores individual debts associated with a financial profile
### Savings
  - It stores individual savings goals associated with a financial profile

This design creates one-to-many relationships between a financial profile and its debts and savings goals

For version 2 a rule based financial risk assessment and financial health score is used 

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
- User authentication
- Editable and deletable debts
- Editable and deletable savings goals
- Debt payment history
- Savings contribution history
- Transaction tracking
- Historical financial performance
- Improved financial dashboards
- More detailed debt repayment strategies
- Database normalization improvements
- Machine-learning-based financial risk prediction
- Improved profile management

### Disclaimer
This application is intended for educational and informational purposes only and should not be considered financial advice