from datetime import datetime
import time
from random import randint, choice
from faker import Faker
import pandas as pd
from pathlib import Path
from rich import print as rprint
import csv

import asyncio


f = Faker()

def create_random_datetimes() -> datetime:
    """Creates a random datetime"""
    return f.date_time_between()

def create_customer() -> dict:
    """Creates a synthetic Customer"""
    user = {}
    user['customer_id'] = "".join([str(randint(1,9)) for x in range(10)])
    user['first_name'] = f.first_name()
    user['last_name'] = f.last_name()
    user['city'] = f.city()
    return user

def create_services() -> list:
    """Returns a choice of a Service"""
    services = [
        {"service_name": "Databases", "costs_per_month": 9.99}, 
        {"service_name": "E-Commerce", "costs_per_month": 39.99}, 
        {"service_name": "Streaming", "costs_per_month": 19.99}, 
        {"service_name": "Automation", "costs_per_month": 89.99}, 
        {"service_name": "Bi Tooling", "costs_per_month": 8.99}, 
        {"service_name": "Hardware", "costs_per_month": 12.69},
        {"service_name": "Custom Development", "costs_per_month": 199.99}
    ]
    return choice(services)

def create_status() -> str:
    return choice(["Success", "Failure"])
    
async def make_single_entry() -> tuple:
    """Creates Random Data. Because of the keyword
    async, returns a coroutine"""    
    usage_times = create_random_datetimes()
    customers = create_customer()
    services = create_services()
    status = create_status()
    return (
        usage_times,
        customers,
        services,
        status)

async def generate_data_async(number: int) -> list:
    """Generates data asynchronously. Returns a list with coroutines"""
    tasks = [make_single_entry() for _ in range(number)]
    return await asyncio.gather(*tasks)

def convertto_dataframe(data) -> pd.DataFrame:
    """Converts the random Data into a Dataframe"""
    result = []
    for item in data:
        tmp = {}
        tmp['Usage Time'] = item[0]
        tmp['Customer ID'] = item[1]['customer_id']
        tmp['First_Name'] = item[1]['first_name']
        tmp['Last_Name'] = item[1]['last_name']
        tmp['City'] = item[1]['city']
        tmp['Servicename'] = item[2]['service_name']
        tmp['Costs per Month'] = item[2]['costs_per_month']
        tmp['Status last use'] = item[3]
        result.append(tmp)
    return pd.DataFrame(result)

def export_as_csv(data: str, target: Path) -> None:
    header = [
        "Usage Time",
        "Customer ID",
        "First_Name",
        "Last_Name,City",
        "Servicename",
        "Costs per Month",
        "Status last use"]
    with open(target, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        if len(data) == 0:
            rprint("Die Daten entsprechen nicht den Vorgaben!")
            return
        for item in data:
            writer.writerow(
                [
                    item[0],
                    item[1]['customer_id'],
                    item[1]['first_name'],
                    item[1]['last_name'],
                    item[1]['city'],
                    item[2]['service_name'],
                    item[2]['costs_per_month'],
                    item[3]
                ]
            )


if __name__ == "__main__":
    current_path = Path(__file__).parent

    rprint("[bold green]Generate Data...[/bold green]")

    start = time.time()
    # execute the coroutines
    generated_data = asyncio.run(generate_data_async(1)) 
    rprint(generated_data)
    ende = time.time()
    rprint(f"The execution was completed in {(ende - start):.2f} seconds!")
    rprint("[bold green]Done![/bold green]")

    rprint("[bold blue]Saving to csv...[/bold blue]")
    export_as_csv(generated_data, current_path / "data" / "example.csv")
    # df = convertto_dataframe(generated_data)
    # df.to_csv(current_path / "data" / "data.csv", index=False)
    rprint("[bold blue]Done![/bold blue]")