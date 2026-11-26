# E-commerce Sales Tracker

A Python data-analysis project that reads e-commerce product and monthly sales data,
cleans the dataset, generates sales and price visualizations, and reports the top-selling products.

## Features

- Clean missing and invalid product, category, price and review values
- Track 12-month sales trends for any product
- Compare average price, total sales and review score across product categories
- Analyze the correlation between price and total sales (with a trendline)
- Identify the top N products by total sales

## Dataset

The project uses `ecommerce_sales_analysis.csv`. The script requires these fields:

- `product_id`
- `product_name`
- `category`
- `price`
- `review_score`
- `sales_month_1` through `sales_month_12`

The dataset also contains `review_count`, which is cleaned if present but not required.

## Requirements

- Python 3
- pandas
- matplotlib
- numpy

Install the dependencies:

```bash
python3 -m pip install pandas matplotlib numpy
```

## Run

From the project directory:

```bash
python3 app.py
```

Optional arguments:

```bash
python3 app.py --product-id 42 --top 10 --csv path/to/data.csv
```

| Argument | Default | Description |
| --- | --- | --- |
| `--csv` | `ecommerce_sales_analysis.csv` | Path to the data file |
| `--product-id` | `1` | Product to plot a sales trend for |
| `--top` | `5` | Number of top-selling products to list |

The script:

1. Validates that the required columns exist and cleans the data.
2. Generates a sales trend chart for the chosen product.
3. Prints category statistics (average price, total sales over all 12 months, average review score).
4. Prints the price-versus-sales correlation.
5. Prints the top-selling products.

## Generated Files

- `sales_trend_<product_id>.png` — monthly sales trend for the chosen product
- `category_price_analysis.png` — average price by category, sorted high to low
- `price_vs_sales_correlation.png` — price versus total sales scatter plot with a trendline

## Notes

Price and sales are not related in the provided dataset (correlation is close to 0), and
category average prices are very similar, so the data may be synthetic. Treat any
price-driven conclusions with caution.
