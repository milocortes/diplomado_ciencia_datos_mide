// Get Polylux from the official package repository
#import "@preview/polylux:0.4.0": *
#import "@preview/codly:1.2.0": *
#import "@preview/codly-languages:0.1.1": *
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "@preview/pinit:0.2.2": *
#import "@preview/thmbox:0.3.0": *

#show: codly-init.with()
#codly(zebra-fill: none)

#show link: set text(fill: blue)
#show link: underline

// Make the paper dimensions fit for a presentation and the text larger
#let ukj-blue = rgb(0, 84, 163)

// Make the paper dimensions fit for a presentation and the text larger
#set page(paper: "presentation-16-9")
#set text(size: 20pt, font: "Lato")

#show <a>: set text(blue)

#show raw: it => {
  show regex("pin\d"): it => pin(eval(it.text.slice(3)))
  it
}


#codly(
  languages: (
    rust: (name: "Rust", icon: "🦀", color: rgb("#CE412B")),
    python : (name : "Python", icon : "🐍")
  )
)

// Use #slide to create a slide and style it using your favourite Typst functions
#slide[
  #set align(horizon)
  = Query Engines

  Hermilo

  17 de Febrero de 2026
]

#slide[

  #text(font: "Lato", size : 22pt)[
  = Apache Arrow
  - El  proyecto #text(fill: ukj-blue)[*Apache Arrow*] es un gran esfuerzo dirigido a resolver los problemas fundamentales de la analítica de datos.
  - Apache Arrow define un #text(fill: ukj-blue)[*formato de memoria columnar*] estandarizado e independiente del lenguaje, diseñado explícitamente para facilitar el análisis de datos de alto rendimiento y el intercambio de información. 
  - Su innovación clave reside en una estructura en memoria cuidadosamente diseñada y optimizada para las arquitecturas de CPU modernas, lo que permite el acceso a datos sin copias (*zero-copy*), el uso eficiente de instrucciones SIMD y una interoperabilidad fluida entre diversos motores de procesamiento de datos y lenguajes de programación.
  ]
]


#slide[
    == ¿Qué es Apache Arrow?
    #toolbox.side-by-side(gutter: 3mm, columns: (2fr, 1.5fr), 

  [
        #figure(
        image("images/apache_arrow.png", width: 100%),
        numbering: none
      )

  ], 
        [
        #figure(
        image("images/apache_arrow_logo.png", width: 75%),
        numbering: none
      )
        #text(font: "Lato", size : 12pt)[
          - Estandar de intercambio de datos. 
          - Un formato in-memory.
          - Un formato de Red. 
          - Un formato de Almacenamiento. 
          - Biblioteca de I/O
          - Biblioteca de cómputo vectorizado.
          - Biblioteca de manejo de dataframes.
          - Un query engine.
          - Administrador de datasets particionados.
        ]

      ]

  )
]


#slide[

  #text(font: "Lato", size : 24pt)[
      == Apache Arrow

  - Apache Arrow nació como un #text(fill: ukj-blue)[*Formato Columnar de Datos*].
  - El núcleo del modelo de memoria de Arrow es la #text(fill: ukj-blue)[*estructura de datos columnar*], que organiza la información en búferes de memoria contiguos, cada uno de los cuales representa una columna lógica. 
  - Esta disposición contrasta con el almacenamiento tradicional basado en filas al permitir operaciones vectorizadas y mejorar la eficiencia de la caché.
  ]
]

#slide[
  == ¿Qué es #text(fill: ukj-blue)[*Columnar*]?
    #toolbox.side-by-side(gutter: 3mm, columns: (2fr, 1.5fr), 

  [
        #figure(
        image("images/apache_arrow_columnas.png", width: 100%),
        numbering: none
      )

  ], 
        [
        #figure(
        image("images/apache_arrow_columnas_dos.png", width: 75%),
        numbering: none
      )

      ]

  )
]

#slide[
  == ¿Qué es #text(fill: ukj-blue)[*Columnar*]?
    #toolbox.side-by-side(gutter: 3mm, columns: (2fr, 1.5fr), 

  [
    Con el formato columnar se aprovecha : 
    - Localidad de Memoria.
    - I/O 
    - Vectorización

  ], 
        [
        - *Consulta* : #text(fill: ukj-blue)[*Todos los arqueros en Europa*], *solo se necesitan dos columnas!*. Menos operaciones de I/O, menos uso de memoria.

        - *Consulta* : #text(fill: ukj-blue)[*Calcula la media para la columna Year*], *solo se necesita una columna!*
          - Vectorizar operaciones requiere memoria contigua.
          - La columna ya se encuentra en memoria contigua!


      ]

  )
]

