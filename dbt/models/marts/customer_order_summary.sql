{{ config(materialized='table') }}

select
    customers.customer_id,
    customers.customer_name,
    customers.segment,
    customers.country,
    customers.signup_date,
    count(orders.order_id) as order_count,
    count(*) filter (where orders.status = 'completed') as completed_order_count,
    coalesce(sum(orders.gross_amount) filter (where orders.status = 'completed'), 0) as completed_revenue,
    coalesce(sum(orders.item_count) filter (where orders.status = 'completed'), 0) as completed_item_count,
    max(orders.order_date) as latest_order_date
from {{ ref('stg_customers') }} as customers
left join {{ ref('stg_orders') }} as orders
    on customers.customer_id = orders.customer_id
group by
    customers.customer_id,
    customers.customer_name,
    customers.segment,
    customers.country,
    customers.signup_date
