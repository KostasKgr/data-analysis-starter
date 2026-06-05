from __future__ import annotations

from pathlib import Path
from typing import cast

import altair as alt
import duckdb
import pandas as pd
import streamlit as st


DB_PATH = Path("./data/dashboard.duckdb")
ORDER_DASHBOARD_VIEW = "order_dashboard"
CUSTOMER_SUMMARY_VIEW = "customer_order_summary"


@st.cache_data(show_spinner=False)
def load_orders(db_path: str) -> pd.DataFrame:
    with duckdb.connect(db_path, read_only=True) as connection:
        dataframe = connection.execute(
            f"""
            select
                order_id,
                customer_id,
                customer_name,
                segment,
                country,
                signup_date,
                order_date,
                status,
                item_count,
                gross_amount,
                completed_revenue,
                order_month
            from {ORDER_DASHBOARD_VIEW}
            order by order_date, order_id
            """
        ).fetch_df()

    dataframe["signup_date"] = cast(pd.Series, pd.to_datetime(dataframe["signup_date"]))
    dataframe["order_date"] = cast(pd.Series, pd.to_datetime(dataframe["order_date"]))
    dataframe["order_month"] = cast(pd.Series, pd.to_datetime(dataframe["order_month"]))
    return dataframe


@st.cache_data(show_spinner=False)
def load_customer_summary(db_path: str) -> pd.DataFrame:
    with duckdb.connect(db_path, read_only=True) as connection:
        dataframe = connection.execute(
            f"""
            select
                customer_id,
                customer_name,
                segment,
                country,
                signup_date,
                order_count,
                completed_order_count,
                completed_revenue,
                completed_item_count,
                latest_order_date
            from {CUSTOMER_SUMMARY_VIEW}
            order by completed_revenue desc, customer_name
            """
        ).fetch_df()

    dataframe["signup_date"] = cast(pd.Series, pd.to_datetime(dataframe["signup_date"]))
    dataframe["latest_order_date"] = cast(pd.Series, pd.to_datetime(dataframe["latest_order_date"]))
    return dataframe


def select_filter_options(dataframe: pd.DataFrame, column_name: str) -> list[str]:
    values = dataframe[column_name].dropna().astype(str).unique().tolist()
    return sorted(values)


def build_revenue_by_segment_chart(dataframe: pd.DataFrame) -> alt.Chart:
    chart_data = (
        dataframe.groupby("segment", as_index=False)
        .agg(completed_revenue=("completed_revenue", "sum"))
        .sort_values("completed_revenue", ascending=False)
    )
    return (
        alt.Chart(chart_data)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("segment:N", title="Segment", sort="-y"),
            y=alt.Y("completed_revenue:Q", title="Completed revenue"),
            color=alt.Color("segment:N", legend=None),
            tooltip=[
                alt.Tooltip("segment:N", title="Segment"),
                alt.Tooltip("completed_revenue:Q", title="Completed revenue", format="$,.2f"),
            ],
        )
    )


def build_status_chart(dataframe: pd.DataFrame) -> alt.Chart:
    chart_data = (
        dataframe.groupby("status", as_index=False)
        .agg(order_count=("order_id", "nunique"), gross_amount=("gross_amount", "sum"))
        .sort_values("order_count", ascending=False)
    )
    return (
        alt.Chart(chart_data)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("status:N", title="Status", sort="-y"),
            y=alt.Y("order_count:Q", title="Orders"),
            color=alt.Color("status:N", legend=None),
            tooltip=[
                alt.Tooltip("status:N", title="Status"),
                alt.Tooltip("order_count:Q", title="Orders"),
                alt.Tooltip("gross_amount:Q", title="Gross amount", format="$,.2f"),
            ],
        )
    )


def build_monthly_revenue_chart(dataframe: pd.DataFrame) -> alt.Chart:
    chart_data = dataframe.groupby("order_month", as_index=False).agg(
        completed_revenue=("completed_revenue", "sum")
    )
    return (
        alt.Chart(chart_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("order_month:T", title="Month"),
            y=alt.Y("completed_revenue:Q", title="Completed revenue"),
            tooltip=[
                alt.Tooltip("order_month:T", title="Month"),
                alt.Tooltip("completed_revenue:Q", title="Completed revenue", format="$,.2f"),
            ],
        )
    )


def render_metrics(orders: pd.DataFrame, customers: pd.DataFrame) -> None:
    completed_revenue = cast(float, orders["completed_revenue"].sum())
    order_count = int(orders["order_id"].nunique())
    customer_count = int(customers["customer_id"].nunique())
    completed_order_count = int((orders["status"] == "completed").sum())
    average_order_value = completed_revenue / max(completed_order_count, 1)

    metric_columns = st.columns(4)
    metric_columns[0].metric("Completed revenue", f"${completed_revenue:,.2f}")
    metric_columns[1].metric("Orders", f"{order_count:,}")
    metric_columns[2].metric("Customers", f"{customer_count:,}")
    metric_columns[3].metric("Avg completed order", f"${average_order_value:,.2f}")


def main() -> None:
    st.set_page_config(page_title="Data Analysis Starter", layout="wide")
    st.title("Data Analysis Starter")

    if not DB_PATH.exists():
        st.error("DuckDB database not found. Run `task dbt:run` before starting the dashboard.")
        st.stop()

    orders = load_orders(str(DB_PATH))
    customer_summary = load_customer_summary(str(DB_PATH))

    segments = st.sidebar.multiselect(
        "Segment",
        options=select_filter_options(orders, "segment"),
    )
    statuses = st.sidebar.multiselect(
        "Status",
        options=select_filter_options(orders, "status"),
    )

    filtered_orders = orders.copy()
    if segments:
        filtered_orders = filtered_orders[filtered_orders["segment"].isin(segments)]
    if statuses:
        filtered_orders = filtered_orders[filtered_orders["status"].isin(statuses)]

    filtered_customers = customer_summary[
        customer_summary["customer_id"].isin(filtered_orders["customer_id"].unique())
    ]

    render_metrics(filtered_orders, filtered_customers)

    chart_columns = st.columns(2)
    with chart_columns[0]:
        st.subheader("Completed Revenue By Segment")
        st.altair_chart(build_revenue_by_segment_chart(filtered_orders), width="stretch")
    with chart_columns[1]:
        st.subheader("Orders By Status")
        st.altair_chart(build_status_chart(filtered_orders), width="stretch")

    st.subheader("Monthly Completed Revenue")
    st.altair_chart(build_monthly_revenue_chart(filtered_orders), width="stretch")

    st.subheader("Recent Orders")
    st.dataframe(
        filtered_orders.sort_values(["order_date", "order_id"], ascending=[False, False]),
        width="stretch",
        hide_index=True,
    )

    st.subheader("Customer Summary")
    st.dataframe(
        filtered_customers.sort_values("completed_revenue", ascending=False),
        width="stretch",
        hide_index=True,
    )


if __name__ == "__main__":
    main()
