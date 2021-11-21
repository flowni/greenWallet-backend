all_purchases_query = """
select purchases.id, purchase_time, partner_id, partners.name as partner_name, 
purchase_prod.amount as total_amount, total_coins, partners.icon_url AS partner_icon_url
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


purchase_details_query_1 = """
select purchase_time, partner_id, partners.name as partner_name,
purchase_prod.amount as total_amount, total_coins
from purchases
left join 
(select purchase_id, sum(amount) as amount, sum(coins_earned) as total_coins from purchase_product
group by purchase_id) AS purchase_prod
on id=purchase_prod.purchase_id
left join 
partners
on partner_id=partners.id
where purchases.id={}
"""
purchase_details_query_2 = """
select product_id, product_name , qty, amount, coins_earned, image 
from purchase_product
left join
products
on product_id = products.id
where purchase_product.purchase_id = {}
"""

product_info_query = """
select * from products
where id = {}
"""

search_user_with_barcode = """
select id,total_coins_earned,balance from users
where barcode = {}"""

insert_purchases_query = """
insert into purchases(user_id, purchase_time,partner_id)
values({},'{}',{})
"""
insert_purchase_product_query = """
insert into purchase_product(purchase_id, product_id, qty, amount, coins_earned)
values({},{},{},{},{})
"""

search_product_with_barcode = """
select id from products
where barcode={}
"""

update_user_coins = """
update users
set total_coins_earned = {}, balance={}
where id={} """