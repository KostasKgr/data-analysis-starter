{{ config(materialized='table') }}

select
    customer_id::varchar as customer_id,
    customer_name::varchar as customer_name,
    segment::varchar as segment,
    signup_date::date as signup_date,
    country::varchar as country
from read_csv_auto('./data/raw/customers.csv', header=true)
