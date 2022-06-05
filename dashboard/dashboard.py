import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column


class DashBoard:
    def __init__(self, pathname):
        self.data = pd.read_excel(pathname, engine='openpyxl')
        self.source = ColumnDataSource(data=self.data)
        self.layout = None
        self.plot = None
        self.layout = None

    def create_layout(self):
        self.make_plot()
        self.layout = row(self.plot)

    def make_plot(self):
        p = figure(plot_height=300, plot_width=1200, toolbar_location='above')
        p.line('x', 'A', source=self.source)
        p.circle('x', 'B', source=self.source)
        self.plot = p
