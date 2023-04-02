import plotly.graph_objects as go

def crear_velocimetro(value,valor_minimo,valor_maximo,variable,suffix="%"):

    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = value,
        mode = "gauge+number",
        number = {'suffix': suffix},
        gauge = {
        'axis': {'range': [valor_minimo, valor_maximo],'tickvals' :[valor_minimo,valor_maximo], 'tickwidth': 1, 'tickcolor': "#bad6db"},
        'bar': {'color': "#051f34" },
        'bgcolor': "#01a9c1",
        'borderwidth': 2,
        'bordercolor': "#bad6db",
          }))
    fig.update_layout(font = {'size' : 35, 'color': "#051f34", 'family': "Arial"},
        annotations=[
            {
                'text': variable,
                'x': 0.5,
                'y': -0.2,
                'xanchor': "center",
                'yanchor': "bottom",
                'showarrow': False,
                'font' : {
                    'size' : 40,
                    'color' : "#051f34"
                }
            }]
            )
    fig.update_traces(gauge_axis_showticklabels = True, gauge_axis_ticks = "")
    fig.write_image("./static/graficos/{}.png".format(variable))

    return fig

