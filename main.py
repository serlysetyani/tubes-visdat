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


listRegion = data.continent.unique().tolist()
mapColor = CategoricalColorMapper(factors=listRegion, palette=Spectral6)


# In[4]:
source = ColumnDataSource(data={
    'x': data.loc[2020].new_deaths_per_million,
    'y': data.loc[2020].total_deaths_per_million,
    'location': data.loc[2020].location,
    'continent': data.loc[2020].continent,
    'date': data.loc[2020].date,
})



# In[ ]:


plot = figure(title='Persebaran Data COVID 19 di Seluruh Dunia', x_axis_label='New Cases', y_axis_label='Total Deaths',
              plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@location')])

plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
            color=dict(field='continent', transform=mapColor), legend='continent')

plot.legend.location = 'bottom_left'



def updatePlot(attr, old, new):
    year = slider.value
    x = selectX.value
    y = selectY.value
    
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y

    newData = {
        'x': data.loc[year][x],
        'y': data.loc[year][y],
        'location': data.loc[year].location,
        'continent': data.loc[year].continent,
        'date': data.loc[year].date,
    }
    source.data = newData

    plot.title.text = 'Gapminder data for %d' % year


slider = Slider(start=2020, end=2022, step=1, value=2020, title='Year')
slider.on_change('value', updatePlot)

selectX = Select(
    options=['New Cases', 'Total Deaths',
             'Total Deaths (Per Million)', 'New Deaths (Per Million)'],
    value='New Cases',
    title='Select X'
)
selectX.on_change('value', updatePlot)

selectY = Select(
    options=['New Cases', 'Total Deaths',
             'Total Deaths (Per Million)', 'New Deaths (Per Million)'],
    value='Total Deaths',
    title='Select Y'
)
selectY.on_change('value', updatePlot) 

columns = [
    TableColumn(field="location", title="Country"),
    TableColumn(field="y", title="Total Deaths"),
    TableColumn(field="date", title="Date"),
]

layout = column(widgetbox(slider, selectX, selectY, plot),
                DataTable(source=source, columns=columns, width=800))

curdoc().add_root(layout)


# In[5]:


# bokeh serve --show myapp.py


# For more on all things interaction in Bokeh, [**Adding Interactions**](https://docs.bokeh.org/en/latest/docs/user_guide/interaction.html) in the Bokeh User Guide is a great place to start.

# In[ ]:
