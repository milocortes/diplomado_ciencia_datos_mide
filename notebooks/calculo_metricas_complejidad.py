import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Cálculo de Métricas de Complejidad
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import math
    import altair as alt

    import polars as pl 
    import pandas as pd
    import numpy as np

    import polars.selectors as cs

    return alt, math, np, pd, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Datos : Comercio Internacional del Atlas de Complejidad Económica
    * Liga de descarga : https://atlas.hks.harvard.edu/data-downloads
    """)
    return


@app.cell
def _(pl):
    ## Cargamos los datos
    anio = 2023
    datos_atlas_url = "datos/complejidad_atlas/hs92_country_product_year_4_2023.csv"

    q = (
        pl.scan_csv(datos_atlas_url, ignore_errors = True).filter(
            year=anio
        )
    )

    datos = q.collect().drop_nulls("product_hs92_code")
    return anio, datos


@app.cell
def _(datos):
    datos
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Matriz de Especialización, $R$

    * Una Matriz de Especialización, $R$, se define al dividir cada entrada de la matriz $X_{c p}$ por la suma de sus respectivas filas o columnas.
    * Está medida se le conoce como **cociente de ubicación** o **Revealed Comparative Advantage, (RCA)**.


    \begin{equation}
        R_{c p}= \frac{x_{c p} / \Sigma_p x_{c p}}{\Sigma_c x_{c p} / \Sigma_c \Sigma_p x_{c p}}
    \end{equation}

    * Ubicaciones con $R_{c p} > 1$ se consideran **especializadas en la actividad $p$**.
    """)
    return


@app.cell
def _(datos, pl):
    datos_rca = datos.with_columns(
        rca = (
            pl.col("export_value")/pl.col("export_value").sum().over("country_iso3_code")
        ) /
        (
            pl.col("export_value").sum().over("product_hs92_code")/pl.col("export_value").sum()
        )

    ).with_columns(
        pl.col("product_hs92_code").cast(pl.Int64)
    )

    datos_rca
    return (datos_rca,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Matriz de Especialización Binaria, $M$

     Definimos la Matriz de Especialización Binaria, $M$, como

    \begin{equation}
    M_{c p}=\left\{\begin{array}{lll}
    1 & \text { if } & R_{c p} \geq R^{\star} \\
    0 & \text { if } & R_{c p}<R^{\star}
    \end{array}\right.
    \end{equation}

    donde $R^{\star}=1$ cuando usamos $R$ y $R^{\star}=0.25$ cuando usamos $R^{\text{pop}}$
    """)
    return


@app.cell
def _(datos_rca, pl):
    ## Umbral de RCA
    rca_umbral = 1.0

    datos_rca_m = datos_rca.with_columns(
        M = pl.when(
            pl.col("export_rca")>= rca_umbral   
        ).then(
            pl.lit(1)
        ).otherwise(
            pl.lit(0)
        )
    )
    return (datos_rca_m,)


@app.cell
def _(datos_rca_m):
    M_df = datos_rca_m.pivot("product_hs92_code", 
                      index = "country_iso3_code", 
                      values = "M"
                ).fill_null(0).sort("country_iso3_code")
    M_df
    return (M_df,)


@app.cell
def _(M_df, pl):
    M = M_df.select(
        pl.exclude("country_iso3_code")
    ).to_numpy()

    M
    return (M,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Proximidad

    Hay múltiples formas de medir **Proximidad**. Algunas, como la **probabilidad condicional mínima**, miran a la colocalización o coaglomeración de actividades:

    \begin{equation}
      \phi_{p p^{\prime}}=\frac{\sum_c M_{c p} M_{c p^{\prime}}}{\max \left(M_p, M_{p,}\right)}
    \end{equation}
    """)
    return


@app.cell
def _(M, np, ubicuidad):
    proximity = M.T @ M / ubicuidad[np.newaxis, :]  
    proximity = np.minimum(proximity, proximity.T)
    proximity = np.nan_to_num(proximity)
    proximity
    return (proximity,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Relatedness Density

    * Con la medida de proximidad, podemos calcular **Relatedness Density** como la fracción de actividades relacionadas presentes en una ubicación

    \begin{equation}
    \omega_{c p}=\frac{\sum_{p \prime} M_{c p \prime} \phi_{p p^{\prime}}}{\sum_{p,} \phi_{p p^{\prime}}} \quad \circ \quad \omega_{c p}=\frac{\sum_{c^{\prime}} M_{c^{\prime}} \phi_{c^{\prime} c}}{\sum_{c^{\prime}} \phi_{c^{\prime} c}}
    \end{equation}
    """)
    return


@app.cell
def _(M, np, proximity):
    density = (np.dot(M,proximity)/np.sum(proximity, axis=1))
    density = np.nan_to_num(density)
    density
    return (density,)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Distancia
    - La Proximidad mide la similaridad entre pares de actividades-productos.
    - Necesitamos una medida que cuantifique la **Distancia** entre las actividades especializadas en un país y las actividades donde no está especializada.


    \begin{equation}
    d_{c p}=\frac{\sum_{p'} (1 - M_{c p'}) \phi_{p p^{\prime}}}{\sum_{p,} \phi_{p p^{\prime}}}
    \end{equation}

    - La distancia nos da una idea de qué tan lejos está cada actividad dado el ecosistema productivo del país.
    """)
    return


@app.cell
def _(M, np, proximity):
    distancia = (np.dot((1 - M),proximity)/np.sum(proximity, axis=1))
    distancia = np.nan_to_num(distancia)
    distancia
    return (distancia,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Verifica Distancia
    """)
    return


@app.cell
def _(M_df, distancia, pd, pl):
    ## Convertimos a dataframe la matriz de distancia
    df_distance = pd.DataFrame(distancia, 
                 columns = [int(i) for i in M_df.columns[1:]], 
                 index = M_df["country_iso3_code"]
    ).reset_index().rename(
        columns = {
            "index" : "country_iso3_code"
        }
    ).melt(id_vars="country_iso3_code").rename( columns=
        {
            "variable" : "product_hs92_code",
            "value" : "distancia"
        }
    )
    df_distance = pl.from_pandas(df_distance)
    df_distance
    return (df_distance,)


@app.cell
def _(datos_rca, df_distance):
    ### Reunimos los datos calculados 
    df_distancia_test = df_distance.join(
        datos_rca.select(
                "country_iso3_code", "product_hs92_code", "distance"
            ).rename(
                {
                    "distance" : "distancia_atlas"
                }
            ),
        on = ["country_iso3_code", "product_hs92_code"]
    )

    df_distancia_test
    return (df_distancia_test,)


@app.cell
def _(alt, df_distancia_test):
    ## Graficamos el ajuste del PCI calculado con el del Atlas
    distancia_original_vs_distancia_estimada = (
        alt.Chart(df_distancia_test.filter(country_iso3_code="MEX"))
        .mark_point()
        .encode(
            x=alt.X("distancia_atlas").title("Distancia Atlas").scale(zero=False), 
            y=alt.Y("distancia").title("Distancia Calculada").scale(zero=False)
        )
        .properties(width=800, title='Distancia Atlas vs Distancia Calculada')
    )
    distancia_original_vs_distancia_estimada + distancia_original_vs_distancia_estimada.transform_regression('distancia_atlas', 'distancia').mark_line()
    return


@app.cell
def _(df_distancia_test):
    ## Calculamos coeficiente de correlación
    df_distancia_test.drop("country_iso3_code", "product_hs92_code").to_pandas().corr()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Economic Complexity

    - Las medidas de **Complejidad Económica** miden la capacidad económica con **métodos de reducción de dimensionalidad**.
    - Representan también funciones de producción generalizadas de dimensionalidad reducida.
    - Las medidas de complejidad económica pueden ser utilizadas para medir la presencia de múltiples factores económicos en una forma que es **agnóstica** sobre cuales podrían ser esos factores.
      - Formalmente, la complejidad $K_c$ de una ubicación $c$ y la complejidad $K_p$ de una actividad $p$ puede definirse como una función una de la otra:

    \begin{equation}
    K_c=f\left(M_{c p}, K_p\right)
    \end{equation}

    \begin{equation}
    K_p=g\left(M_{c p}, K_c\right)
    \end{equation}

    - Estas ecuaciones declaran que la complejidad de una ubicación es una función de la complejidad de las actividades que están presentes en esta, y viceversa.
    - Una economía es tan compleja como las actividades que puede realizar, y una actividad es tan compleja como los lugares que pueden realizarla.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ¿Cómo medimos la complejidad?

    - La idea de medir la complejidad usando estas ecuaciones acopladas fue introducida por Cesar Hidalgo y Ricardo Haussman. Los autores utilizan promedios simples para $f$ y $g$.
    - Las medidas resultantes se conocen como **Índice de Complejidad Económica, (ECI; $K_c$)** y el **Índice de Complejidad de Producto, (PCI; $K_p$)**.
    - Estas medidas están definidas por el siguiente sistema de ecuaciones:

    \begin{equation}
    K_c=\frac{1}{M_c} \sum_p M_{c p} K_p
    \end{equation}

    \begin{equation}
    K_p=\frac{1}{M_p} \sum_c M_{c p} K_c
    \end{equation}

    Reemplazando la segunda ecuación en la primera:

    \begin{equation}
        K_c=\widetilde{M}_{c c}, K_{c t}
    \end{equation}

    donde

    \begin{equation}
    \widetilde{M}_{c c \prime}=\sum_p \frac{M_{c p} M_{c \prime p}}{M_c M_p}
    \end{equation}
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Originalmente el cálculo de ECI y PCI se definió mediante un método iterativo llamado  **algoritmo de reflexión** que primero calcula la diversidad y ubicuidad para posteriormente y luego utiliza recursivamente la información de uno para corregir el otro.
    - Se puede demostrar que el método de reflección es equivalente a encontrar los eigenvalores de la matriz $\widetilde{M}$

    \begin{equation}
    \tilde{M}=D^{-1} M U^{-1} M^{\prime}
    \end{equation}

    donde $D$ es la matriz diagonal formada a partir del vector de diversidad y $U$ es la matriz diagonal formada a partir del vector de ubicuidad

    En el contexto de datos de comercio entre países, podemos pensar a $\widetilde{M}$ como una matriz de diversidad-ponderada (o normalizada) que refleja qué tan similares son las canastas exportadoras de los dos países, es decir, que tan similares son sus patrones de especialización.

    De la ecuación anterior podemos ver que:

    \begin{equation}
    \tilde{M}=D^{-1} S
    \end{equation}

    donde $S = M U^{-1} M^\prime$ es una matriz de similaridad simétrica en que cada elemento $S_{c c'}$ representa los productos que el pais $c$ tiene en común con el país $c'$, ponderado o normalizado por la inversa de la ubicuidad de cada producto.
    """)
    return


@app.cell
def _(M, np):
    ## Calculamos diversidad
    diversidad = M.sum(axis = 1)
    D = np.diag(diversidad)

    ## Calculamos ubicuidad
    ubicuidad = M.sum(axis = 0)
    U = np.diag(ubicuidad)
    return D, U, diversidad, ubicuidad


@app.cell
def _(D, M, U, np):
    # Calculamos M tilde cc
    M_tilde_cc = np.linalg.pinv(D) @ M @ np.linalg.pinv(U) @ M.T
    M_tilde_cc 
    return (M_tilde_cc,)


@app.cell
def _(D, M, U, np):
    # Calculamos M tilde pp
    M_tilde_pp = np.linalg.pinv(U) @ M.T @ np.linalg.pinv(D) @ M
    M_tilde_pp 
    return (M_tilde_pp,)


@app.cell
def _(M_tilde_cc, np):
    ## Calculamos los eigenvectores y eigenvalores de la matriz M tilde cc
    eigenvalues_cc, eigenvectors_cc = np.linalg.eig(M_tilde_cc)

    ## Obtenemos el eigenvector asociado con el segundo eigenvalor más grande
    Kc = eigenvectors_cc[:, 1]

    Kc
    return (Kc,)


@app.cell
def _(M_tilde_pp, np):
    ## Calculamos los eigenvectores y eigenvalores de la matriz M tilde cc
    eigenvalues_pp, eigenvectors_pp = np.linalg.eig(M_tilde_pp)

    ## Obtenemos el eigenvector asociado con el segundo eigenvalor más grande
    Kp = eigenvectors_pp[:, 1].astype(float)

    Kp 
    return (Kp,)


@app.cell
def _(Kc, diversidad, math, np):
    ## Adjust sign of ECI and PCI so it makes sense, as per book
    corr_mat = np.corrcoef(diversidad, Kc)
    s1 = math.copysign(1.0, corr_mat[0,1])
    return (s1,)


@app.cell
def _(Kc, Kp, np, s1):
    ## Ajustamos y normalizamos ECI y PCI
    # La normalización usando usando la media y std ECI preserva
    # Que ---> ECI = (mean of PCI of products for which MCP=1)

    eci = (s1*(Kc - np.mean(Kc))/np.std(Kc)).real
    pci = (Kp - np.mean(Kp))/np.std(Kp)
    return eci, pci


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Verificamos el ajuste con los datos del Atlas de Complejidad
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Verifica ECI
    """)
    return


@app.cell
def _(anio, pl):
    ### Cargamos datos de ECI de los paises
    github_eci_url = "datos/complejidad_atlas/growth_proj_eci_rankings.csv"

    eci_atlas = pl.read_csv(github_eci_url)

    ### Filtramos para el año de estudio
    eci_atlas = eci_atlas.filter(year = anio)

    eci_atlas
    return (eci_atlas,)


@app.cell
def _(M_df, eci, eci_atlas, pl):
    ### Reunimos los datos calculados 
    df_eci_test = pl.DataFrame(
          {
            "country_iso3_code" : M_df["country_iso3_code"], 
            "eci" : eci  
        }  
    ).join(eci_atlas.select("country_iso3_code","eci_hs92").unique(), on = "country_iso3_code")

    df_eci_test
    return (df_eci_test,)


@app.cell
def _(alt, df_eci_test):
    ## Graficamos el ajuste del PCI calculado con el del Atlas
    eci_original_vs_pci_estimado = (
        alt.Chart(df_eci_test)
        .mark_point()
        .encode(
            x=alt.X("eci_hs92").title("ECI Atlas"), 
            y=alt.Y("eci").title("ECI Calculado")
        )
        .properties(width=800, title='ECI Atlas vs ECI Calculado')
    )
    eci_original_vs_pci_estimado + eci_original_vs_pci_estimado.transform_regression('eci_hs92', 'eci').mark_line()
    return


@app.cell
def _(df_eci_test):
    ## Calculamos coeficiente de correlación
    df_eci_test.drop("country_iso3_code").to_pandas().corr()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Verifica PCI
    """)
    return


@app.cell
def _(M_df, datos, pci, pl):
    ### Reunimos los datos calculados
    df_pci_test = pl.DataFrame(
          {
            "product_hs92_code" : [int(i) for i in M_df.columns[1:]], 
            "pci" : pci  
        }  
    ).join(datos.select("product_hs92_code","pci").unique(), on = "product_hs92_code")

    df_pci_test
    return (df_pci_test,)


@app.cell
def _(alt, df_pci_test):
    ## Graficamos el ajuste del PCI calculado con el del Atlas
    pci_original_vs_pci_estimado = (
        alt.Chart(df_pci_test)
        .mark_point()
        .encode(
            x=alt.X("pci").title("PCI Atlas"), 
            y=alt.Y("pci_right").title("PCI Calculado")
        )
        .properties(width=800, title='PCI Atlas vs PCI Calculado')
    )
    pci_original_vs_pci_estimado + pci_original_vs_pci_estimado.transform_regression('pci', 'pci_right').mark_line()
    return


@app.cell
def _(df_pci_test):
    ## Calculamos coeficiente de correlación
    df_pci_test.drop("product_hs92_code").to_pandas().corr()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Opportunity Value - Economic Complexity Outlook Index (COI)

    - Los lugares difieren no sólo en lo que se especializan o producen, sino también en sus oportunidades.
    - Este **opportunity value** de opciones explotadas se cuantifica al agregar el nivel de complejidad de las actividades que actualmente no están especializadas, ponderado por cuán cerca están estos productos del ecosistema productivo actual del lugar.

    \begin{equation}
        \text { opportunity value }_c=\sum_{p^{\prime}}\left(1-d_{c p^{\prime}}\right)\left(1-M_{c p^{\prime}}\right) P C I_{p^{\prime}}
    \end{equation}

    - El término $1 - M_{c p\prime}$ se asegura de contabilizar solo actividades no especializadas.
    - Un valor alto del opportunity value implica estar en la proximidad de más actividades y/o de actividades más complejas.
    """)
    return


@app.cell
def _(M, density, np, pci):
    # Calculamos Opportunity Value
    ov = ((density.T * (1 - M.T)) * pci[np.newaxis].T).sum(axis=1)
    ov
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Opportunity Gain - Opportunity Outlook Gain (COG)

    - Podemos utilizar el opportunity value para calcular el beneficio potencial que obtendría un lugar si se especializa en una nueva actividad particular.
    - Se llama a este valor como la **ganancia de oportunidad (Opportunity Gain)** que un lugar $c$ obtendría de especializarse en la actividad $p$.
    - Se calcula como el cambio en el valor de oportunidad obtenido de especializarse en la actividad $p$.
    - La ganancia de oportunidad cuantifica la contribución de especializarse en una nueva actividad en términos de abrir las puertas a actividades cada vez más complejas.
    - Formalmente la calculamos como:

    \begin{equation}
    \text { opportunity gain }_c=\sum_{p^{\prime}} \frac{\phi_{p p^{\prime}}}{\sum_{p^{\prime \prime}} \phi_{p^{\prime \prime} p^{\prime}}}\left(1-M_{c p^{\prime}}\right) P C I_{p^{\prime}}
    \end{equation}

    >En la publicación **The atlas of economic complexity: Mapping paths to prosperity** se especifica la siguiente fórmula para el Opportunity Gain
    >
    \begin{equation}
    \text { opportunity gain }_c=\sum_{p^{\prime}} \frac{\phi_{p p^{\prime}}}{\sum_{p^{\prime \prime}} \phi_{p^{\prime \prime} p^{\prime}}}\left(1-M_{c p^{\prime}}\right) P C I_{p^{\prime}}-\left(1-d_{c p}\right) P C I_p
    \end{equation}

    > Aquí usaremos la especificación del glosario del portal del Atlas de Complejidad Económica ([liga](https://atlas.hks.harvard.edu/glossary))
    """)
    return


