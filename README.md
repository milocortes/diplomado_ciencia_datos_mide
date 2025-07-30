# Diplomado en Ciencia de Datos 2025

Repositorio de módulo **Herramientas computacionales para el manejo de datos: Python** del Diplomado de ciencia de datos del MIDE

## Contenido

* [Variables y tipos de datos](notebooks/variables_data_types_mide_2024.ipynb).
* Colecciones:
    - [Listas](notebooks/collections_mide_2024.ipynb)
    - [Tuplas](notebooks/collections_mide_2024.ipynb)
    - [Conjuntos](notebooks/collections_mide_2024.ipynb)
    - [Diccionarios](notebooks/dictionaries_mide_2024.ipynb)
* [Flujos de control](notebooks/control_flow_mide_2024.ipynb):
    - while loop
    - if-elif-else 
    - for loop

* [Compresión de colecciones](notebooks/list_dictionary_comprehensions_mide_2024.ipynb):
    - Compresión de listas.
    - Compresión de diccionarios.
* [Funciones](notebooks/functions_mide_2024.ipynb):
    - Definición de funciones.
    - Funciones lambda.
* [Clases y programación orientada a objetos (OOP)](notebooks/classes_oop_mide_2024.ipynb).
    - Definicion de clases
    - Instancia de variables
    - Métodos: estáticos y de clase
    - Herencia
* [Concurrencia](notebooks/concurrencia_mide_2024.ipynb).
    - Multithreading
    - Multiprocessing
    - Global Interpreter Lock
    - Jerarquía de Memoria y tiempos de acceso
* [Lectura y escritura de archivos](notebooks/reading_writing_files_mide_2024.ipynb)
* Bibliotecas de Ciencia de Datos en Python
    - [Numpy](notebooks/numpy_mide_2024.ipynb)
    - [Pandas](notebooks/pandas_mide_2024.ipynb)
    - [Apache Arrow](notebooks/arrow_mide_2024.ipynb)
    - [Polars](notebooks/polars_mide_2024.ipynb)
* [Acceso a bases de datos ```psycopg2```](notebooks/databases_access_mide_2024.ipynb)

## Descarga del repositorio

Para descargar el repositorio para la rama ```edicion-2025``` utiliza la instrucción:

```
git clone -b edicion-2025 https://github.com/milocortes/diplomado_ciencia_datos_mide.git
```

## Creación del ambiente virtual con uv

Crearemos un ambiente virtual con la instrucción:

```bash 
uv init --python 3.11
```

### Instalación de Jupyter notebook y Marimo
Para la instalación de Jupyter Notebook con uv ejecutamos:

```bash 
uv add notebook
```

Instalamos Marimo con uv:

```bash 
uv add marimo
```


#### Inicio del servicio de Jupyter Notebook

Para iniciar Jupyter Notebook, ejecutamos :

```bash 
uv run --with jupyter jupyter notebook
```

#### Inicio del servicio de Marimo

Para iniciar Marimo, ejecutamos :

```bash 
uv run marimo edit
```


## Recursos adicionales

* [Instalación de miniconda y jupyter notebook.](https://www.youtube.com/watch?v=YBFwFMxKyyc)
* [Algorithms - The Secret Rules of Modern Living - BBC documentary](https://www.youtube.com/watch?v=k2AqGongii0)