import pandas as pd
from bokeh.io import curdoc, output_notebook, output_file, show
from bokeh.layouts import row, column
from bokeh.models import Select, DataRange1d, HoverTool, ColumnDataSource, PanTool, BoxZoomTool, WheelZoomTool, ResetTool, LassoSelectTool
from bokeh.plotting import figure

output_notebook()
output_file('test.html')

def get_dataset(src, drug_id):
    src.drop('Unnamed: 0', axis = 1, inplace = True)
    df = src.loc[src['ndc'] == int(drug_id)]
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index(['date'])
    df.sort_index(inplace=True)
    source = ColumnDataSource(data=df)
    return source


def make_plot(source, title):
    plot = figure(plot_width=800, plot_height = 800, x_axis_type = 'datetime',
                  toolbar_location='below',
                  tools = [PanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool()])
    plot.xaxis.axis_label = 'Time'
    plot.yaxis.axis_label = 'Price ($)'
    plot.axis.axis_label_text_font_style = 'bold'
    plot.x_range = DataRange1d(range_padding = 0.0)
    plot.grid.grid_line_alpha = 0.3
    plot.title.text = title
    plot.line(x= 'date', y='nadac_per_unit', source=source)
    plot.add_tools(HoverTool(tooltips=[('Date', '@date{%F}'), ('Price', '@nadac_per_unit')],
                                        formatters = {'date': 'datetime'}))

    return plot


def update_plot(attrname, old, new):
    ver = vselect.value
    df1 = df.loc[df['ndc'] == int(new)]
    df1['date'] = pd.to_datetime(df1['date'])
    df1 = df1.set_index(['date'])
    df1.sort_index(inplace=True)
    newSource = ColumnDataSource(df1)
    source.data = newSource.data


df = pd.read_csv('plotting_data.csv')
ver = '54034808' #Initial id number
cc = df['ndc'].astype(str).unique() #select-menu options

vselect = Select(value=ver, title='Drug ID', options=sorted((cc)))

source = get_dataset(df, ver)
plot = make_plot(source, "Drug Prices")

vselect.on_change('value', update_plot)
controls = row(vselect)

curdoc().add_root(row(plot, controls))
show(plot)
