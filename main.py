
from fastapi import FastAPI
import pandas as pd
app = FastAPI(title='revision  de peliculas y series')

@app.get('/')
async def read_root():
    return {'generacion de  API'}

@app.on_event('startup')
async def startup():
    global df
    uniondf = pd.read_csv('uniondf.csv') 
    
@app.get('/')
async def index():
    return {'API realizada por Lucila Alonso'}

@app.get('/about/')
async def about():
    return {'Proyecto individual Data Science EHDP'}

#función que debe devolver la película o serie con duración máxima de acuerdo a las diferentes plataformas
@app.get('/get_max_duration/({year}, {platform}, {min_o_season})')
async def get_max_duration(anio:int,plataforma:str,min_o_season:str):
    #colocamos dentro de una variable llamada result, el resultado de buscar un año y la plataforma
    result = uniondf[(uniondf['release_year']==anio) & (uniondf['platform']==plataforma)]
    #ahora dentro del if, la función toma en cuenta si se ingresa como parámetro la palabra "min" o "seasons", para ver si se quiere buscar una serie o una película
    if min_o_season == 'min':
    #dentro de a se va guardando en resultado maximo de la columna correspondiente a min, lo cual va llenando una lista para luego devolver la de mayor duración en esa plataforma y en ese año
        a = result['min'].max()
        name = result[result['min']==a] ['title']
        name = name.to_list()
        name = name[0]
    else:
        a = result['seasons'].max()
        #dentro de a se va guardando en resultado maximo de la columna correspondiente a seasons, lo cual va llenando una lista para luego devolver la de mayor duración en esa plataforma y en ese año
        name = result[result['seasons']==a] ['title']
        name = name.to_list()
        name = name[0]
    return name

#función que debe devolver la cantidad de peliculas y tv shows que tienen las diferentes plataformas
@app.get('/get_count_platform/({platform})')
async def get_count_platform(plataforma:str):
    #sumamos las cantidad de películas según la plataforma
    movie =((uniondf['platform']==plataforma) & (uniondf.iloc[:, 1].str.contains('Movie'))).sum()  
    #sumamos la cantidad de series según la plataforma
    tv_show =((df['platform']==plataforma) & (uniondf.iloc[:, 1].str.contains('TV Show'))).sum() 
    return ('Platform: ' + str(plataforma) + ' amount of movies: ' + str(movie) + ' amount of TV Shows: ' +str(tv_show))

#función que debe devolver la cantidad de veces que aparece un género con respecto a alguna plataforma
@app.get('/get_listedin/({genero})')
async def get_listedin(genero:str):
    # se crea una lista llamada plataforma con los elementos únicos de la columna platform
    plataforma = list(uniondf.platform.unique()) 
    #se crea esta lista para ir agregando la cantidad de apariciones de cada actor
    cant_apariciones = list()             
    for elemento in plataforma:    
    #se va ubicando nuestro elemento dentro de la variable df_plataforma
        uniondf_plataforma = uniondf[(uniondf.platform == elemento)] 
        #se crea una columna para los indices de la cantidad de veces que se encuentra el genero buscado 
        uniondf_plataforma['indices'] = uniondf_plataforma.listed_in.str.find(genero) 
        #se adjunta la cantidad de apariciones del género para que se vayan sumando, dentro de la lista cant_apariciones y nos devuelve la de índice 0
        cant_apariciones.append(uniondf_plataforma[uniondf_plataforma.indices != -1].indices.shape[0]) 
    return max(cant_apariciones), plataforma[cant_apariciones.index(max(cant_apariciones))]