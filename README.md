# 💰 Personal Finance & Wealth Planning System

## 📌 Overview

The **Personal Finance & Wealth Planning System** is a Streamlit-based financial planning application designed to help users organize, track, and evaluate different aspects of their personal finances.

The system allows users to manage financial profiles, analyze monthly budgets, manage multiple debts and savings goals, assess investment risk tolerance, and receive educational financial recommendations based on their financial information.

**Version 3.0** expands the application's financial management capabilities by introducing full CRUD functionality for debts and savings goals, debt payment tracking, savings contribution tracking, automatic balance updates, and improved database transaction handling.

The application uses **SQLite** for persistent storage, allowing financial information to remain available across sessions and enabling financial activities to be associated with individual financial profiles.

---

## 🚀 Version 3.0

Version 3.0 focuses on improving **financial record management and transaction tracking**.

### Major Improvements

- Full CRUD functionality for financial profiles
- Full CRUD functionality for debts
- Full CRUD functionality for savings goals
- Ability to record payments toward individual debts
- Automatic debt balance updates after payments
- Debt payment history storage
- Ability to record contributions toward individual savings goals
- Automatic savings balance updates after contributions
- Savings contribution history storage
- Transaction-safe database operations
- Profile-scoped debt and savings management
- Improved Streamlit session-state handling
- Improved persistent financial data management

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

The Debt Planner allows users to create and manage multiple debts associated with their financial profile.

#### Supported Debt Types

- Credit Cards
- Car Loans
- Student Loans
- Personal Loans
- Mortgages
- Other debt types

#### Features

- Stores multiple debts for each financial profile
- Records debt balances and interest rates
- Estimates debt repayment timelines
- Provides debt management recommendations
- Allows existing debts to be edited
- Allows debts to be deleted
- Allows payments to be recorded against individual debts
- Automatically reduces the outstanding debt balance after a payment
- Stores debt payment history for future analysis

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

Version 3.0 extends the application's architecture to support financial transaction history.

```text
financial_profile
│
├── debts
│   └── debt_payment_history
│
└── savings
    └── savings_contributions
```

The `financial_profile` table acts as the parent record for the user's financial information.

A financial profile can contain multiple debts and multiple savings goals.

Each debt can contain multiple payment records, while each savings goal can contain multiple contribution records.

---

## 🗄️ Database Design

Version 3.0 uses **SQLite** for persistent financial data storage.

### Financial Profile

The `financial_profile` table stores general financial, budget, and investment assessment information associated with a financial profile.

### Debts

The `debts` table stores individual debts associated with a financial profile.

Each financial profile can contain multiple debts.

```text
financial_profile
        │
        │ One-to-Many
        ▼
      debts
```

### Debt Payment History

The `debt_payment_history` table stores individual payments made toward debts.

Each payment is associated with a specific debt.

When a debt payment is recorded, the application:

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

### Savings

The `savings` table stores individual savings goals associated with a financial profile.

Each financial profile can contain multiple savings goals.

```text
financial_profile
        │
        │ One-to-Many
        ▼
     savings
```

### Savings Contributions

The `savings_contributions` table stores individual contributions made toward savings goals.

Each contribution is associated with a specific savings goal.

When a savings contribution is recorded, the application:

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

Foreign-key relationships and cascading deletes are used to help maintain consistency between related financial records.

---

## 🔄 CRUD Functionality

Version 3.0 expands the application's **Create, Read, Update, and Delete (CRUD)** functionality.

### Financial Profiles

Users can create and load persistent financial profiles.

### Debts

Users can:

- **Create** debts
- **Read/View** saved debts
- **Update/Edit** existing debts
- **Delete** debts
- Record debt payments

### Savings Goals

Users can:

- **Create** savings goals
- **Read/View** saved savings goals
- **Update/Edit** existing savings goals
- **Delete** savings goals
- Record savings contributions

---

## 🔐 Transaction Management

Version 3.0 improves database consistency by using transactions for operations that require multiple related database changes.

For example, recording a debt payment requires:

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

These related operations are performed within a single database transaction so that they are **committed together** or **rolled back if an error occurs**.

This helps prevent situations where a payment or contribution is recorded without the corresponding balance being updated.

---

## 🧠 Financial Assessment

Version 3.0 continues to use a **rule-based financial risk assessment and financial health score**.

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

---

## 📸 Screenshots

Screenshots of the application can be found in the `images/` directory.

The screenshots demonstrate different areas of the application, including:

- Budget planning
- Debt management
- Savings planning
- Investment profile assessment
- Financial advisor functionality

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

## 🌟 Version 3.0 Highlights

Version 3.0 represents a transition from primarily performing financial calculations to supporting **persistent financial activity management**.

Users can now modify existing financial records and record financial activities such as debt payments and savings contributions while maintaining updated balances in the database.

### Version 3.0 introduces:

```text
Persistent Financial Profiles
            │
            ├── Budget Information
            │
            ├── Debts
            │     ├── CRUD Operations
            │     └── Payment Tracking
            │
            ├── Savings Goals
            │     ├── CRUD Operations
            │     └── Contribution Tracking
            │
            ├── Investment Assessment
            │
            └── Financial Advisor
```

These improvements provide the foundation for future historical financial analysis, debt repayment strategies, financial trend visualization, and machine-learning-based financial assessment.

---

## 🔮 Future Improvements

Planned enhancements for future versions include:

- Displayable debt payment history
- Displayable savings contribution history
- Debt snowball repayment strategy
- Debt avalanche repayment strategy
- Debt strategy comparisons
- Estimated debt payoff dates
- Savings progress and status analysis
- Historical financial snapshots
- Financial performance trend charts
- Improved financial dashboards
- Expanded AI Advisor capabilities
- Machine-learning-based financial risk prediction
- Explainable machine-learning predictions
- Improved profile management
- User authentication
- Additional database normalization and validation

---

## ⚠️ Disclaimer

This application is intended for **educational and informational purposes only** and should not be considered professional financial, investment, tax, or legal advice.