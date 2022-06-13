#!/usr/bin/env python
# coding: utf-8

# # <center>Interactive Data Visualization in Python With Bokeh</center>

# ## Adding Interaction

# In[1]:

import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select


# In[2]:


data = pd.read_csv('./data/covid-data.csv')
data['continent'] = data['continent'].astype(str)
data['location'] = data['location'].astype(str)

data['Year'] = pd.to_datetime(data['date']).dt.year


data.set_index('Year', inplace=True)


# In[3]:


# Make a list of the unique values from the region column: regions_list
regions_list = data.continent.unique().tolist()

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)


# In[4]:
source = ColumnDataSource(data={
    'x': data.loc[2020].new_deaths_per_million,
    'y': data.loc[2020].total_deaths_per_million,
    'location': data.loc[2020].location,
    'continent': data.loc[2020].continent,
})

# Make the ColumnDataSource: source


# In[ ]:


# Create the figure: plot
plot = figure(title='2020', x_axis_label='new_deaths_per_million', y_axis_label='total_deaths_per_million',
              plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@location')])

# Add a circle glyph to the figure p
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
            color=dict(field='continent', transform=color_mapper), legend='continent')

# Set the legend and axis attributes
plot.legend.location = 'bottom_left'

# Define the callback function: update_plot


def update_plot(attr, old, new):
    # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # new data
    # new_data = {
    # 'x'       : data.loc[yr][x],
    # 'y'       : data.loc[yr][y],
    # 'country' : data.loc[yr].Country,
    # 'pop'     : (data.loc[yr].population / 20000000) + 2,
    # 'region'  : data.loc[yr].region,
    # }
    new_data = {
        'x': data.loc[yr][x],
        'y': data.loc[yr][y],
        'location': data.loc[yr].location,
        'continent': data.loc[yr].continent,
    }
    source.data = new_data

    # Add title to figure: plot.title.text
    plot.title.text = 'Gapminder data for %d' % yr


# Make a slider object: slider
slider = Slider(start=2020, end=2022, step=1, value=2020, title='Year')
slider.on_change('value', update_plot)

# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['new_cases', 'total_deaths',
             'total_deaths_per_million', 'new_deaths_per_million'],
    value='new_cases',
    title='x-axis data'
)
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['new_cases', 'total_deaths',
             'total_deaths_per_million', 'new_deaths_per_million'],
    value='total_deaths',
    title='y-axis data'
)
# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)

# Create layout and add to current document
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)


# In[5]:


# bokeh serve --show myapp.py


# For more on all things interaction in Bokeh, [**Adding Interactions**](https://docs.bokeh.org/en/latest/docs/user_guide/interaction.html) in the Bokeh User Guide is a great place to start.

# In[ ]:
