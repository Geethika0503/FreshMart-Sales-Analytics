"""CLI:  python -m freshmart report --store 3 --month 6"""
import argparse
from .loader import SalesLoader
from .cleaner import clean_sales, clean_products, QualityLog
from .report import top_margin, store_productivity, stockouts


def main():
    ap = argparse.ArgumentParser(prog="freshmart")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("report")
    r.add_argument("--data", default="data")
    r.add_argument("--store", type=int)
    r.add_argument("--month", type=int)

    args = ap.parse_args()

    loader = SalesLoader(args.data)
    d = loader.load_all()

    log = QualityLog()

    products = clean_products(d["products"], log)

    sales = clean_sales(
        d["sales"],
        products,
        d["stores"],
        log
    )

    if args.month is not None:
        sales = sales[sales["sale_date"].dt.month == args.month]

    print("\nTop Margin Products:")
    print(top_margin(sales, products, store_id=args.store))

    print("\nStore Productivity:")
    print(store_productivity(sales, products, d["stores"]))

    print("\nStock-outs:")
    print(stockouts(sales))


if __name__ == "__main__":
    main()