#slide[

  #text(font: "Lato", size : 24pt)[
      == PyArrow

  - #text(fill: ukj-blue)[*PyArrow*] es el punto de entrada al ecosistema de Apache Arrow para desarrolladas de Python, y es el medio que ofrece el acceso a los muchos beneficios de Arrow.  
  - De manera que el tipo fundamental de datos en PyArrow es una *columna de datos* la cual es expuesta por mendio de un objeto `pyarrow.Array`. 
  - A este nivel, PyArrow es similar a los arreglos 1D de #text(fill: ukj-blue)[*NumPy*]. 
  ]
]


#slide[
  == PyArrow Arrays
    #toolbox.side-by-side(gutter: 3mm, columns: (2fr, 1.5fr), 

  [

    #text(font: "Lato", size : 16pt)[
  ```python 
  import pyarrow as pa 
  
  ## Arrays can be made of numbers
  >>> pa.array([1, 2, 3, 4, 5]) 

  ## Or strings
  >>> pa.array(["A", "B", "C", "D", "E"])

  ## Or even complex objects
  >>> pa.array([{"a" : 5}, {"b" : 10}])  

  ## Arrays can also be masked
  >>> pa.array([1, 2, 3, 4, 5], 
  mask = pa.array([True, False, True, False, True]) )

  ```
    ]

  ], 
        [
        #text(font: "Lato", size : 16pt)[

    Comparado a los arreglos clásicos de NumPy, los arreglos de PyArrow son un poco más complejos.
          - Estandar de intercambio de datos. 

        ]

      ]

  )
]

#slide[
  == Manipulación de Arreglos 

#toolbox.side-by-side(gutter: 3mm, columns: (1.5fr, 2fr), 

  [

    #text(font: "Lato", size : 15pt)[
  - La comunidad Arrow ha creado una implementación de referencia de código abierto de un motor de cálculo y consulta basado en el formato Arrow llamado #text(fill: ukj-blue)[*Acero*].

  - PyArrow proporciona también acceso al motor de cálculo #text(fill: ukj-blue)[*Acero*] mediante el módulo `pyarrow.compute`. 

  - Para este fin, existe la biblioteca Acero para facilitar diversas implementaciones de alto rendimiento de funciones que operan con datos con formato Arrow, junto con la creación de planes de ejecución de filtrados, agregaciones y transformaciones para flujos de datos.
    ]

  ], 
        [
    #text(font: "Lato", size : 16pt)[
  ```python 
  import pyarrow.compute as pc 
  
  >>> arr = pa.array([1, 2, 3, 4, 5]) 
  >>> pc.multiply(arr, 2)
  >>> pc.value_counts(arr)  
  >>> pc.min_max(arr)
  ```
    ]

      ]

  )
]

#slide[
  #text(font: "Lato", size : 28pt)[
  
  == PyArrow Tables 

  - Como los arreglos son "columnas", estos puden ser agrupados para formar `pyarrow.Table`.
  - Las tablas son constituidas por `pyarrow.ChunkedArray` de manera que concatenar filas a ellas resultan una operación barata.

  - A este nivel, PyArrow es similar a los #text(fill: ukj-blue)[*DataFrames de Pandas*]. 

  ]
]


#slide[
  == PyArrow Tables
    #toolbox.side-by-side(gutter: 3mm, columns: (2fr, 1.5fr), 

  [

    #text(font: "Lato", size : 18pt)[
  ```python 
  >>> table = pa.table([
    pa.array([1, 2, 3, 4, 5]),
    pa.array(["a", "b", "c", "d", "e"]),
    pa.array([1.0, 2.0, 3.0, 4.0, 5.0]),
  ], names = ["col1", "col2", "col3"])
  >>> table.take([0, 1, 4])
  col1: [[1,2,5]]
  col2: [["a","b","e"]]
  col3: [[1,2,5]] 
  >>> table.schema
  col1: int64
  col2: string
  col3: double
  ```
    ]


  ], 
        [
        #text(font: "Lato", size : 16pt)[

    - Comparado a Pandas, las tablas de PyArrow son completamente implementadas en C++ y nunca modifican datos *in-place*.

    - `Tables` están basadas en #text(fill: ukj-blue)[*ChunkedArrays*] de manera que concatenar datos es una operación *zero copy*. 
    
    ///Se crea una nueva tabla que hace referencia a los datos de la tabla existente como el primer fragmento de las matrices y los datos agregados ven el nuevo fragmento.

    - El motor de cómputo Acero en Arrow es capaz de proporcionar muchas de las operaciones comunes de la analítica de datos como joining, filtrados y agregaciones de datos.



        ]

      ]

  )
]

