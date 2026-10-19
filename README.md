# 💰 Personal Finance & Wealth Planning System

## 📌 Overview

The **Personal Finance & Wealth Planning System** is a Streamlit-based financial planning application designed to help users organize, track, and evaluate different aspects of their personal finances.

The system allows users to manage financial profiles, analyze monthly budgets, manage multiple debts and savings goals, assess investment risk tolerance, and receive educational financial recommendations based on their financial information.

**Version 4.0** builds on the persistent financial record management introduced in Version 3.0 and adds **Debt Snowball and Debt Avalanche repayment strategies**, including multi-debt payoff forecasting, optional recurring extra payments, and estimated total interest.

The application uses **SQLite** for persistent financial records. Repayment forecasts run on temporary copies of debt information and **do not change saved balances or record actual payments**.

---

## 🚀 Version 4.0 — Debt Repayment Strategies & Forecasting

Version 4.0 focuses on helping users explore **how different debt repayment priorities can affect their estimated debt-free timeline**.

### Major Improvements

- **Debt Avalanche** prioritization based on the highest annual interest rate among outstanding debts
- **Debt Snowball** prioritization based on the smallest outstanding balance
- Display of recommended debt repayment priorities in the Streamlit Debt Planner
- Ability to enter an **extra monthly payment** for forecasting
- Month-by-month simulation of interest charges and scheduled payments across multiple debts
- Reallocation of recurring payment amounts when simulated debts are paid off
- Application of unused payment amounts toward other outstanding debts within the simulated month
- Estimated **months until debt-free** for the selected strategy
- Estimated **total interest** across the simulated repayment period
- Tracking of individual simulated debt payoff months in the calculation results
- Separation of **hypothetical forecasts** from actual SQLite payment transactions

> **Forecasting note:** The extra payment entered for a forecast is assumed to recur monthly. Forecast results are estimates based on simplified monthly interest and fixed payment assumptions.

---

## ✨ Features

### 📊 Budget Dashboard

The Budget Dashboard helps users understand their monthly income, expenses, cash flow, and savings.

- Tracks monthly income and expenses
- Calculates remaining monthly cash flow
- Calculates savings rate
- Visualizes spending patterns
- Provides minimum savings recommendations
- Stores budget information within financial profiles

---

### 💳 Debt Planner

The Debt Planner allows users to create, manage, and analyze multiple debts associated with their financial profile.

#### Supported Debt Types

- Credit Cards
- Car Loans
- Student Loans
- Personal Loans
- Mortgages
- Other debt types

#### Debt Management Features

- Stores multiple debts for each financial profile
- Records debt balances, annual interest rates, and monthly payments
- Estimates individual debt repayment timelines and interest
- Provides debt management recommendations
- Allows existing debts to be edited or deleted
- Allows actual payments to be recorded against individual debts
- Automatically reduces saved debt balances when actual payments are recorded
- Stores and displays debt payment history
- Provides credit utilization and relevant loan-to-value information

#### 🏔️ Debt Avalanche Strategy

The **Debt Avalanche** method prioritizes the outstanding debt with the **highest annual interest rate**. The Debt Planner displays a suggested priority order and can simulate a long-term repayment plan using that strategy.

The approach generally aims to reduce the total interest paid, subject to the forecast's assumptions.

#### ❄️ Debt Snowball Strategy

The **Debt Snowball** method prioritizes the outstanding debt with the **smallest remaining balance**. The Debt Planner displays a suggested priority order and can simulate a long-term repayment plan using that strategy.

The approach focuses on paying off smaller debts first and progressively redirecting their payment amounts toward remaining debts.

#### 🔮 Multi-Debt Repayment Forecasting

For either strategy, users can enter an optional additional monthly payment and run a forecast. The forecasting engine:

1. Retrieves the debts saved for the selected financial profile.
2. Copies debt balances, annual interest rates, and monthly payments into temporary Python data structures.
3. Calculates monthly interest and applies scheduled payments to active debts.
4. Allocates additional monthly funds and unused payment amounts according to the selected strategy.
5. Transfers the recurring monthly payment allocation of completed debts to other active debts for subsequent months.
6. Repeats the simulation until the debts are paid off or the forecast reaches its safety limit.
7. Returns estimated months to payoff, total interest, and individual debt payoff-month information.

The Streamlit interface currently displays the selected strategy's **estimated months until debt-free** and **estimated total interest**. Individual payoff months are available in the calculation results but are not yet shown in a dedicated timeline visualization.

**Important:** Simulated payments are hypothetical. They do **not** update the `debts` table or create entries in `debt_payment_history`.

