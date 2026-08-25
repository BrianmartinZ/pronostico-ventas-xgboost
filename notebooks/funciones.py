import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

# Creamos una función que se llame to.long() y que reciba como parámetro un dataframe
def to_long(df):

    # Transformamos la tabla de formato ancho a largo utilizando a función melt(id_vars=[columnas fijas] nuevas columnas:var_name, value_name)
    long = df.melt(id_vars=['ProductID','Product_name','Type'], var_name='Año_Mes', value_name='Cantidad')
    long['Fecha'] = pd.to_datetime(long['Año_Mes'], format='%Y-%m') # convertimos Año-Mes en fecha real
    long['Anio'] = long['Fecha'].dt.year # extraemos Año y Mes
    long['Mes'] = long['Fecha'].dt.month
    return long


# Features (lags y medias móviles)
def crear_features(df):
    g = df.groupby('ProductID')
    df['Ventas_Lag_1']  = g['Sales'].shift(1)
    df['Ventas_Lag_3']  = g['Sales'].shift(3)
    df['Ventas_Lag_6']  = g['Sales'].shift(6)
    df['Ventas_Lag_12'] = g['Sales'].shift(12)
    df['Ventas_Rolling_3'] = g['Sales'].transform(lambda x: x.shift(1).rolling(3).mean())
    df['Ventas_Lag_12'] = df['Ventas_Lag_12'].fillna(df['Ventas_Rolling_3'])
    df['Ventas_Lag_6']  = df['Ventas_Lag_6'].fillna(df['Ventas_Lag_1'])
    df['Ventas_Lag_3']  = df['Ventas_Lag_3'].fillna(df['Ventas_Lag_1'])
    return df