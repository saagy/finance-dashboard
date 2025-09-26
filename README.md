# 💸 Finance Dashboard

A simple **personal finance dashboard** built with **Streamlit**, **Pandas**, and **Plotly**.
This app allows you to upload your bank transactions in CSV format, categorize your expenses, and visualize them with interactive charts.

---

## 🚀 Features

* 📂 **CSV Upload** – Import your transaction history.
* 🏷 **Custom Categories** – Add, edit, and save expense categories with keywords.
* ✏️ **Interactive Editor** – Re-assign categories directly in the dashboard.
* 📊 **Expense Analytics** – View total spending per category in tables and pie charts.
* 💰 **Payment Overview** – Track credits (payments received) and total income.
* 💾 **Persistent Categories** – Categories and keywords are saved locally in `categories.json`.

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/finance-dashboard.git
cd finance-dashboard
pip install -r requirements.txt
```

---

## ⚙️ Requirements

This project uses the following Python libraries:

* [streamlit](https://streamlit.io/)
* [pandas](https://pandas.pydata.org/)
* [plotly](https://plotly.com/python/)

Install them manually if needed:

```bash
pip install streamlit pandas plotly
```

---

## ▶️ Usage

Run the app with:

```bash
streamlit run app.py
```

Then open the app in your browser (default: `http://localhost:8501`).

---

## 📂 CSV File Format

Your CSV file should contain at least the following columns:

* **Date** – formatted as `DD MMM YYYY` (e.g., `01 Jan 2024`)
* **Details** – description of the transaction
* **Amount** – transaction amount (debits are expenses, credits are income)
* **Debit/Credit** – indicates whether the transaction is `"Debit"` or `"Credit"`

---

## 🛠 How It Works

1. **Upload CSV** – Import your transactions.
2. **Categorize** – Add categories and assign keywords so transactions are auto-classified.
3. **Edit Transactions** – Use the editor to manually fix or re-assign categories.
4. **Visualize** – View a pie chart and table of expenses per category.
5. **Track Income** – Monitor total credits (payments received).

---

## 📑 File Persistence

* Categories and their associated keywords are stored in a local file: **`categories.json`**.
* This ensures your custom categories are saved across app sessions.

---

## 📌 Example

* Upload a transactions file.
* Add a category like `"Groceries"` and assign keywords such as `"Carrefour"`, `"Walmart"`.
* Any matching transactions will automatically be categorized under **Groceries**.

---

## 📜 License

This project is licensed under the MIT License – feel free to use, modify, and distribute.

---
