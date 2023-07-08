#from fastapi import, HTTPException FastAPI
from fastapi import FastAPI
from typing import Union
import pandas as pd
import numpy as np
import json
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = FastAPI()


df_1 = pd.read_csv('API1_fucnion1.csv')
df_2 = pd.read_csv('API1_fucnion2.csv')
df_3 = pd.read_csv('API1_fucnion3.csv')
df_4 = pd.read_csv('API1_fucnion4.csv')
df_5 = pd.read_csv('API1_fucnion5.csv')
df_6 = pd.read_csv('API1_fucnion6.csv')
df = pd.read_csv('API1_fucnion7.csv')

#1
@app.get('/peliculas_idioma/{Idioma}')
def peliculas_idioma(Idioma: str):
    if isinstance(Idioma, str):  
        Idioma = Idioma.lower()
        Idioma = unicodedata.normalize('NFKD', Idioma).encode('ascii', 'ignore').decode('utf-8','ignore')  # Eliminar acento
    """Recibe un idioma y devuelve la cantidad de películas producidas en ese idioma(las dos primereas letras en ingles)."""
    peliculas = df_1[df_1['original_language'] == Idioma]

    cantidad = len(peliculas)
    return {'idioma': Idioma, 'cantidad': cantidad}
   
#2
@app.get('/peliculas_duracion/{Pelicula}')
def peliculas_duracion(Pelicula: str):
    """
    Recibe el título de una película y devuelve la duración y el año de lanzamiento.
    """
    Pelicula = unicodedata.normalize('NFKD', Pelicula).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    pelicula = df_2.loc[df_2['title'].str.lower() == Pelicula.lower()]

    if pelicula.empty:
        return "No se encontró la película en el dataset"

    duracion = pelicula['runtime'].values[0]
    año = pelicula['release_year'].values[0]

    return f"{Pelicula}. Duración: {duracion} minutos. Año: {año}"

#3
@app.get('/franquicia/{Franquicia}')
def franquicia(Franquicia: str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
    franquicia = df_3[df_3['belongs_to_collection'].str.lower() == Franquicia.lower()]
    if franquicia.empty:
        return "No se encontró la franquicia en el dataset"
    cantidad_peliculas = franquicia.shape[0]
    ganancia_total = franquicia['revenue'].sum()
    ganancia_promedio = franquicia['revenue'].mean()

    return {'franquicia':franquicia, 'cantidad':cantidad_peliculas, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}




#4
@app.get('/peliculas_pais/{Pais}')
def peliculas_pais(Pais: str):
    Pais = Pais.lower()
    """ Recibe el nombre de un país y devuelve la cantidad de películas producidas en el mismo."""
    df_clean = df_4.dropna(subset=['production_countries'])
    peliculas = df_clean[df_clean['production_countries'].str.contains(Pais, case=False)]
    cantidad_peliculas = len(peliculas)

    return {'pais': Pais, 'cantidad': cantidad_peliculas}


#5
@app.get('/productoras_exitosas/{Productora}')
def productoras_exitosas(Productora:str):
    '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''
    if isinstance(Productora, str):  
        Productora = Productora.lower()
        Productora = unicodedata.normalize('NFKD', Productora).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    peliculas = df[df['production_companies'].str.lower().str.contains(Productora, na=False)]
    revenue_total = peliculas['revenue'].sum()
    cantidad_peliculas = len(peliculas)

    return {'productora':Productora, 'revenue_total': revenue_total,'cantidad':cantidad_peliculas}
    

#6
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    nombre_director = nombre_director.lower()
    nombre_director = unicodedata.normalize('NFKD', nombre_director).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    """  Ingesar  nombre de un director devuelve el éxito del mismo medido a través del retorno. 
    nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma"""
    director_films = df_6[df_6['crew'].str.contains(nombre_director, case=False, regex=False) & ~df_6['crew'].str.contains('director', case=False, regex=False)]

    if director_films.empty:
        return "No se encontró información para el director: {}".format(nombre_director)
    
    cantidad_films = len(director_films)
    retorno_total = director_films['return'].sum()
    exito_director = retorno_total / cantidad_films

    detalles_peliculas = director_films[['title', 'release_date', 'return', 'budget', 'revenue']]
    detalles_peliculas = detalles_peliculas.rename(columns={
        'title': 'Título',
        'release_date': 'Fecha de Lanzamiento',
        'return': 'Retorno',
        'budget': 'Presupuesto',
        'revenue': 'Ganancia'
    })

    return {'director': nombre_director, 'retorno_total_director': exito_director}, detalles_peliculas



# ML


@app.get('/recomendacion/{titulo}')    
def recomendacion(titulo: str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    ml = df.head(10000) 
    ml.reset_index(drop=True, inplace=True)  
    ml.reset_index(inplace=True) 
    ml = ml.dropna(subset=["features"])
    indices = ml[["title", "index"]]  
    tfidf = TfidfVectorizer(stop_words="english", max_features=10000)  
    tfidf_matrix = tfidf.fit_transform(ml["features"])  
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) 
    titulo = titulo.lower().strip()
    titulo = unicodedata.normalize('NFKD', titulo).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    idx = indices[indices["title"] == titulo]
    if idx.empty:
        recommendations = ["Datos no disponibles"]
    else:
        idy = idx["index"].iloc[0]
        sim_scores = list(enumerate(cosine_sim[idy]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        movies_indices = [i[0] for i in sim_scores]
        recommendations = list(ml['title'].iloc[movies_indices].str.title())

    return {'lista_recomendada': recommendations}