#slide[
  == Ejecutando Analítica de Datos

#toolbox.side-by-side(gutter: 3mm, columns: (1.5fr, 2fr), 

  [

    #text(font: "Lato", size : 18pt)[
  - El motor de cómputo de Acero potencia las capacidades de análisis y transformación disponibles en las tablas
  - Muchas funciones de `pyarrow.compute` proporcionan kernels que operan en tablas y las `Table` exponen métodos de join, filtrado y agrupación.
    ]

  ], 
        [
    #text(font: "Lato", size : 14pt)[
  ```python 
  import pyarrow as pa
  import pyarrow.compute as pc 
  
  >>> table = pa.table([
    pa.array(["a", "a", "b", "b", "c", "d", "e", "c"]),
    pa.array([11, 20, 3, 4, 5, 1, 4, 10])
  ], names = ["keys", "values"])
  >>> table.filter(pc.field("values") == )
  >>> table.group_by("keys").aggregate(["keys", "sum"])
  >>> table1 = pa.table({"id" : [1, 2, 3], 
    "year" : [2020, 2022, 2019]
  })
  >>> table2 = pa.table({"id" : [3, 4], 
    "n_legs" : [5, 100], 
    "animal" : ["Brittle Stars", "Centipede"]
  })
  >>> table1.join(table2, keys = "id")
  ```
    ]

      ]

  )
]

/*
#slide[
  == PyArrow, NumPy y Pandas

        #text(font: "Lato", size : 24pt)[
        - Uno de las metas de diseño originales de Apache Arrow fue permitir el fácil intercambio de datos sin el costo de convertir a través de múltiples formatos o serializarlos antes de transferirlos.
        - PyArrow proporciona el soporte de conversión de datos copy-free de y hacía pandas y numpy.
        - Si tenemos datos en PyArrow podemos invocar al método `to_numpy` del objeto `pyarrow.Array` y `to_pandas` en  `pyarrow.Array` y `pyarrow.Table` para convertirlos a objetos de pandas o numpy sin enfrentar ningún costo adicional de conversión.
        ]
]

#slide[
  == PyArrow, NumPy y Pandas
    #toolbox.side-by-side(gutter: 3mm, columns: (2fr,2fr), 

  [
        #figure(
        image("images/intercambio_datos.png", width: 110%),
        numbering: none
      )

  ], 
        [
        #figure(
        image("images/intercambio_datos_arrow.png", width: 110%),
        numbering: none
      )


      ]

  )

  Tomado de *In-Memory Analytics with Apache Arrow*
]
#slide[
  == Y es rápido!!
#text(font: "Lato", size : 18pt)[
  ```python 
  >>> data = [a % 5 for a in range(100_000_000)]
  >>> npdata = np.array(data)
  >>> padata = np.array(data)
  >>> import timeit
  >>> timeit.timeit(
    lambda: np.unique(npdata, return_counts = True),
    number = 1
  )
  >>> timeit.timeit(
    lambda: pc.value_counts(padata),
    number=1
  )
  ```
]
]

#slide[
  #text(font: "Lato", size : 26pt)[
  == Datasets 
  - #text(fill: ukj-blue)[*Datasets*] son una abstracción que permite trabajar con grandes conjuntos tabulares de datos, potencialmente más grandes que la memoria y distribuidos a través de múltiples archivos.
  - Datasets proporciona un acceso #text(fill: ukj-blue)[*lazy*], evitando la necesidad de cargar todos los datos en memoria inmediatamente.
  - Datasets son compatibles con el motor de cómputo Acero en la mayoría de los casos en lugar de las tablas.
  ]
]

#slide[
  == Datasets

  #figure(
    image("images/datasets_api.png", width: 110%), 
    numbering: none
  )
]

#slide[
  #text(font: "Lato", size : 26pt)[
  == Datasets
  - En el actual ecosistema de #text(fill: ukj-blue)[*data lakes*] y #text(fill: ukj-blue)[*lakehouses*], muchos conjuntos de datos son ahora enormes colecciones de archivos en estructuras de directorios particionados en lugar de un solo archivo.
  - La API Datasets proporciona una serie de utilidades para interactuar fácilmente con conjuntos de datos grandes, distribuidos y posiblemente particionados que se distribuyen en múltiples archivos.
  ]
]
*/

#slide[
  == Apache Parquet, a columnar storage format
        #figure(
        image("images/parquet2.jpg", width: 75%),
        numbering: none
      )

]

#slide[
  == Parquet, a columnar storage format
  - Parquet almacena los datos en columnas en lugar de en filas, a diferencia de los formatos de almacenamiento tradicionales basados ​​en filas (como CSV o JSON).
 - Este diseño columnar implica que, cuando una consulta solo necesita acceder a unos pocos campos o columnas específicos de un conjunto de datos, Parquet puede leer únicamente las columnas relevantes sin cargar la fila completa en la memoria.
 - Parquet también emplea diversas técnicas para mejorar aún más el rendimiento y reducir los costes de almacenamiento:
  - Compression
  - Encoding
  - Metadata and statistics
]


#slide[
  == Data Lakes hacen uso intensivo de archivos Parquet.
    #toolbox.side-by-side(gutter: 3mm, columns: (2fr,2fr), 

  [
        #figure(
        image("images/delta_lake.png", width: 64%),
        numbering: none
      )

  ], 
        [
        #figure(
        image("images/delta_lake_transaction_log.png", width: 130%),
        numbering: none
      )


      ]

  )

   #text(font: "Lato", size : 10pt)[Tomado de Denny Lee, “Understanding the Delta Lake Transaction Log at the File Level”, Denny Lee (blog), November 26, 2023.]
]

#slide[
  == Data Lakes hacen uso intensivo de archivos Parquet.
    #toolbox.side-by-side(gutter: 3mm, columns: (2fr,2fr), 

  [
        #figure(
        image("images/delta_lake_v0.png", width: 100%),
        numbering: none
      )

  ], 
        [
        #figure(
        image("images/delta_lake_v1.png", width: 100%),
        numbering: none
      )


      ]

  )

   #text(font: "Lato", size : 10pt)[Tomado de Denny Lee, “Understanding the Delta Lake Transaction Log at the File Level”, Denny Lee (blog), November 26, 2023.]
]

/*
#slide[
  == PyArrow Datasets

    #toolbox.side-by-side(gutter: 3mm, columns: (2fr, 1.5fr), 

  [

    #text(font: "Lato", size : 14pt)[
  ```python 
  >>> from deltalake import DeltaTable
  >>> import pyarrow.dataset as ds

  # Cargamos la Delta table
  >>> dt = DeltaTable("datos/atlas")

  # Convertimos a PyArrow Dataset
  >>> dataset = dt.to_pyarrow_dataset()

  # Observamos los primeros 10 registros
  >>> dataset.head(10)

  # Filtramos sólo registros de México en 2024
  >>> filtrado = dataset.scanner(filter=ds.field("year") == 2024)#.to_table()

  ```
    ]


  ], 
        [
        #text(font: "Lato", size : 18pt)[

    - `Datasets` proporciona acceso lazy a grandes volúmenes de datos guardados en cualquiera de los formatos soportados por PyArrow y accesibles mediante cualquier *FileSystems* reconocido por PyArrow.
    - Los `Datasets` pueden siempre ser convertidos de regreso a `Tables` para tener acceso al conjunto completo de datos mediante la API de `Tables`.
        ]

      ]

  )

]
*/

#slide[
   #text(font: "Lato", size : 20pt)[
  == Query Engines
  - Los #text(fill: ukj-blue)[*Query Engines*]#footnote[Motores de procesamiento de consultas] incorporan patrones arquitectónicos sofisticados, diseñados para transformar consultas declarativas en planes de ejecución eficientes que aprovechan el hardware subyacente y las estructuras de datos.
   ]
]

#slide[
   #text(font: "Lato", size : 20pt)[
  == Query Engines
  - Un #text(fill: ukj-blue)[*Query Engine*] transforma una consulta (como una consulta SQL) en resultados concretos a través de varias etapas:
    - *Parsing (Análisis sintáctico)* : Convierte el texto de la consulta en una representación estructurada (como un árbol de sintaxis abstracta)
    - *Planificación*: Determinar qué operaciones son necesarias (escaneo, filtrado, unión, agregación)
    - *Optimización*: Reordenar y transformar las operaciones para lograr eficiencia
    - *Ejecución* : Procesar los datos y generar los resultados.

Es posible que este pipeline recuerde a un compilador, y eso no es casualidad. Los motores de consulta son, en esencia, #text(fill: ukj-blue)[*compiladores especializados que traducen consultas declarativas en planes de ejecución eficientes*].
   ]
]

#slide[
  == Ejemplo
  Veamos una consulta ligeramente más compleja:

    #toolbox.side-by-side(gutter: 3mm, columns: (1.5fr, 1.5fr), 

  [

    #text(font: "Lato", size : 18pt)[
  ```sql 
SELECT department, AVG(salary)
FROM employees
WHERE hire_date > '2020-01-01'
GROUP BY department
ORDER BY AVG(salary) DESC;

  ```
    ]


  ], 
        [
        #text(font: "Lato", size : 18pt)[

          Esta Consulta: 
          - Escanea la tabla `employee`.
          - Filtra sólo los recién contratados.
          - Agrupa a los empleados por departamento.
          - Calcula el salario promedio por departamento.
          - Ordena los resultados por ese promedio.
          
        ]

      ]

  )

Un query engine #text(fill: ukj-blue)[*debe determinar la forma más eficiente de ejecutar estas operaciones*]. ¿Debe filtrar antes o después de agrupar? ¿Cómo debe almacenar los resultados intermedios? #text(fill: ukj-blue)[*Estas decisiones repercuten significativamente en el rendimiento, especialmente con grandes conjuntos de datos*].
]

#slide[
   #text(font: "Lato", size : 16pt)[
  == SQL: The Universal Query Language
  #text(fill: ukj-blue)[*SQL (Structured Query Language)*] ha sido el lenguaje de consultas dominante desde 1970. Lo podemos encontrar en: 

  - Bases de Datos Relacionales (PostgreSQL, MySQL, SQLite)
  - Data warehouses (Snowflake, BigQuery, Redshift)
  - Sistemas de Big data (Apache Spark, Presto, Hive)
  - Analítica embebida (DuckDB)

Aquí hay dos ejemplos más que muestran la expresividad de SQL:

    #toolbox.side-by-side(gutter: 3mm, columns: (1.5fr, 1.5fr), 

  [

    #text(font: "Lato", size : 12pt)[
#text(font: "Lato", size : 17pt)[Identificación de las 5 páginas más visitadas ayer:]
  ```sql 
SELECT page_url, COUNT(*) AS visits
FROM page_views
WHERE view_date = CURRENT_DATE - 1
GROUP BY page_url
ORDER BY visits DESC
LIMIT 5;

  ```
    ]
  ], 
        [
        #text(font: "Lato", size : 12pt)[

#text(font: "Lato", size : 17pt)[Cálculo del crecimiento mes a mes:]
```sql 
SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS growth
FROM monthly_sales
WHERE year = 2024;
```          
        ]

      ]

  )

   ]
]

#slide[

== Más allá de SQL : DataFrames APIs
    #toolbox.side-by-side(gutter: 3mm, columns: (1.5fr, 1.5fr), 

  [
   #text(font: "Lato", size : 20pt)[
  
  - Si bien SQL es omnipresente, muchos query engines también ofrecen API programáticas. 
  - Estas son especialmente populares en la ciencia de datos, donde las consultas a menudo se construyen de forma dinámica o se combinan con código personalizado.
  - Esta es la misma consulta expresada utilizando la API de DataFrame de Polars en Python:
   ]
    ]
  , 
        [
      #text(font: "Lato", size : 12pt)[
  ```python 
  import polars as pl 

  pl.read_parquet(
        "/data/employees"
      ).filter(
        pl.col("hire_date") > "2020-01-01"
      ).group_by(
        pl.col("department")
      ).agg(
        pl.col("salary").avg().alias("avg_salary")
      ).sort_by(
        "avg_salary", 
        descending = True
      )

  ```

La API de Polars ofrece las mismas operaciones lógicas que SQL, pero expresadas como llamadas a métodos. Internamente, ambos enfoques generan el mismo plan de consulta.
    ]
        ]


  )
]


#slide[
= Polars : Query Engine for DataFrames
  #figure(
        image("images/Polars_logo_1.png", width: 80%),
        numbering: none
      )

]

#slide[
= Polars : Query Engine for DataFrames

#text(font: "Lato", size : 16pt)[
  Polars es una biblioteca desarrollada en Rust que integra las siguientes características por diseño:
  - *Velocidad* : Rust es un lenguaje de system programmig conocido por su desempeño y seguridad.
  - *Paralelismo* : Aprovecha arquitecturas multicore he implementa algoritmos paralelos de work stealing.
  - *Eficiencia de memoria*: 
    - Polars utiliza evaluaciones lazy, lo que significa que una operación no es realizada hasta que esta es necesitada.
    - Las consultas pueden ser encadenadas y optimizadas antes de su ejecución, lo que se traduce en ejecuciones más eficientes de queries.
  - *Almacenamiento eficiente de datos* : Polars utiliza Apache Arrow como modelo de almacenamiento en memoria. Es decir, utiliza un formato columnar del almacenamiento de datos, lo cual resulta más eficiente que el tradicional almacenamiento basado en filas (como el utilizado por Pandas).
  - Diseñado para *out-of-core processing* (más grande que la RAM).
]
]

#slide[
= Polars : Query Engine for DataFrames
  #figure(
        image("images/polars-materialization.png", width: 95%),
        numbering: none
      )

]

#slide[
  == Roadmap de un query 

  #figure(
        image("images/polars-roadmap.svg", width: 110%),
        numbering: none
      )
]


#slide[
  == Paralelismo : Work Stealing
  #figure(
        image("images/stealing.png", width: 55%),
        numbering: none
      )
]


#slide[
  == Polars Expressions

  #text(font: "Lato", size : 26pt)[
  *¿Qué es una expresión?*

  #text(fill: ukj-blue)[*Una expresión es un árbol de operaciones que*] #text(fill: red)[*describen*] cómo construir ona o más Series.

    ]
]

#slide[
= DuckDB : a SQL database that runs everywhere
#v(3cm)
  #figure(
        image("images/DuckDB_Logo-horizontal.png", width: 100%),
        numbering: none
      )

]


#slide[
= DuckDB : a SQL database that runs everywhere

#text(font: "Lato", size : 16pt)[
  - DuckDB es un sistema de bases de datos analíticas de alto rendimiento.
  - Está diseñado para ser rápido, fiable, portable y fácil de usar. 
  - DuckDB ofrece un dialecto SQL completo, con funcionalidades que van mucho más allá del SQL básico.
  - DuckDB está disponible como una #link("https://duckdb.org/docs/current/clients/cli/overview")[aplicación CLI standalone] y clientes para #link("https://duckdb.org/docs/current/clients/python/overview")[Python], #link("https://duckdb.org/docs/current/clients/r")[R], #link(" and has clients for")[Java], etc.
 
]

   #toolbox.side-by-side(gutter: 3mm, columns: (1.5fr, 1.5fr), 

  [
   #text(font: "Lato", size : 14pt)[
  ```sql 
-- Get the top-3 busiest train stations
SELECT
    station_name,
    count(*) AS num_services
FROM train_services
GROUP BY ALL
ORDER BY num_services DESC
LIMIT 3;

  ```
   ]
    ]
  , 
        [
      #text(font: "Lato", size : 14pt)[
  ```python 
# Get the top-3 busiest train stations
import duckdb
duckdb.sql("""
    SELECT station, count(*) AS num_services
    FROM train_services
    GROUP BY ALL
    ORDER BY num_services DESC
    LIMIT 3;
    """)

  ```

    ]
        ]


  )
]

#slide[
= DuckDB : Importación de datos


   #toolbox.side-by-side(gutter: 3mm, columns: (1.5fr, 1.5fr), 

  [
    Lectura de archivos CSVs

   #text(font: "Lato", size : 16pt)[
  ```sql 
-- Load CSV file to a table. DuckDB auto-detects
-- the CSV's format, column name and types
CREATE TABLE stations AS
    FROM 'https://blobs.duckdb.org/stations.csv';
  ```
   ]
    ]
  , 
        [
  Lectura directa de un archivo Parquet sobre HTTPS
      #text(font: "Lato", size : 16pt)[
  ```sql
-- Directly query Parquet file over HTTPS
SELECT
    station_name,
    count(*) AS num_services
FROM 'https://blobs.duckdb.org/train_services.parquet'
GROUP BY ALL
ORDER BY num_services DESC
LIMIT 10;
  ```

    ]
        ]


  )
]