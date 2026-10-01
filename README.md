# FreshMart-Sales-AnalyticsFreshMart Sales Analytics

A simple Python project that looks at FreshMart’s sales data and finds useful insights about products, promotions, stores, and stock-outs.

📌 About the Project

This project helps understand:

Which products make more profit
Which promotions work well
Which stores use their space effectively
Where stock-outs may be causing lost sales
How sales change across days and months
🛠️ Tools Used
Python
Pandas
NumPy
Matplotlib
Seaborn
Jupyter Notebook
VS Code
📊 What I Did
Product Profit

I compared products based on profit margin, not just sales.

Promotions

I checked whether promotions actually increased sales using sales lift and p-values.

Stock-outs

I found products that had 6 or more days with no sales and estimated the possible revenue lost.

Store Performance

I compared stores based on profit per square foot.

Sales Patterns

I looked at sales by category, weekday, and month to find useful patterns.

💡 Main Findings
Some products bring much more profit than others.
Some promotions clearly improve sales.
Some products are out of stock for several days.
Store performance changes when we consider the size of the store.
Keeping profitable products in stock can help reduce lost sales.
▶️ How to Run

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the required libraries:

pip install pandas numpy matplotlib seaborn

Run a report:

python -m freshmart report --store 4

To check a particular month:

python -m freshmart report --store 2 --month 6
📁 Project Structure
FreshMart-Sales-Analytics/
│
├── data/
├── freshmart/
│   ├── __init__.py
│   ├── __main__.py
│   ├── loader.py
│   ├── cleaner.py
│   └── report.py
│
├── notebooks/
├── README.md
└── .gitignore
🔮 Recommendation

FreshMart should keep high-profit products in stock, focus on promotions that increase sales, and use store space wisely. More customer data could help understand which products customers usually buy together.
