import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    return (mo,)


@app.cell
def _(mo):
    atlas = mo.sql(
        f"""
        INSTALL psql from community;
        LOAD psql; 

        SELECT 
            year, 
            SUM(export_value) AS total_export_value,
            SUM(import_value) AS total_import_value
        FROM "datos/atlas/hs92_country_country_product_year_6_*.csv"
        WHERE country_iso3_code = 'MEX' AND partner_iso3_code = 'CHN'
        GROUP BY year;
        """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
