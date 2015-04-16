# -*- coding: utf-8 -*-
#Toma los datos de desaparecidos y de rezago nunicipal de los csv's y exporta
# los resultados como shapefiles
#
#
#
##---(Wed Apr 15 18:12:49 2015)---
from geopandas import GeoDataFrame
import pandas as pd
from fiona.crs import from_epsg
#Leemos los desaparecidos, los acomodamos y los unimos al shape de estados.
desaparecidos = pd.read_csv('data/desaparecidos.csv',header=0,names=['estado','municipio','cvegeo','year','total','tasa'], encoding='utf-8')
tmp = desaparecidos.groupby(['estado','year']).sum().reset_index('year').reset_index('estado')
estado_tiempo = tmp.pivot(index='estado',columns='year',values='total')
estado_tiempo = estado_tiempo.reset_index('estado')
gf = GeoDataFrame.from_file('data/estados.shp', encoding='utf-8')
gf.rename(columns = {'NOMBRE':'estado'},inplace=True)
des_estado = pd.merge(gf,estado_tiempo, on='estado')

#Ahora leemos los datos de rezago, ajustamos la clave y los unimos a los datos de arriba:
rezago = pd.read_csv('data/rezago_estados.csv')
def f(x):
    return str(x)
    
cve_str = rezago['cvegeo'].apply(f)
def completa_clave(x):
    if len(x) == 1:
        return '0' + x
    else:
        return x
        
rezago['cvegeo'] = cve_str.apply(completa_clave)
des_estado.rename(columns={'CVEGEO':'cvegeo'},inplace=True)
final = des_estado.merge(rezago,on='cvegeo')
final.drop('nombre',axis=1,inplace=True)

#renombrtamos las columnas de años para que sean texto:
final = final.rename(columns={2006:'2006',2007:'2007',2008:'2008',2009:'2009',2010:'2010',2011:'2011',2012:'2012',2013:'2013',2014:'2014'})

#Damos valor a la proyección y exportamos:
final = GeoDataFrame(final)
crs = from_epsg(4326)
final.crs = crs
final.to_file('data/des_rezago_estado.shp')