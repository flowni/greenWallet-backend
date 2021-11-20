all_purchases_query = """
select purchases.id, purchase_time, partner_id, partners.name as partner_name, purchase_prod.amount as total_amount, total_coins
from purchases
left join 
(select purchase_id, sum(amount) as amount, sum(coins_earned) as total_coins from purchase_product
group by purchase_id) AS purchase_prod
on id=purchase_prod.purchase_id
left join 
partners
on partner_id=partners.id
where purchases.user_id={}
"""