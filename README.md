
# Uses duckdb

## Installation

```sh
wget https://install.duckdb.org/v1.5.2/duckdb_cli-linux-amd64.zip
unzip duckdb_cli-linux-amd64.zip
mv duckdb ~/.local/bin
rm duckdb_cli-linux-amd64.zip
```

# Uses dbt

```sh
# Python 3.14 was not compatible currently
uv venv --python 3.12
uv add dbt-duckdb
uv run dbt init .

uv run dbt debug --project-dir ./jira --profiles-dir ./jira
task dbt:run
task dbt:test
```

## Local dashboard

```sh
task dbt:run
task dashboard
```

The dashboard makes a temporary copy of `./data/dev.duckdb` to display data.
