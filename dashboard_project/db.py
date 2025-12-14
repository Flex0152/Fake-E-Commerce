import duckdb as dd
from duckdb import DuckDBPyConnection
import pandas as pd
from pathlib import Path
from icecream import ic
from contextlib import contextmanager


DB_PATH = Path("data/warehouse.duckdb")
DATA_PATH = Path("data/example.csv")


class DuckDBManager:
    def __init__(self, db_path: Path, data_path: Path):
        # wenn data Ordner nicht existiert
        if not db_path.parent.is_dir():
            db_path.parent.mkdir(parents=True, exist_ok=True)

        # ohne Daten, keine Analyse möglich
        if not data_path.is_file():
            raise FileNotFoundError(f"Daten nicht gefunden! Pfad: {data_path}")                

        # initialisierung der Attribute
        self.data_path: Path = data_path
        self.db_path: Path = db_path

    @contextmanager
    def connect_database(self):
        conn = dd.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _create_tblServices(self, con: DuckDBPyConnection):
        con.execute(
            """
            CREATE OR REPLACE TABLE tblServices AS
            WITH cte AS (
            SELECT DISTINCT
            Servicename,
            Costs
            FROM staging_data
            ORDER BY Costs)
            SELECT 
            ROW_NUMBER() OVER () AS service_id,
            Servicename, 
            Costs
            FROM CTE
            """)
        
    def _create_tblCustomers(self, con: DuckDBPyConnection):
        con.execute(
            """
            CREATE OR REPLACE TABLE tblCustomers AS
            SELECT DISTINCT
            "Customer ID" as customer_id,
            First_Name,
            Last_Name,
            Gender,
            City,
            "Support Level" as support_level,
            Birthday,
            date_diff('year', Birthday, today()) as Age
            FROM staging_data
            ORDER BY Last_Name
            """)

    def _create_tblOrders(self, con: DuckDBPyConnection):
        con.execute(
            """
            CREATE OR REPLACE TABLE tblOrders AS
            SELECT 
            ROW_NUMBER () OVER () as order_id,
            sd."Purchase date" as purchase_date,
            c.customer_id,
            s.service_id,
            sd.payment_method,
            sd."Sales Canal" as sales_canal,
            sd."Customer Satisfaction" as satisfaction
            FROM 
            staging_data sd
            JOIN tblCustomers c ON sd."Customer ID" = c.customer_id
            JOIN tblServices s ON sd.Servicename = s.Servicename
            """)

    def _create_staging_data(self, con: DuckDBPyConnection, data_path: Path):
        con.execute(
            "CREATE OR REPLACE TABLE staging_data AS " \
            f"SELECT * FROM read_csv_auto($data_path)",
            {"data_path": str(data_path.absolute())})

    def create_table(self) -> None:
        try:
            with self.connect_database() as connect:                
                self._create_staging_data(connect, self.data_path)
                self._create_tblServices(connect)
                self._create_tblCustomers(connect)
                self._create_tblOrders(connect)
                
                ic("Datenbank steht bereit!")
        except Exception as e:
            raise e

    def get_cities(self) -> pd.DataFrame:
        """Alle zur Verfügung stehenden Städte."""
        try:
            with self.connect_database() as connect:
                result = connect.execute("SELECT DISTINCT City FROM tblCustomers ORDER BY City").df()
        except dd.Error as e:
            raise e
        except Exception as e:
            raise e

        return result

    def get_city_profit(self, city: str) -> pd.DataFrame:
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
        try:
            with self.connect_database() as connect:
                result = connect.execute(query, {'city': city}).df()
        except dd.Error as e:
            raise e
        except Exception as e:
            raise e

        return result

    def get_city_profit_per_year(self, city: str) -> pd.DataFrame:
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
        
        try:
            with self.connect_database() as connect:
                result = connect.execute(query, {'city': city}).df()
        except Exception as e:
            raise e

        return result
    
    def total_overview_orders(self):
    # Welcher Service ist der beliebteste?
        query = """
        SELECT 
        count(s.service_id) as in_total,
        s.Servicename
        FROM 
        tblOrders o
        JOIN tblServices s ON o.service_id = s.service_id
        GROUP BY o.service_id, s.Servicename
        ORDER BY in_total desc
        """
        try:
            with self.connect_database() as connect:
                result = connect.execute(query).df()
        except Exception as e:
            raise e
        
        return result
    

if __name__ == "__main__":
    db = DuckDBManager(Path("tmp/tmp.duckdb"), DATA_PATH)
    db.create_table()
    print(db.get_city_profit('Williamville'))
