# FreshMart-Sales-AnalyticsFreshMart Sales Analytics

FreshMart Sales Analysis is a Python-based data analysis project created to help a supermarket owner understand sales performance across different stores and products.

The project cleans the sales data, checks data quality, analyzes store and product performance, and generates useful business insights.

## Features

* Load sales, product, store, and promotion data
* Clean and validate sales data
* Handle duplicate and missing values
* Convert incorrect data formats
* Calculate revenue and net price
* Analyze product profit margins
* Compare store performance
* Measure promotion impact
* Identify sales patterns
* Check stockout situations
* Generate business recommendations

## Technologies Used

* Python
* Pandas
* NumPy
* Jupyter Notebook
* Git & GitHub

## Project Structure

```text
freshmart-capstone-starter/
│
├── data/
│   ├── sales.csv
│   ├── products.csv
│   ├── stores.csv
│   ├── promotions.csv
│   └── sales_clean.csv
│
├── freshmart/
│   ├── __init__.py
│   ├── loader.py
│   ├── cleaning.py
│   └── reports.py
│
├── freshmart_analysis.ipynb
├── README.md
└── .gitignore
```

## Dataset

The project uses four main datasets:

* **Sales** – contains daily sales transactions
* **Products** – contains product and pricing information
* **Stores** – contains store details
* **Promotions** – contains promotion information

The dataset contains sales information from **5 supermarkets** and includes product, store, pricing, quantity, discount, and promotion details.

## Data Cleaning

Before performing the analysis, the sales data is cleaned by handling:

* Duplicate records
* Incorrect price formats
* Different date formats
* Negative quantities
* Unknown product IDs
* Unknown store IDs
* Missing discount values

A `QualityLog` is also used to record the data-quality issues found and the actions taken to fix them.

## Analysis

The project focuses on several important business questions:

### Store Performance

Compare stores based on their sales and profit performance.

### Product Margins

Identify products with better profit margins and understand which products contribute more to the business.

### Promotion Impact

Compare sales during promotions with previous sales periods to understand whether promotions are actually helping.

### Sales Patterns

Look for useful patterns in sales across products, stores, and time periods.

### Stockouts

Identify products and stores where stock availability may be affecting sales.

## How to Run the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Open the project folder

```bash
cd freshmart-capstone-starter
```

### 3. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

### 4. Install the required packages

```bash
pip install pandas numpy jupyter
```

### 5. Run the notebook

```bash
jupyter notebook
```

Open the FreshMart analysis notebook and run the cells from top to bottom.

## Business Insights

The analysis helps the supermarket owner understand:

* Which stores are performing better
* Which products have higher margins
* Whether promotions are effective
* Where sales patterns are changing
* Where stockouts may be affecting revenue

These insights can be used to make better decisions about pricing, promotions, inventory, and store performance.

## Learning Outcomes

Through this project, I learned:

* Data cleaning using Python
* Working with CSV files
* Handling missing and duplicate data
* Data validation
* Business-oriented data analysis
* Calculating revenue and profit-related metrics
* Working with Python packages
* Creating reports from data
* Using Git and GitHub for project management

## Future Improvements

Some possible improvements are:

* Add an interactive dashboard using Power BI or Streamlit
* Add sales forecasting
* Add more detailed inventory analysis
* Use larger and more recent datasets
* Add automated business reports
* Improve promotion and customer-level analysis
