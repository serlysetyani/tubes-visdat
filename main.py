#!/usr/bin/env python
# coding: utf-8

# # <center>Interactive Data Visualization in Python With Bokeh</center>

# ## Adding Interaction

# In[1]:

import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper, Slider, Select, TableColumn, DataTable
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, gridplot, column


# In[2]:


data = pd.read_csv('./data/covid-data.csv')
data['continent'] = data['continent'].astype(str)
data['location'] = data['location'].astype(str)

data['Year'] = pd.to_datetime(data['date']).dt.year


data.set_index('Year', inplace=True)


# In[3]:


regions_list = data.continent.unique().tolist()

color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)


# In[4]:
source = ColumnDataSource(data={
    'x': data.loc[2020].new_deaths_per_million,
    'y': data.loc[2020].total_deaths_per_million,
    'location': data.loc[2020].location,
    'continent': data.loc[2020].continent,
    'date': data.loc[2020].date,
})



# In[ ]:


plot = figure(title='2020', x_axis_label='new_cases', y_axis_label='total_deaths',
              plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@location')])

plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
            color=dict(field='continent', transform=color_mapper), legend='continent')

plot.legend.location = 'bottom_left'



def update_plot(attr, old, new):
    yr = slider.value
    x = x_select.value
    y = y_select.value
    
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y

    new_data = {
        'x': data.loc[yr][x],
        'y': data.loc[yr][y],
        'location': data.loc[yr].location,
        'continent': data.loc[yr].continent,
        'date': data.loc[yr].date,
    }
    source.data = new_data

    plot.title.text = 'Gapminder data for %d' % yr


slider = Slider(start=2020, end=2022, step=1, value=2020, title='Year')
slider.on_change('value', update_plot)

x_select = Select(
    options=['new_cases', 'total_deaths',
             'total_deaths_per_million', 'new_deaths_per_million'],
    value='new_cases',
    title='x-axis data'
)
x_select.on_change('value', update_plot)

y_select = Select(
    options=['new_cases', 'total_deaths',
             'total_deaths_per_million', 'new_deaths_per_million'],
    value='total_deaths',
    title='y-axis data'
)
y_select.on_change('value', update_plot)

columns = [
    TableColumn(field="location", title="Country"),
    TableColumn(field="y", title="Total Deaths"),
    TableColumn(field="date", title="Date"),
]

layout = column(widgetbox(slider, x_select, y_select, plot),
                DataTable(source=source, columns=columns, width=800))

curdoc().add_root(layout)


# In[5]:


# bokeh serve --show myapp.py


# For more on all things interaction in Bokeh, [**Adding Interactions**](https://docs.bokeh.org/en/latest/docs/user_guide/interaction.html) in the Bokeh User Guide is a great place to start.

# In[ ]:
