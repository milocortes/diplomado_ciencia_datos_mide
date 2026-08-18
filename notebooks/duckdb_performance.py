import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    return mo, pl


@app.cell
def _(mo):
    atlas = mo.sql(
        f"""
        install psql from community; 
        load psql ; 

        SELECT 
            year, 
            SUM(export_value) AS total_export_value,
            SUM(import_value) AS total_import_value    
        FROM "datos/atlas/hs92_country_country_product_year_6_*.csv"        
        WHERE country_iso3_code = 'MEX' AND partner_iso3_code = 'USA'
        GROUP BY year;
        """
    )
    return (atlas,)


@app.cell
def _(atlas, pl):
    import altair as alt 

    atlas_melt = atlas.unpivot(
        index=["year"], 
        on=["total_export_value", "total_import_value"],
        variable_name="metric", 
        value_name="val"
    ).with_columns(
        pl.col("val")/1_000_000_000
    )

    # Create the chart
    chart = alt.Chart(atlas_melt).mark_line().encode(
        x='year',      # :T specifies Temporal data type (dates/times)
        y='val:Q',     # :Q specifies Quantitative data type (numbers)
        color='metric:N' # :N specifies Nominal data type (categories/labels)
    ).properties(
        width=600,
        height=400,
        title="Stock Prices Over Time"
    )

    # Display the chart
    chart.show()
    return (alt,)


@app.cell
def _(alt, atlas, pl):
    atlas_balance = atlas.with_columns(
        Balance = pl.col("total_export_value") - pl.col("total_import_value") 
    ).select(
        "year", "Balance"
    ).with_columns(
        pl.col("Balance")/1_000_000_000
    ).sort("year", descending=False)

    alt.Chart(atlas_balance).mark_line().encode(
        x='year',      # :T specifies Temporal data type (dates/times)
        y='Balance:Q',     # :Q specifies Quantitative data type (numbers)
    ).properties(
        width=600,
        height=400,
        title="Stock Prices Over Time"
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT * FROM
        """
    )
    return


if __name__ == "__main__":
    app.run()
