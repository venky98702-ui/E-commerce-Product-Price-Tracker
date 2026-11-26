import argparse

import matplotlib

matplotlib.use("Agg")  # render to files only; works without a display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class EcommercePriceTracker:
    REQUIRED_COLUMNS = ['product_id', 'product_name', 'category', 'price', 'review_score']

    def __init__(self, csv_file):
        """Initialize the tracker with CSV data."""
        self.df = pd.read_csv(csv_file)
        self.months = [f'sales_month_{i}' for i in range(1, 13)]

        missing = [c for c in self.REQUIRED_COLUMNS + self.months if c not in self.df.columns]
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

    def clean_data(self):
        """Clean the dataset by handling missing values and invalid entries."""
        df = self.df.copy()

        # Remove rows with missing critical columns
        df = df.dropna(subset=['product_id', 'product_name', 'category', 'price'])

        # Ensure numeric columns are numeric; invalid prices become NaN and are dropped
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df[df['price'] >= 0]  # NaN comparisons are False, so NaN prices are removed too

        # Review score is optional, but must be numeric and within 0-5 if present
        df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce')
        df.loc[~df['review_score'].between(0, 5), 'review_score'] = np.nan

        if 'review_count' in df.columns:
            df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce').fillna(0)

        # Normalise category labels so "Books " and "books" don't split into two groups
        df['category'] = df['category'].astype(str).str.strip()

        # Ensure sales columns are numeric
        for month in self.months:
            df[month] = pd.to_numeric(df[month], errors='coerce').fillna(0)

        df['total_sales'] = df[self.months].sum(axis=1)
        self.df = df.reset_index(drop=True)

    def track_sales_by_product(self, product_id):
        """Plot the 12-month sales trend for a specific product."""
        product = self.df[self.df['product_id'] == product_id]
        if product.empty:
            return f"Product ID {product_id} not found."

        product_name = product['product_name'].iloc[0]
        price = product['price'].iloc[0]
        sales = product[self.months].iloc[0]

        plt.figure(figsize=(10, 6))
        plt.plot(range(1, 13), sales, marker='o', label=f'Sales (Price: ${price:.2f})')
        plt.title(f'Sales Trend for {product_name} (ID: {product_id})')
        plt.xlabel('Month')
        plt.ylabel('Units Sold')
        plt.xticks(range(1, 13))
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'sales_trend_{product_id}.png')
        plt.close()

        return f"Generated sales trend plot for {product_name} at price ${price:.2f}"

    def category_price_analysis(self):
        """Analyze average price, total sales and review score by category."""
        category_stats = (
            self.df.groupby('category')
            .agg(
                avg_price=('price', 'mean'),
                total_sales=('total_sales', 'sum'),  # all 12 months
                avg_review_score=('review_score', 'mean'),
            )
            .reset_index()
            .sort_values('avg_price', ascending=False)
            .reset_index(drop=True)
        )

        plt.figure(figsize=(12, 6))
        plt.bar(category_stats['category'], category_stats['avg_price'])
        plt.title('Average Price by Category')
        plt.xlabel('Category')
        plt.ylabel('Average Price ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()  # keeps long labels such as "Home & Kitchen" from being clipped
        plt.savefig('category_price_analysis.png')
        plt.close()

        return category_stats

    def price_vs_sales_correlation(self):
        """Analyze correlation between price and total sales."""
        correlation = self.df['price'].corr(self.df['total_sales'])

        plt.figure(figsize=(10, 6))
        plt.scatter(self.df['price'], self.df['total_sales'], alpha=0.5)

        # Linear trendline (needs at least two distinct prices)
        if self.df['price'].nunique() > 1:
            slope, intercept = np.polyfit(self.df['price'], self.df['total_sales'], 1)
            xs = np.linspace(self.df['price'].min(), self.df['price'].max(), 100)
            plt.plot(xs, slope * xs + intercept, color='red', linewidth=2, label='Trendline')
            plt.legend()

        plt.title(f'Price vs Total Sales (Correlation: {correlation:.2f})')
        plt.xlabel('Price ($)')
        plt.ylabel('Total Units Sold')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('price_vs_sales_correlation.png')
        plt.close()

        return f"Price-Sales Correlation: {correlation:.2f}"

    def top_products_by_sales(self, n=5):
        """Identify top N products by total sales."""
        return (
            self.df[['product_id', 'product_name', 'category', 'price', 'total_sales']]
            .sort_values('total_sales', ascending=False)
            .head(n)
        )


def main():
    parser = argparse.ArgumentParser(description="E-commerce sales and price analysis")
    parser.add_argument('--csv', default='ecommerce_sales_analysis.csv', help='path to the CSV file')
    parser.add_argument('--product-id', type=int, default=1, help='product to plot a sales trend for')
    parser.add_argument('--top', type=int, default=5, help='number of top products to list')
    args = parser.parse_args()

    tracker = EcommercePriceTracker(args.csv)
    tracker.clean_data()

    print(f"Tracking Product ID {args.product_id}:")
    print(tracker.track_sales_by_product(args.product_id))

    print("\nCategory Price Analysis:")
    print(tracker.category_price_analysis())

    print("\nPrice vs Sales Correlation:")
    print(tracker.price_vs_sales_correlation())

    print(f"\nTop {args.top} Products by Sales:")
    print(tracker.top_products_by_sales(args.top))


if __name__ == "__main__":
    main()
