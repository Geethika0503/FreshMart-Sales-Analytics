"""Every cleaning rule as a function; QualityLog records what each one did."""
import pandas as pd

class QualityLog:
    def __init__(self): self.rows = []
    def add(self, problem, affected, fix, why): self.rows.append({"problem": problem, "rows_affected": int(affected), "fix": fix, "why": why})
    def to_frame(self): return pd.DataFrame(self.rows)

def clean_products(products, log):
    p = products.copy()
    # TODO: product_name whitespace; cost_price > unit_price -> flag column margin_ok. Log each rule.
    whitespace_count = p["product_name"].astype(str).str.strip().ne(p["product_name"].astype(str)).sum()
    p["product_name"] = p["product_name"].astype(str).str.strip()
    log.add("product_name whitespace", whitespace_count, "Trim whitespace", "Keep product names consistent")

    p["margin_ok"] = p["cost_price"] <= p["unit_price"]
    margin_count = (~p["margin_ok"]).sum()
    log.add("cost_price > unit_price", margin_count, "Flag margin_ok=False", "Identify products with invalid margins")
    return p

def clean_sales(sales, products, stores, log):
    df = sales.copy()
    # TODO, in this order, logging each: duplicates -> unit_price text to number -> dates (two formats!)
    #       -> negative qty -> unknown product_id -> unknown store_id -> missing discount_pct
    # Then derive: net_price = unit_price * (1 - discount_pct/100); revenue = net_price * qty

    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()
    log.add("Duplicate sales", duplicates, "Remove duplicate rows", "Avoid counting the same sale twice")

    old_price = df["unit_price"].copy()
    df["unit_price"] = pd.to_numeric(
        df["unit_price"].astype(str).str.replace(r"[$,]", "", regex=True),
        errors="coerce"
    )
    price_count = old_price.astype(str).ne(df["unit_price"].astype(str)).sum()
    log.add("unit_price text", price_count, "Convert to numeric", "Allow price calculations")

    old_dates = df["sale_date"].copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"], format="mixed", errors="coerce")
    date_count = df["sale_date"].isna().sum()
    log.add("Invalid sale dates", date_count, "Convert to datetime", "Allow date-based analysis")

    negative_qty = (df["qty"] < 0).sum()
    df.loc[df["qty"] < 0, "qty"] = 0
    log.add("Negative quantity", negative_qty, "Replace with 0", "Quantity cannot be negative")

    unknown_products = (~df["product_id"].isin(products["product_id"])).sum()
    df = df[df["product_id"].isin(products["product_id"])]
    log.add("Unknown product_id", unknown_products, "Remove unknown products", "Keep only valid products")

    unknown_stores = (~df["store_id"].isin(stores["store_id"])).sum()
    df = df[df["store_id"].isin(stores["store_id"])]
    log.add("Unknown store_id", unknown_stores, "Remove unknown stores", "Keep only valid stores")

    missing_discount = df["discount_pct"].isna().sum()
    df["discount_pct"] = df["discount_pct"].fillna(0)
    log.add("Missing discount_pct", missing_discount, "Fill with 0", "No discount means full price")

    df["net_price"] = df["unit_price"] * (1 - df["discount_pct"] / 100)
    df["revenue"] = df["net_price"] * df["qty"]

    return df.reset_index(drop=True)