{{ config(materialized='table') }}

select
    orders.order_id,
    orders.customer_id,
    customers.customer_name,
    customers.segment,
    customers.country,
    customers.signup_date,
    orders.order_date,
    orders.status,
    orders.item_count,
    orders.gross_amount,
    case
        when orders.status = 'completed' then orders.gross_amount
        else 0
    end as completed_revenue,
    date_trunc('month', orders.order_date) as order_month
from {{ ref('stg_orders') }} as orders
join {{ ref('stg_customers') }} as customers
    on orders.customer_id = customers.customer_id
