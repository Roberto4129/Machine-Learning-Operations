from fastapi import FastAPI, HTTPException
from typing import Union
import pandas as pd
import numpy as np
import json
import unicodedata

app = FastAPI()



@app.get('/peliculas_idioma/{Idioma}')
def peliculas_idioma(Idioma:str):
    if isinstance(Idioma, str):  
        Idioma = Idioma.lower()
        Idioma = unicodedata.normalize('NFKD', Idioma).encode('ascii', 'ignore').decode('utf-8','ignore')
    '''Ingresas el idioma(dos primeras letras escrito en ingles), retornando la cantidad de peliculas producidas en el mismo'''
    peliculas = df_1[df_1['original_language'] == Idioma]
    cantidad = len(peliculas)
    
    return {'idioma':Idioma, 'cantidad':cantidad}
   



@app.get('/peliculas_duracion/{Pelicula}')
def peliculas_duracion(Pelicula: str):
    if isinstance(Pelicula, str): 
        Pelicula = Pelicula.lower()
        Pelicula = unicodedata.normalize('NFKD', Pelicula).encode('ascii', 'ignore').decode('utf-8','ignore')
    '''Ingresas la pelicula, retornando la duracion y el año'''
    pelicula = df_2[df_2['title'] == Pelicula]
    if pelicula.empty:
        return "No se encontró la película "
    duracion = pelicula['runtime'].values[0]
    anio = pelicula['release_year'].values[0]

    return {'pelicula':pelicula, 'duracion':duracion, 'Anio':anio}
    

@app.get('/franquicia/{Franquicia}')
def franquicia(Franquicia: str):
    if isinstance(Franquicia, str):  
        Franquicia = Franquicia.lower()
        Franquicia = unicodedata.normalize('NFKD', Franquicia).encode('ascii', 'ignore').decode('utf-8','ignore')
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
    
    franquicia = df_3[df_3['belongs_to_collection'] == Franquicia]
    if franquicia.empty:
        return "No se encontró la franquicia en el dataset"
    cantidad_peliculas = len(franquicia)
    ganancia_total = franquicia['revenue'].sum()
    ganancia_promedio = franquicia['revenue'].mean()

    return {'franquicia':franquicia, 'cantidad':cantidad_peliculas, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}



@app.get('/peliculas_pais/{Pais}')
def peliculas_pais(Pais:str):
    if isinstance(Pais, str):  
        Pais = Pais.lower()
        Pais = unicodedata.normalize('NFKD', Pais).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    """
    Ingresas el pais y devuelve la cantidad de películas producidas en el mismo.
    """
    df_clean = df_4.dropna(subset=['production_countries'])
    peliculas = df_clean[df_clean['production_countries'].str.contains(Pais)]
    cantidad_peliculas = len(peliculas)

    return {'pais':Pais, 'cantidad':cantidad_peliculas}

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
    


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    if isinstance(nombre_director, str):
        nombre_director = nombre_director.lower()
        nombre_director = unicodedata.normalize('NFKD', nombre_director).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        
        director_films = df_6[df_6['crew'].str.contains(nombre_director, case=False) & ~df_6['crew'].str.contains('director', case=False)]

        if director_films.empty:
            return "No se encontró información para el director: {}".format(nombre_director)
        else:
            cantidad_films = director_films.shape[0]
            retorno_total = director_films['return'].sum()
            exito_director = retorno_total / cantidad_films

            detalles_peliculas = director_films[['title', 'release_date', 'return', 'budget', 'revenue']]
            detalles_peliculas = detalles_peliculas.rename(columns={
                'title': 'Título',
                'release_date': 'Fecha de Lanzamiento',
                'return': ' Retorno',
                'budget': 'Presupuesto',
                'revenue': 'Ganancia'
            })
#(" El éxito del mismo medido a través del retorno es de:")
            return {'director':nombre_director, 'retorno_total_director':exito_director}, detalles_peliculas
    else:
        return "El nombre del director debe ser una cadena de texto."



# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    titulo = titulo.lower().strip() 
    titulo = unicodedata.normalize('NFKD', titulo).encode('ascii', 'ignore').decode('utf-8', 'ignore')  
    idx = indices[indices["title"] == titulo]  
    if idx.empty:  
        recommendations = ["Datos no disponible"]
    else:
        idy = idx["index"].iloc[0] 
        sim_score = list(enumerate(cosine_sim[idy]))  
        sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)  
        sim_score = sim_score[1:6]  
        movies_index = [i[0] for i in sim_score]  
        recommendations = list(ml['title'].iloc[movies_index].str.title())  

    return {'lista recomendada': recommendations}
    
    
    


    

