import csv
import random
from datetime import datetime, timedelta


variants = ["V2001", "V2002", "V2003", "V2004", "V2005", "V2006", "V2007", "V2008", "V2009", "V2010",
            "V2011", "V2012", "V2013", "V2014", "V2015", "V2016", "V2017", "V2018", "V2019", "V2020"]
customers = [1,2,3,4,5,6,7,8,9,10]


def random_date(start_date, end_date):
    days_diff = (end_date - start_date).days
    random_days = random.randint(0, days_diff)
    return start_date + timedelta(days=random_days)


start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)

with open('ecommerce_orders.csv', 'w', newline='') as csvfile:
    fieldnames = ["order_id", "variant_id", "cust_id", "status_id", "quantity", "date",
                  "order_status", "price", "discount"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for order_id in range(1, 301):
        variant_id = random.choice(variants)
        cust_id = random.choice(customers)
        status_id = random.randint(1, 3) if order_id > 15 and order_id <30 else 1
        quantity = random.randint(1, 5)
        date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        order_status = "Pending" if status_id == 1 and order_id < 15 else "Completed"
        price = random.uniform(10, 100)
        discount = random.uniform(0, 0.3)

        writer.writerow({
            "order_id": order_id,
            "variant_id": variant_id,
            "cust_id": cust_id,
            "status_id": status_id,
            "quantity": quantity,
            "date": date,
            "order_status": order_status,
            "price": price,
            "discount": discount
        })

print("Done")
