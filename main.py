from bokeh.models import ColumnDataSource, Legend, CustomJS, Select
from bokeh.plotting import figure
from bokeh.palettes import Category10
from bokeh.layouts import row, column
import pandas as pd
from bokeh.server.server import Server

from dashboard import dashboard

PATHNAME = "Test.xlsx"


def bkapp(doc):
    df0 = pd.read_excel("Test.xlsx", engine='openpyxl')
    source = ColumnDataSource(data=df0)

    tools_to_show = 'box_zoom,save,hover,reset'
    plot = figure(plot_height=300, plot_width=1200,
                  toolbar_location='above',
                  tools=tools_to_show)

    plot.line('x', 'A', source=source)
    plot.line('x', 'B', source=source)

    def update(attr, old, new):
        df1 = df0[df0['C'] == select.value]
        newSource = ColumnDataSource(df1)
        source.data = newSource.data

    options = list(df0['C'].unique())
    select = Select(title="C", value=options[0], options=options)
    select.on_change('value', update)

    doc.add_root(column(select, plot))


def test(doc):
    # df0 = pd.DataFrame({'x': [1, 2, 3], 'Ay': [1, 5, 3], 'A': [0.2, 0.1, 0.2], 'By': [2, 4, 3], 'B': [0.1, 0.3, 0.2]})
    df0 = pd.read_excel("Test.xlsx", engine='openpyxl')

    tools_to_show = 'box_zoom,save,hover,reset'
    p = figure(plot_height=300, plot_width=1200,
               toolbar_location='above',
               tools=tools_to_show)

    legend_it = []
    color = Category10[10]
    columns = ['A', 'B']
    source = ColumnDataSource(df0)
    c = []
    for i, col in enumerate(columns):
        c.append(p.line('x', col, source=source, name=col, color=color[i]))
        legend_it.append((col, [c[i]]))

    legend = Legend(items=legend_it, location=(5, 114))  # (0, -60))

    p.add_layout(legend, 'right')

    select = Select(title="color", value=color[0],
                    options=color)
    callbacks = CustomJS(args=dict(renderer=c[0], select=select), code="""
        renderer.glyph.line_color = select.value;
        renderer.trigger('change')
    """)

    select.callback = callbacks

    layout = row(select, p)

    doc.add_root(layout)


def modify_doc(doc):
    dash = dashboard.DashBoard(PATHNAME)
    dash.create_layout()
    doc.add_root(dash.layout)


# server = Server({'/': test}, num_procs=1)
# server = Server({'/': bkapp}, num_procs=1)
server = Server({'/': modify_doc})
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
