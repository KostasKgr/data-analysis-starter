# Data Analysis Starter

This project is a small local analytics starter using dbt, DuckDB, and Streamlit.
dbt reads a sample customer CSV and order JSON file from `data/raw/`, builds a
few models in DuckDB, and the dashboard displays the resulting reporting views.

## DuckDB CLI

```sh
wget https://install.duckdb.org/v1.5.2/duckdb_cli-linux-amd64.zip
unzip duckdb_cli-linux-amd64.zip
mv duckdb ~/.local/bin
rm duckdb_cli-linux-amd64.zip
```

## dbt

```sh
task dbt:run
task dbt:test
```

Use the combined verification task when rebuilding and testing together:

```sh
task dbt:verify
```

## Local dashboard

```sh
task dbt:run
task dashboard
```

The dashboard makes a temporary copy of `./data/dev.duckdb` to display data.