---

### 🎯 Savings Goals Planner

The Savings Goals Planner allows users to create and manage multiple financial goals.

- Supports multiple savings goals for each financial profile
- Tracks target and current savings amounts
- Stores target dates and monthly contribution goals
- Calculates required monthly savings
- Calculates projected savings
- Calculates savings-goal progress
- Evaluates whether users are on track to reach their goals
- Allows existing savings goals to be edited
- Allows savings goals to be deleted
- Allows contributions to be recorded against individual savings goals
- Automatically increases current savings after a contribution
- Stores savings contribution history for future analysis

---

### 📈 Investment Profile Assessment

The Investment Profile Assessment evaluates information about the user to determine an investment risk category.

- Determines an investor's risk profile
- Categorizes users as:
  - **Conservative**
  - **Moderate**
  - **Aggressive**
- Provides educational investment allocation suggestions
- Considers factors such as:
  - Investment time horizon
  - Investment experience
  - Reaction to market declines
  - Job stability
  - Income stability
  - Spending risk

---

### 🤖 Financial Advisor

The Financial Advisor combines information collected throughout the application to provide a broader financial assessment.

- Combines financial information from multiple modules
- Aggregates budget, debt, savings, and investment information
- Generates personalized educational financial recommendations
- Performs rule-based financial risk classification
- Calculates a financial health score
- Uses stored financial profile information for financial assessment

---

## 🏗️ System Architecture

Version 4.0 retains the database relationships introduced in Version 3.0 and adds a **read-only forecasting workflow** in the application layer.

```text
financial_profile
│
├── debts
│   └── debt_payment_history
│
└── savings
    └── savings_contributions
```

The `financial_profile` table acts as the parent record for the user's financial information. Each profile can contain multiple debts and savings goals. Debt payment and savings contribution histories remain associated with their respective records.

### Forecasting Workflow

```text
SQLite: saved debts for selected profile
                  │
                  ▼
        Temporary Python debt list
                  │
         ┌────────┴────────┐
         ▼                 ▼
   Debt Avalanche     Debt Snowball
   (highest APR)     (lowest balance)
         │                 │
         └────────┬────────┘
                  ▼
      Monthly repayment simulation
                  │
                  ▼
    Payoff months + total interest
                  │
                  ▼
         Streamlit Debt Planner

     No forecast writes to SQLite
```

---

## 🗄️ Database Design

The application uses **SQLite** for persistent financial data storage.

### Financial Profile

The `financial_profile` table stores general financial, budget, and investment assessment information associated with a financial profile.

### Debts

The `debts` table stores individual debts associated with a financial profile. Each financial profile can contain multiple debts.

```text
financial_profile
        │
        │ One-to-Many
        ▼
      debts
```

### Debt Payment History

The `debt_payment_history` table stores actual payments made toward debts. When an actual payment is recorded, the application:

1. Records the payment in `debt_payment_history`.
2. Reduces the current outstanding debt balance.
3. Commits both database operations together.

```text
debts
  │
  │ One-to-Many
  ▼
debt_payment_history
```

**Forecasted payments are not inserted into this table.**

### Savings

The `savings` table stores individual savings goals associated with a financial profile.

```text
financial_profile
        │
        │ One-to-Many
        ▼
      savings
```

### Savings Contributions

The `savings_contributions` table stores actual contributions made toward savings goals. When a savings contribution is recorded, the application:

1. Records the contribution in `savings_contributions`.
2. Increases the current savings balance.
3. Commits both database operations together.

```text
savings
   │
   │ One-to-Many
   ▼
savings_contributions
```

Foreign-key relationships and cascading deletes help maintain consistency between related financial records.

---

## 🔄 CRUD Functionality

Version 4.0 retains the **Create, Read, Update, and Delete (CRUD)** functionality introduced in Version 3.0.

### Financial Profiles

Users can create and load persistent financial profiles.

### Debts

Users can:

- **Create** debts
- **Read/View** saved debts
- **Update/Edit** existing debts
- **Delete** debts
- Record and review actual debt payments
- Run hypothetical Snowball and Avalanche forecasts without changing saved balances

### Savings Goals

Users can:

- **Create** savings goals
- **Read/View** saved savings goals
- **Update/Edit** existing savings goals
- **Delete** savings goals
- Record savings contributions

---

## 🔐 Transaction Management

The application uses transactions for operations that require multiple related database changes.

For example, recording an **actual debt payment** requires:

```text
INSERT debt payment history
            +
UPDATE outstanding debt balance
            ↓
       COMMIT TRANSACTION
```

