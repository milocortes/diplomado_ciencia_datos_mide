import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import sqlalchemy

    return mo, pl, sqlalchemy


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # DuckDB para carga de CSV de datos de Comercio Bilateral
    """)
    return


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
        GROUP BY year
        ORDER BY year;
        """
    )
    return (atlas,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Graficamos las importaciones y exportaciones de México
    """)
    return


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
        x=alt.X('year').title("Year"),      # :T specifies Temporal data type (dates/times)
        y=alt.Y('val:Q').title("Miles de millones de pesos"),     # :Q specifies Quantitative data type (numbers)
        color=alt.Color('metric:N').title("Flujo") # :N specifies Nominal data type (categories/labels)
    ).properties(
        width=600,
        height=400,
        title="Exportaciones-Importaciones Mexicana"
    )

    # Display the chart
    chart.show()
    return (alt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Graficamos la Balanza Comercial de México vs USA
    """)
    return


@app.cell
def _(alt, atlas, pl):
    atlas_balance = atlas.with_columns(
        pl.col("year").cast(pl.String).str.to_datetime("%Y"),
         Balance = pl.col("total_export_value") - pl.col("total_import_value"),
 
    ).select(
        "year", "Balance"
    ).with_columns(
        pl.col("Balance")/1_000_000_000
    ).sort("year", descending=False)

    alt.Chart(atlas_balance).mark_line().encode(
        x=alt.X('year:T').title("Year"),
        y=alt.Y('Balance:Q').title("Balance Comercial [Miles de Millones de Dólares]"),
    ).properties(
        width=600,
        height=400,
        title="Balance Comercial de Mexico vs USA"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # DuckDB para cargar datos de SQLite
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        INSTALL sqlite;
        LOAD sqlite;

        ATTACH 'datos/onet/onet.db' AS onet (TYPE sqlite);
        USE onet;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Listemos las tablas en la base de datos
    """)
    return


@app.cell
def _(duckdb_tables, duckdb_views, mo):
    _df = mo.sql(
        f"""
        PRAGMA show_tables;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Consultemos la tabla `naics4d_onet_empleo`
    """)
    return


@app.cell
def _(mo, naics4d_onet_empleo):
    _df = mo.sql(
        f"""
        SELECT * FROM naics4d_onet_empleo;
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Polars para cargar datos de SQLite
    """)
    return


@app.cell
def _(pl, sqlalchemy):
    ## Iniciamos conexión con sqlite
    DATABASE_URL = "sqlite:///datos/onet/onet.db"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    # Inspect the database
    inspector = sqlalchemy.inspect(engine)

    # Get all table names
    table_names = inspector.get_table_names()

    ## Cargamos datos de ONET
    def get_tabla(tabla : str) -> pl.DataFrame:
        return pl.read_database(
                    query=f"SELECT * FROM {tabla}", 
                    connection=engine.connect(), 
                    infer_schema_length=None
                )

    onet_empleo = get_tabla("naics4d_onet_empleo")
    onet_empleo
    return get_tabla, onet_empleo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analicemos la actividad **Electrical Equipment Manufacturing**
    """)
    return


@app.cell
def _(onet_empleo, pl):
    electrical_manufacturing = onet_empleo.filter(
        # Filtramos por la actividad Electrical Equipment Manufacturing
        (pl.col("NAICS_TITLE") == "Electrical Equipment Manufacturing") & 
        # Filtramos por la clasificación detallada
        (pl.col("OCC_GROUP") == 'detailed') & 
        # Filtramos los registros donde no hay información por confidencialidad
        (pl.col("TOT_EMP") != "**")
    ).with_columns(
        # Convertimos la variable TOT_EMP a entero
        pl.col("TOT_EMP").cast(pl.Int32)
    ).with_columns(
        # Creamos la razón de empleo con respecto al total 
        razon = pl.col("TOT_EMP") / pl.col("TOT_EMP").sum()
    ).select(
        "NAICS", "NAICS_TITLE", "OCC_CODE", "OCC_TITLE", "TOT_EMP", "razon"
    )
    electrical_manufacturing
    return (electrical_manufacturing,)


@app.cell
def _(alt, electrical_manufacturing):
    ## Ocupaciones más importantes
    mas_importantes = electrical_manufacturing.sort("razon", descending=True).head(10)

    _chart = (
        alt.Chart(
            mas_importantes        
            )
            .mark_bar()
            .encode(
                x=alt.X(field='razon', type='quantitative'),
                y=alt.Y(field='OCC_TITLE', type='nominal').sort('-x'),
                tooltip=[
                    alt.Tooltip(field='OCC_TITLE'),
                    alt.Tooltip(field='razon', format=',.2f')
                ]
            )
            .properties(
                height=290,
                width='container',
                config={
                    'axis': {
                        'grid': False
                    }
                }
            )
    )

    _chart

    return (mas_importantes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ¿Qué Skills necesitan estas ocupacionezs?
    """)
    return


@app.cell
def _(get_tabla):
    skills = get_tabla("skills")
    skills
    return (skills,)


@app.cell
def _(pl, skills):
    skills_mas_importantes = skills.with_columns(
        pl.col("O*NET-SOC Code").map_elements(lambda x : x.split(".")[0])
    ).filter(
        pl.col("Scale ID")=="IM"
    ).group_by("O*NET-SOC Code", "Element Name").agg(
        pl.col("Data Value").mean()
    )
    skills_mas_importantes
    return (skills_mas_importantes,)


@app.cell
def _(mas_importantes, skills_mas_importantes):
    ## Reunimos datos
    skills_mas_importantes_weights = skills_mas_importantes.join(
        mas_importantes, 
        left_on="O*NET-SOC Code", 
        right_on="OCC_CODE",
        how="inner"
    )

    skills_mas_importantes_weights
    return (skills_mas_importantes_weights,)


@app.cell
def _(pl, skills_mas_importantes_weights):
    ## Calculemos un promedio ponderado de las Skills más importantes
    skills_mas_importantes_weights.group_by("Element Name").agg(
                weighted_avg = (pl.col("Data Value") * pl.col("razon")).sum() / pl.col("razon").sum()
    ).sort("weighted_avg", descending=True)
    return


if __name__ == "__main__":
    app.run()
