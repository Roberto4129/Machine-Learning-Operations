# HENRY’S LABS

PROYECTOINDIVIDUAL 01 DATA 12 --Machine Learning Operations


Este proyecto tiene como objetivo desarrollar un sistema de recomendación de películas mediante el ciclo de vida completo de un proyecto de Machine Learning, desde la transformación y limpieza de los datos hasta la implementación de una API para su consumo.

## Descripción del problema (Contexto y rol a desarrollar)
### Contexto
En el contexto de una start-up que provee servicios de agregación de plataformas de streaming, se requiere desarrollar un sistema de recomendación de películas.

### Rol a desarrollar
El rol a desempeñar es el de MLOps Engineer, encargado de llevar el modelo de recomendación al mundo real. El objetivo es crear un modelo de recomendación funcional, partiendo desde cero en cuanto a la calidad y madurez de los datos.

## Propuesta de trabajo (requerimientos de aprobación)
### Transformaciones de datos
- Se realizarán las siguientes transformaciones a los datos:
  - Desanidar los campos anidados como `belongs_to_collection` y `production_companies`.
  - Rellenar los valores nulos de los campos `revenue` y `budget` con el número 0.
  - Eliminar los valores nulos del campo `release_date`.
  - Formatear las fechas en el formato AAAA-mm-dd y extraer el año en una nueva columna llamada `release_year`.
  - Crear una columna llamada `return` que contenga el retorno de inversión calculado como la división de `revenue` entre `budget`, y rellenar con 0 cuando no hay datos disponibles.
  - Eliminar las columnas no utilizadas: `video`, `imdb_id`, `adult`, `original_title`, `poster_path` y `homepage`.

### Desarrollo de la API
Se implementará una API utilizando el framework FastAPI. Se crearán 6 funciones para los endpoints que se consumirán en la API:

1. `peliculas_idioma(Idioma: str)`: Devuelve la cantidad de películas producidas en el idioma especificado.
2. `peliculas_duracion(Pelicula: str)`: Devuelve la duración y el año de una película especificada.
3. `franquicia(Franquicia: str)`: Devuelve la cantidad de películas, ganancia total y ganancia promedio de una franquicia especificada.
4. `peliculas_pais(Pais: str)`: Devuelve la cantidad de películas producidas en el país especificado.
5. `productoras_exitosas(Productora: str)`: Devuelve el revenue total y la cantidad de películas realizadas por una productora especificada.
6. `get_director(nombre_director)`: Devuelve el éxito de un director medido a través del retorno, junto con el nombre, fecha de lanzamiento, retorno individual, costo y ganancia de cada película en formato de lista.

### Deployment
La API será desplegada en Render , para que pueda ser consumida desde la web.

### Análisis exploratorio de los datos (EDA)
Se realizará un análisis exploratorio de los datos para investigar las relaciones entre las variables, identificar outliers o anomalías, y descubrir patrones interesantes que puedan ser útiles en un análisis posterior. Se recomienda utilizar técnicas como nubes de palabras para identificar las palabras más frecuentes en los títulos de las películas, lo cual podría ser útil para el sistema de recomendación.

## Conclusiones
En este proyecto individual, se ha abordado el desarrollo de un sistema de recomendación de películas desde el rol de un MLOps Engineer. Se han aplicado transformaciones a los datos, se ha implementado una API utilizando FastAPI, se ha realizado un análisis exploratorio de los datos y se ha propuesto su despliegue en un entorno de producción. Este proyecto ha permitido poner en práctica los conocimientos y habilidades relacionados con el ciclo de vida completo de un proyecto de Machine Learning y el rol de un MLOps Engineer.
