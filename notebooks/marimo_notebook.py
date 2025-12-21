import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    import marimo as mo
    return (duckdb,)


@app.cell
def _(duckdb):
    db = duckdb.connect()
    return (db,)


@app.cell
def _(db):
    db.sql("SELECT * FROM read_csv_auto('data/example.csv') LIMIT 10")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