@app.cell
def _(M, np, pci, proximity):
    #og = (1-M) * ((1 - M) @ (proximity * (pci/ proximity.sum(axis=1))[:, np.newaxis]))
    og = (proximity  @ ((proximity.sum(axis=1)**-1)[np.newaxis].T * (1 - M.T) * (pci[np.newaxis].T))).T
    og
    return (og,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Verifica Opportunity Gain
    """)
    return


@app.cell
def _(M_df, og, pd, pl):
    ## Convertimos a dataframe la matriz de distancia
    df_cog = pd.DataFrame(og, 
                 columns = [int(i) for i in M_df.columns[1:]], 
                 index = M_df["country_iso3_code"]
    ).reset_index().rename(
        columns = {
            "index" : "country_iso3_code"
        }
    ).melt(id_vars="country_iso3_code").rename( columns=
        {
            "variable" : "product_hs92_code",
            "value" : "cog"
        }
    )
    df_cog = pl.from_pandas(df_cog)
    df_cog
    return (df_cog,)


@app.cell
def _(datos_rca, df_cog):
    ### Reunimos los datos calculados 
    df_cog_test = df_cog.join(
        datos_rca.select(
                "country_iso3_code", "product_hs92_code", "cog"
            ).rename(
                {
                    "cog" : "cog_atlas"
                }
            ),
        on = ["country_iso3_code", "product_hs92_code"]
    )
    return (df_cog_test,)


@app.cell
def _(alt, df_cog_test):
    ## Graficamos el ajuste del PCI calculado con el del Atlas
    cog_original_vs_cog_estimada = (
        alt.Chart(df_cog_test.filter(country_iso3_code="USA"))
        .mark_point()
        .encode(
            x=alt.X("cog_atlas").title("COG Atlas").scale(zero=False), 
            y=alt.Y("cog").title("COG Calculada").scale(zero=False)
        )
        .properties(width=800, title='COG Atlas vs COG Calculada')
    )
    cog_original_vs_cog_estimada + cog_original_vs_cog_estimada.transform_regression('cog_atlas', 'cog').mark_line()
    return


@app.cell
def _(df_cog_test):
    ## Calculamos coeficiente de correlación
    df_cog_test.drop("country_iso3_code", "product_hs92_code").to_pandas().corr()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Verifica Gráfica Growth Opportunities Atlas
    """)
    return


@app.cell
def _(df_cog_test, df_distancia_test):
    test_growth_opp = df_cog_test.join(
        df_distancia_test,
        on = ["country_iso3_code", "product_hs92_code"]
    )
    test_growth_opp
    return (test_growth_opp,)


@app.cell
def _(alt, test_growth_opp):
    ## Graficamos el ajuste del PCI calculado con el del Atlas
    alt.Chart(test_growth_opp.filter(country_iso3_code="MEX")).mark_point().encode(
            x=alt.X("distancia").title("Distancia").scale(zero=False), 
            y=alt.Y("cog").title("COG").scale(zero=False)
        ).properties(width=800, title='COG vs Distancia')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
