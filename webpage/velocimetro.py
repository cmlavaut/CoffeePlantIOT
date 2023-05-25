import plotly.graph_objects as go

def crear_velocimetro(valor, max_valor,variable, suffix="%"):
    figura = go.Figure()

    figura.add_trace(go.Indicator(
        mode = "gauge+number",
        value = valor,
        number = {'suffix': suffix},
        title = {'text': "{}".format(variable)},
        gauge = {
            'axis': {'range': [0, max_valor]},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "blue",
        }
    ))

    figura.update_layout(font = {'size' : 40, 'color': "blue", 'family': "Arial"},
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

    figura.update_layout(height=300, width=400)
    figura.show()
    figura.write_image("./static/graficos/{}.png".format(variable))

    return figura


