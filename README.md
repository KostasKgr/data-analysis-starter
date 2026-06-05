# Data Analysis Starter

This project is a small local analytics starter using dbt, DuckDB, and Streamlit.
dbt reads sample customer and order files from `data/raw/`, builds analysis
tables in DuckDB, and Streamlit displays the resulting dashboard.

## What's included

- Sample raw data in `data/raw/`: a customer CSV and an order JSON file.
- dbt models in `dbt/models/`:
  - `staging`: cleaned, typed models that stay close to the raw files.
  - `marts`: dashboard-ready analysis tables.
- A local DuckDB database at `data/dev.duckdb`, created by dbt.
- A Streamlit dashboard in `dashboard.py` that reads the mart tables.

## Setup

Install Python dependencies with `uv`:

```sh
uv sync
```

This project uses Task for common commands. The DuckDB Python package is
installed by `uv`; the DuckDB CLI is optional but useful for inspecting the
database directly.

## DuckDB CLI

```sh
wget https://install.duckdb.org/v1.5.2/duckdb_cli-linux-amd64.zip
unzip duckdb_cli-linux-amd64.zip
mv duckdb ~/.local/bin
rm duckdb_cli-linux-amd64.zip
```

## Build and test dbt

```sh
task dbt:run
task dbt:test
```

Use the combined verification task when rebuilding and testing together:

```sh
task dbt:verify
```

## Run the dashboard

```sh
task dbt:run
task dashboard
```

`task dashboard` makes a temporary copy of `./data/dev.duckdb` before starting
Streamlit. This avoids holding a read lock on the development database while you
continue iterating with dbt.

## Adapting this starter

1. Replace or add raw files in `data/raw/`.
2. Update the staging models in `dbt/models/staging/` to read, cast, rename, and
   lightly clean your raw data.
3. Add dbt tests in the staging and mart `schema.yml` files for identifiers,
   required fields, accepted values, and relationships.
4. Build reusable analysis outputs in `dbt/models/marts/`. These should be the
   tables your dashboard, notebooks, or ad hoc analysis can query directly.
5. Point `dashboard.py` at the mart tables that support your analysis.

Keep staging models source-shaped and predictable. Put joins, aggregations, and
dashboard-ready calculations in marts.
