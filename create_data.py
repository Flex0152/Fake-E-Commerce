from datetime import datetime, date
import time
from random import randint, choice, shuffle
from faker import Faker
from pathlib import Path
from rich import print as rprint
import csv

import asyncio


f = Faker()

def create_random_datetimes(start_date: date) -> datetime:
    """Creates a random datetime"""
    return f.date_time_between(start_date)

def create_customer() -> dict:
    """Creates a synthetic Customer"""
    user = {}
    user['customer_id'] = "".join([str(randint(1,9)) for x in range(10)])
    user['first_name'] = f.first_name()
    user['last_name'] = f.last_name()
    user['Gender'] = choice(["F", "M"])
    user['Birthday'] = f.date_between(date(1900, 1, 1), date(2000, 12, 31))
    user['city'] = f.city()
    user['support_level'] = choice(['Standard', 'Premium'])
    return user

def create_services() -> list:
    """Returns a choice of a Service"""
    services = [
        {"service_name": "Databases", "costs": 9.99}, 
        {"service_name": "E-Commerce", "costs": 39.99}, 
        {"service_name": "Streaming", "costs": 19.99}, 
        {"service_name": "Automation", "costs": 89.99}, 
        {"service_name": "Bi Tooling", "costs": 8.99}, 
        {"service_name": "Hardware", "costs": 12.69},
        {"service_name": "Custom Development", "costs": 199.99}
    ]
    return choice(services)

def create_customer_satisfaction() -> str:
    return randint(1,5)
    # return choice(["Success", "Failure"])

def create_payment_method() -> str:
    return choice(['Kreditkarte', 'SEPA', 'PayPal'])

def create_sales_canal() -> str:
    return choice(['online', 'by telephone', 'on site'])
    
async def make_single_entry(customer: dict) -> tuple:
    """Creates Random Data. Because of the keyword
    async, returns a coroutine"""    
    purchase_date = create_random_datetimes(date(2010, 1, 1))
    services = create_services()
    payment_method = create_payment_method()
    sales_canal = create_sales_canal()
    satisfaction = create_customer_satisfaction()
    
    return (
        purchase_date,
        customer,
        services,
        payment_method,
        sales_canal,
        satisfaction)

async def generate_data_async(max_services: int, max_customers: int) -> list:
    """Generates data asynchronously. Returns a list with coroutines"""
    customers = [create_customer() for _ in range(max_customers)]
    tasks = [
        make_single_entry(customer)
        for customer in customers
        for _ in range(max_services)
    ]
    # shuffle makes data even more realistic
    shuffle(tasks)
    return await asyncio.gather(*tasks)

def export_as_csv(data: list, target: Path) -> None:
    header = [
        "Purchase date",
        "Customer ID",
        "First_Name",
        "Last_Name",
        "Gender",
        "Birthday",
        "Support Level",
        "City",
        "Servicename",
        "Costs",
        "payment_method",
        "Sales Canal",
        "Customer Satisfaction"]
    
    if len(data) == 0:
        rprint("Keine Daten!")
        return
    
    with open(target, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)    
        for i, item in enumerate(data):
            try:
                writer.writerow(
                    [
                        item[0],
                        item[1]['customer_id'],
                        item[1]['first_name'],
                        item[1]['last_name'],
                        item[1]['Gender'],
                        item[1]['Birthday'],
                        item[1]['support_level'],
                        item[1]['city'],
                        item[2]['service_name'],
                        item[2]['costs'],
                        item[3],
                        item[4],
                        item[5]
                    ]
                )
            except (KeyError, IndexError, TypeError) as e:
                rprint(f"[yellow]Datensatz {i} fehlerhaft: {e}[/yellow]")


if __name__ == "__main__":
    current_path = Path(__file__).parent

    rprint("[bold green]Generate Data...[/bold green]")

    start = time.time()
    # execute the coroutines
    # creates max_customers * max_services entrys
    generated_data = asyncio.run(generate_data_async(max_customers=100, max_services=1000)) 

    rprint("[bold blue]Saving to csv...[/bold blue]")
    export_as_csv(generated_data, current_path / "data" / "example.csv")
    rprint("[bold blue]Done![/bold blue]")

    ende = time.time()
    rprint(f"The execution was completed in {(ende - start):.2f} seconds!")
    rprint("[bold green]Done![/bold green]")