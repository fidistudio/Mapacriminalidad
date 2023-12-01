import dash
from dash import dcc, html 
import pandas as pd
import plotly.express as px

# Cargar los datos
df = pd.read_csv('carpetasFGJ_2023.csv')  # Asegúrate de que el nombre del archivo sea correcto

# Filtrar para asegurar que todas las filas tengan coordenadas
df = df.dropna(subset=['latitud', 'longitud'])

# Obtener las opciones únicas de la columna "categoría"
opciones_categorias = [{'label': cat, 'value': cat} for cat in df['categoria'].unique()]

# Crear la figura inicial del mapa de calor
fig = px.density_mapbox(df, lat='latitud', lon='longitud', 
                        radius=10, 
                        center={"lat": 19.36, "lon": -99.133209},  # Centro en la Ciudad de México
                        zoom=10, 
                        mapbox_style="mapbox://styles/mapbox/light-v10")  # Puedes cambiar el estilo del mapa aquí

fig.update_layout(mapbox_accesstoken='pk.eyJ1IjoiZmlkaW1hcGJveCIsImEiOiJjbHBsZm52c2cwMXl0MmxvNnkzeTdqOHRqIn0.n7wc9LyNMPFGf5V03Vt8mg')

# Iniciar la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1("Mapa de Calor de Criminalidad en la Ciudad de México", className='h1'),

    # Agregar un Dropdown para elegir la categoría
    dcc.Dropdown(
        id='dropdown-categoria',
        options=opciones_categorias, 
        value=opciones_categorias[0]['value'],  # Valor inicial
        className='dropdown',
        style={'width': '50%'}  # Ancho del dropdown
    ),

    # Agregar el gráfico (sin especificar 'figure')
    dcc.Graph(id='mapa-criminalidad', className='graph')
], className='body')

# Definir la función para actualizar el gráfico en función de la opción seleccionada
@app.callback(
    dash.dependencies.Output('mapa-criminalidad', 'figure'), 
    [dash.dependencies.Input('dropdown-categoria', 'value')]
)
def actualizar_mapa(categoria_seleccionada):
    # Filtrar el DataFrame por la categoría seleccionada
    df_filtrado = df[df['categoria'] == categoria_seleccionada]

    # Asegurarse de que haya datos después del filtrado
    if df_filtrado.empty:
        return px.scatter_mapbox()

    # Obtener el centro y zoom basado en los datos filtrados
    center_lat = df_filtrado['latitud'].mean()
    center_lon = df_filtrado['longitud'].mean()
    zoom = 12  # Puedes ajustar esto según tus necesidades

    # Crear la nueva figura actualizada del mapa de calor 
    nueva_figura = px.density_mapbox(df_filtrado, lat='latitud', lon='longitud', 
                                      radius=10, 
                                      center={"lat": center_lat, "lon": center_lon},
                                      zoom=zoom,
                                      mapbox_style="mapbox://styles/mapbox/light-v10")  # Puedes cambiar el estilo del mapa aquí
    
    return nueva_figura

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
