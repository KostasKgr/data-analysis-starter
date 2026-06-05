To run dbt use 

```sh
task dbt:run
```

# Python environment

This project uses `uv` for Python dependencies and commands.
Always run Python commands through `uv run`, not the system `python3`.

# Misc

`duckdb` cli is installed and available.


# Work verifications

If dbt related files changed then run the tests

```sh
task dbt:test
```

If you need to both rebuild and test, prefer the sequential combined task to avoid DuckDB lock conflicts:

```sh
task dbt:verify
```


If you change python code or dependencies run python tests

```sh
uv run python -m py_compile dashboard.py
uv run basedpyright dashboard.py
```
