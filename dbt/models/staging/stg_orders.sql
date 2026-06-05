{{ config(materialized='table') }}

select
    order_id::varchar as order_id,
    customer_id::varchar as customer_id,
    order_date::date as order_date,
    status::varchar as status,
    item_count::integer as item_count,
    gross_amount::decimal(12, 2) as gross_amount
from read_json_auto('./data/raw/orders.json')
