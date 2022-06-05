import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import row, column


class DashBoard:
    def __init__(self, pathname):
        self.data = pd.read_excel(pathname, engine='openpyxl')
        self.options = list(self.data['C'].unique())
        self.selected_data = self.data[self.data['C'] == self.options[0]]

        self.source = None
        self.layout = None
        self.plot = None
        self.layout = None
        self.select = None

    def create_layout(self):
        self.make_plot()
        self.make_select()
        self.layout = column(self.select, self.plot)

    def make_plot(self):
        p = figure(plot_height=300, plot_width=1200, toolbar_location='above')
        p.line('x', 'A', source=self.source, legend='Ay', color='red')
        p.circle('x', 'B', source=self.source, legend='By', color='green')
        self.plot = p

    def make_select(self):

        def update(attr, old, new):
            selected_option = self.select.value
            self.selected_data = self.data[self.data['C'] == selected_option]
            newSource = ColumnDataSource(self.selected_data)
            self.source.data = newSource.data

        self.select = Select(title="C", value=self.options[0], options=self.options)
        self.select.on_change('value', update)

    def source_data(self):
        self.source = ColumnDataSource(data=self.selected_data)
