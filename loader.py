"""Load and validate the four FreshMart files."""
from pathlib import Path
import pandas as pd

REQUIRED = {
    "sales_2025.csv": ["receipt_id", "store_id", "product_id", "sale_date", "qty", "unit_price", "discount_pct"],
    "products.csv": ["product_id", "product_name", "category", "unit_price", "cost_price", "is_perishable"],
    "stores.csv": ["store_id", "store_name", "city", "opened_on", "floor_area_sqft"],
    "promotions.csv": ["promo_id", "product_id", "store_id", "start_date", "end_date", "discount_pct"],
}

class DataFileError(Exception):
    """A required file is missing or unreadable."""

class SchemaError(Exception):
    """A file is missing required columns."""

class SalesLoader:
    """Reads the four CSVs from a folder and validates their columns."""
    def __init__(self, folder):
        self.folder = Path(folder)
        
        # TODO completed
        if not self.folder.exists():
            raise DataFileError(f"Folder not found: {self.folder}")

    def _read(self, name):
        # TODO completed
        file_path = self.folder / name
        
        if not file_path.exists():
            raise DataFileError(f"File not found: {file_path}")
        
        df = pd.read_csv(file_path)
        
        # TODO completed
        missing_columns = [
            column for column in REQUIRED[name]
            if column not in df.columns
        ]
        
        if missing_columns:
            raise SchemaError(
                f"Missing columns in {name}: {missing_columns}"
            )
        
        return df

    def load_all(self):
        return {name.split(".")[0].replace("_2025", ""): self._read(name) for name in REQUIRED}

    def stream_sales(self, chunksize=5000):
        """Generator: yield the sales file chunk by chunk (pd.read_csv(..., chunksize=))."""
        # TODO completed
        sales_file = self.folder / "sales_2025.csv"
        
        if not sales_file.exists():
            raise DataFileError(f"File not found: {sales_file}")
        
        yield from pd.read_csv(sales_file, chunksize=chunksize)