Similarly, recording a savings contribution requires:

```text
INSERT savings contribution history
            +
UPDATE current savings balance
            ↓
       COMMIT TRANSACTION
```

These related operations are committed together or rolled back if an error occurs. **Version 4 forecasting is separate from this transaction workflow** and only changes in-memory simulated debt records.

---

## 🧠 Financial Assessment

The application continues to use a **rule-based financial risk assessment and financial health score**.

The financial assessment considers information such as:

- Income
- Expenses
- Savings rate
- Debt balances
- Debt interest rates
- Savings progress
- Emergency fund information
- Investment risk profile

**Machine-learning-based financial risk prediction is planned for a future version.**

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **SQLite**
- **Pandas**
- **NumPy**
- **Matplotlib**

---

## 📁 Project Structure

```text
Personal-Finance-Wealth-Planning-System/
│
├── 🏠_Home.py
│
├── pages/
│   ├── Budget_Dashboard.py
│   ├── Debt_Planner.py
│   ├── Savings_Goals.py
│   ├── Investment_Profile.py
│   └── AI_Advisor.py
│
├── src/
│   ├── calculations.py
│   ├── recommendations.py
│   ├── database.py
│   ├── visualizations.py
│   └── ml_models.py
│
├── data/
│   └── finance_app.db
│
├── images/
│   └── Application screenshots
│
├── requirements.txt
└── README.md
```

The Version 4 debt forecasting calculations are implemented in `src/calculations.py`, while the interactive controls and results are integrated into `pages/Debt_Planner.py`. The database access functions remain in `src/database.py`.

---

## 📸 Screenshots

Screenshots of the application can be found in the `images/` directory, including examples of:

- Budget planning
- Debt management and repayment strategies
- Savings planning
- Investment profile assessment
- Financial advisor functionality

*Update the screenshots directory as needed to reflect the Version 4 interface.*

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd Personal-Finance-Wealth-Planning-System
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Launch the Application

Run the Streamlit application:

```bash
streamlit run 🏠_Home.py
```

The Streamlit application should then open in your web browser.

---

## 🌟 Version 4.0 Highlights

Version 4.0 expands the Debt Planner from **recording and tracking debts** to **exploring possible repayment outcomes**.

```text
Persistent Financial Profiles
            │
            ├── Budget Information
            │
            ├── Debts
            │     ├── CRUD Operations
            │     ├── Actual Payment Tracking
            │     └── Repayment Forecasting
            │           ├── Snowball Strategy
            │           ├── Avalanche Strategy
            │           ├── Extra Monthly Payments
            │           └── Estimated Time & Interest
            │
            ├── Savings Goals
            │     ├── CRUD Operations
            │     └── Contribution Tracking
            │
            ├── Investment Assessment
            │
            └── Financial Advisor
```

The key distinction is that **actual payments change the saved financial records**, while **forecasts model potential future payments without changing those records**.

---

## 🧪 Current Limitations

Version 4.0 introduces an initial repayment forecasting engine. The following limitations remain:

- Forecasts use simplified monthly interest calculations rather than lender-specific accrual rules.
- Forecasts assume fixed interest rates and scheduled payments, apart from simulated payment reallocations.
- Additional monthly payments are treated as recurring assumptions.
- Comprehensive validation of edge cases and numerical accuracy is still planned.
- Snowball and Avalanche results are currently shown through separate strategy actions rather than a dedicated comparison dashboard.
- Individual payoff-month values are calculated but not yet visualized as a full timeline.
- Forecasts have a maximum-month safeguard; some scenarios may not produce a completed payoff forecast.
- Fees, changing minimum payments, promotional interest rates, and other lender-specific conditions are not fully modeled.

---

## 🔮 Future Improvements — Version 5 and Beyond

Planned enhancements include:

- Further testing and correction of repayment simulation edge cases
- Side-by-side **Snowball vs. Avalanche** comparisons
- Estimated interest savings between repayment strategies
- Individual debt payoff timelines and visualizations
- More detailed debt repayment charts and forecasts
- Improved forecasting inputs and validation
- Savings progress and status analysis
- Historical financial snapshots and performance trends
- Improved financial dashboards
- Expanded Financial Advisor capabilities
- Machine-learning-based financial risk prediction and explainability
- Improved profile management and user authentication
- Additional database normalization and validation

---

## ⚠️ Disclaimer

This application is intended for **educational and informational purposes only** and should not be considered professional financial, investment, tax, or legal advice. Repayment forecasts are estimates and may differ from actual lender statements or repayment schedules.
