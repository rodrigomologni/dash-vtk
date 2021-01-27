import dash
import dash_vtk
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import numpy as np
import pyvista as pv
from pyvista import examples

# Get point cloud data from PyVista
dataset = examples.download_lidar()
subset = 0.5
selection = np.random.randint(low=0, high=dataset.n_points-1,
                              size=int(dataset.n_points * subset))
points = dataset.points[selection]
xyz = points.ravel()
elevation = points[:, -1].ravel()
min_elevation = np.amin(elevation)
max_elevation = np.amax(elevation)
print(f'Number of points: {points.shape}')
print(f'Elevation range: [{min_elevation}, {max_elevation}]')

# Setup VTK rendering of PointCloud
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

vtk_view = dash_vtk.View(
    [
        dash_vtk.PointCloudRepresentation(
            xyz=xyz,
            scalars=elevation,
            colorDataRange=[min_elevation, max_elevation],
            property={ 'pointSize': 2 },
        )
    ]
)

app.layout = dbc.Container(
    fluid=True,
    children=[
        html.H1("Demo of dash_vtk.PointCloudRepresentation"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    width=12,
                    children=[
                        html.Div(
                            vtk_view,
                            style={"height": "calc(80vh - 20px)", "width": "100%"},
                        )
                    ],
                ),
            ]
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
