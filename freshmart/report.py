"""Analysis functions. Each returns a DataFrame; each is timed."""
import time, functools
import numpy as np, pandas as pd

def timed(fn):
    """TODO: decorator that prints how long fn took. Use functools.wraps."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f"{fn.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timed
def top_margin(sales, products, store_id=None, n=10):
    """Top n products by (net_price - cost_price) * qty. Exclude rows where margin_ok is False."""
    df = sales.copy()
    if store_id is not None:
        df = df[df["store_id"] == store_id]

    df = df.merge(
        products[["product_id", "product_name", "cost_price", "margin_ok"]],
        on="product_id",
        how="left"
    )

    df = df[df["margin_ok"] == True]
    df["margin"] = (df["net_price"] - df["cost_price"]) * df["qty"]
    result = (
        df.groupby(["product_id", "product_name"], as_index=False)["margin"]
        .sum()
        .sort_values("margin", ascending=False)
        .head(n)
    )
    return result

@timed
def promo_lift(sales, promotions, rng=None, n_perm=1000):
    """For each promotion: qty/day in the promo window vs same weekdays in the 8 weeks before; permutation p-value."""

    if rng is None:
        rng = np.random.default_rng(42)

    df = sales.copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    results = []

    for _, promo in promotions.iterrows():
        promo_id = promo["promo_id"]
        product_id = promo["product_id"]
        store_id = promo["store_id"]

        start = pd.to_datetime(promo["start_date"])
        end = pd.to_datetime(promo["end_date"])

        promo_days = pd.date_range(start, end)

        before_start = start - pd.Timedelta(weeks=8)
        before_end = start - pd.Timedelta(days=1)

        promo_data = df[(df["product_id"] == product_id) & (df["store_id"] == store_id) & (df["sale_date"].isin(promo_days))]

        before_data = df[(df["product_id"] == product_id) & (df["store_id"] == store_id) &(df["sale_date"] >= before_start) & (df["sale_date"] <= before_end) &(df["sale_date"].dt.dayofweek.isin(promo_days.dayofweek))]

        promo_daily = promo_data.groupby("sale_date")["qty"].sum()
        before_daily = before_data.groupby("sale_date")["qty"].sum()

        promo_mean = promo_daily.mean() if len(promo_daily) else 0
        before_mean = before_daily.mean() if len(before_daily) else 0

        lift = promo_mean - before_mean
        combined = np.concatenate([ promo_daily.values,before_daily.values])

        if len(combined) > 1:
            count = 0
            for _ in range(n_perm):
                shuffled = rng.permutation(combined)
                a = shuffled[:len(promo_daily)]
                b = shuffled[len(promo_daily):]
                if abs(a.mean() - b.mean()) >= abs(lift):
                    count += 1
            p_value = (count + 1) / (n_perm + 1)
        else:
            p_value = 1.0
        results.append({"promo_id": promo_id, "lift": lift, "p_value": p_value})
    return pd.DataFrame(results)

@timed
def patterns(sales, products):
    """Return two pivot tables: category x weekday units, category x month units."""
    df = sales.merge(products[["product_id", "category"]],on="product_id")
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["weekday"] = df["sale_date"].dt.day_name()
    df["month"] = df["sale_date"].dt.month_name()

    wd = pd.pivot_table(df, values="qty", index="category", columns="weekday", aggfunc="sum", fill_value=0)
    mo = pd.pivot_table( df, values="qty", index="category", columns="month", aggfunc="sum", fill_value=0)
    
    return wd, mo

@timed
def stockouts(sales, min_rate=1.5, min_run=6):
    """Product-store pairs with >= min_rate receipts/day on average and a run of >= min_run zero-sale days."""
    df = sales.copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    results = []
    for (product_id, store_id), group in df.groupby(["product_id", "store_id"]):
        daily = group.groupby("sale_date").agg(
            qty=("qty", "sum"),
            revenue=("revenue", "sum")
        )

        dates = pd.date_range(daily.index.min(), daily.index.max())
        daily = daily.reindex(dates, fill_value=0)
        rate = daily["qty"].mean()
        if rate < min_rate:
            continue

        avg_daily_revenue = daily["revenue"].mean()
        current_run = 0
        max_zero_run = 0

        for qty in daily["qty"]:
            if qty == 0:
                current_run += 1
                max_zero_run = max(max_zero_run, current_run)
            else:
                current_run = 0
        if max_zero_run >= min_run:
            results.append({"product_id": product_id, "store_id": store_id, "rate": rate, "max_zero_run": max_zero_run, "avg_daily_revenue": avg_daily_revenue})
    return pd.DataFrame(results)

@timed
def store_productivity(sales, products, stores):
    """Revenue, margin, receipts and margin per sq ft per store."""
    df = sales.merge(products[["product_id", "cost_price"]], on="product_id", how="left")
    df["margin"] = ((df["net_price"] - df["cost_price"]) * df["qty"])
    result = df.groupby("store_id").agg(
        revenue=("revenue", "sum"),
        margin=("margin", "sum"),
        receipts=("receipt_id", "nunique")
    ).reset_index()
    result = result.merge(
        stores[["store_id", "store_name", "floor_area_sqft"]],
        on="store_id",
        how="left"
    )
    result["margin_per_sq_ft"] = (
        result["margin"] / result["floor_area_sqft"]
    )
    return result
