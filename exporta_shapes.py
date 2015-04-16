# -*- coding: utf-8 -*-
#Toma los datos de desaparecidos y de rezago nunicipal de los csv's y exporta
# los resultados como shapefiles
#
#
#
##---(Wed Apr 15 18:12:49 2015)---
from geopandas import GeoDataFrame
import pandas as pd
desaparecidos = pd.read_csv('data/desaparecidos.csv',header=0,names=['estado','municipio','cvegeo','year','total','tasa'], encoding='utf-8')
muns_time = desaparecidos.pivot('cvegeo','year','total')
muns_time.head()
rezago_muns = pd.read_csv('data/rezago_municipios.csv')
muns = GeoDataFrame.from_file('data/mexico_mpios_4326.shp',encoding='utf-8')
muns.head()
remove = muns.columns[5:-1]
muns.drop(remove,axis=1,inplace=True)
muns.drop([u'OID'],axis=1,inplace=True)
def f(x):
    return str(x)

cve_str = rezago_muns['cve_mun'].apply(f)
def completa_clave(x):
    if len(x) == 4:
        return '0' + x
    else:
        return x
    
rezago_muns['cve_txt'] = cve_str.apply(completa_clave)
rezago_muns.rename(columns={'cve_txt':'cvegeo'},inplace=True)
muns.rename(columns={'CVEGEO':'cvegeo'},inplace=True)
muns_time.reset_index(inplace=True)
d_c_str = muns_time['cvegeo'].apply(f)
muns_time['cv_txt'] = d_c_str.apply(completa_clave)
muns_geo = muns.merge(rezago_muns,on='cvegeo')
muns_geo_des = muns_geo.merge(muns_time,left_on='cvegeo',right_on='cv_txt',how='inner')
muns_geo_des.head()
muns_geo_des.drop(['NOMBRE','NOM_ENT','cv_txt'],axis=1,inplace=True)
muns_geo_des.head()
muns_geo_des = muns_geo_des.rename(columns={2006:'2006',2007:'2007',2008:'2008',2009:'2009',2010:'2010',2011:'2011',2012:'2012',2013:'2013',2014:'2014'})
muns_geo_des.crs
from fiona.crs import from_epsg
crs = from_epsg(4326)
#muns_geo_des.crs = crs
#muns_geo_des.to_file('data/muns_geo_des.shp')
muns_geo_des = GeoDataFrame(muns_geo_des)
muns_geo_des.crs = crs
#print muns_geo_des.columns
muns_geo_des.drop(['cvegeo_y','analfabeta'],axis=1,inplace=True)
muns_geo_des.rename(columns={'POB1':'poblacion'})
print 'escribiendo archivo...'
muns_geo_des.to_file('data/muns_geo_des.shp',encoding='latin1')