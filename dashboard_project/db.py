import duckdb as dd
from duckdb import DuckDBPyConnection
import pandas as pd


DB_PATH = "..\\data\\warehouse.duckdb"

def connect_database(db_path: str) -> DuckDBPyConnection:
    connect = dd.connect(db_path, read_only=True)
    return connect

def get_cities(db_path: str):
    """Alle zur Verfügung stehenden Städte."""
    with connect_database(db_path) as con:
        return con.execute("SELECT DISTINCT City FROM tblCustomers ORDER BY City").df()

def get_city_profit(city: str, con: DuckDBPyConnection) -> pd.DataFrame:
    """Anzahl und Umsatz der Bestellungen einer Stadt"""
    query = """
    SELECT 
      s.servicename as servicename,
      count(s.servicename) as counter,
      sum(s.costs) as total_costs
    FROM 
      tblOrders o
    JOIN tblCustomers c ON o.customer_id = c.customer_id
    JOIN tblServices s ON o.service_id = s.service_id
    WHERE c.City = $city
    GROUP BY s.servicename
    ORDER BY total_costs DESC
    """
    result = con.execute(query, {'city': city}).df()
    return result

def get_city_profit_per_year(city: str, con: DuckDBPyConnection) -> pd.DataFrame:
    """Anzahl der Verkäufe pro Jahr"""
    query = """
    SELECT 
    EXTRACT(YEAR FROM purchase_date) AS Year,
    COUNT(*) as Sales
    FROM tblOrders o
    JOIN tblCustomers c ON c.customer_id = o.customer_id
    WHERE c.City = $city
    GROUP BY Year
    """
    return con.execute(query, {"city": city}).df()

def close_database(con: DuckDBPyConnection) -> None:
    con.close()

