
# import packages
import pandas as pd
import matplotlib as mpl
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError as e:
    print("please install the 'plotly' module to use geoMap")
try:
    from IPython.display import display, HTML
except ImportError as e:
    IPython = False
    print(e)

# define class
class geoMap:

    ## read in data
    # this csv contains lat and lon points for fault lines
    # note: this data set is a cleaned version of 'ordered_rectangles.csv.' it was reformatted to work with the plotly express line.geo function
    world_fts = pd.read_csv("/Users/sara/Desktop/SDS 271/final project/SDS271-G5-Package/data/faults_lines_danger.csv")
    # this csv countains geometry and descriptive data for all countries
    all_countries = pd.read_csv('/Users/sara/Desktop/SDS 271/final project/SDS271-G5-Package/data/countries_geo_clean.csv')  

    # create list of colorscale options
    colorscale_options = ['viridis_r', 'Blues', 'Purples']
    # create list of variable options
    variable_options = ['POPULATION', 'POP. DENSITY (LOG)', 'GDP (USD)', 'GDP PER CAPITA', 'BUILDINGS TOTAL', 'GOV. EFFECTIVENESS']
    # create dictionary of variables with definitions
    var_dict = {
        "POPULATION": '\n     Definition: Total Population \n     Source: (World Bank, 2021) \n', 
        "POP. DENSITY (LOG)": '\n     Definition: Population per sq. kilometer of land area (on a log scale) \n     Source: (World Bank, 2021) \n',
        "GDP USD": '\n     Definition: GDP in 2021 US Dollars \n     Source: (World Bank, 2021) \n', 
        'GDP PER CAPITA': '\n     Definition: GDP (2021 US$) per Population \n     Source: (World Bank, 2021) \n',
        'BUILDINGS TOTAL': '\n     Definition: Total Number of Buildings \n     Source: (Yepes-Estrada et al., 2023) \n',
        'GOV. EFFECTIVENESS' : """\n     Definition: The Government Effectiveness measure captures perceptions of the quality of public services, 
        \t\t the quality of the civil service and the degree of its independence from political pressures, 
        \t\t the quality of policy formulation and implementation, and the credibility of the government's commitment to such policies. \n     Source: (World Bank, 2021) """
    }

    # initialize parameters
    def __init__(self, code = 'ALL', var = 3, colorscale = 0, countryCenter = True, showFaults = True, faultColors = ['#FAD1BB', '#E5A785', '#CF7C50', '#BA521A']):
        # df sets the data frame used to generate a map
        self.df = geoMap.all_countries
        # faultLines determines which fault lines to use
        self.faultLines = self.world_fts
        # code stores the country that will be mapped, default is 'ALL'
        self.code = code
        # var stores the selected variable 
        self.var = self.variable_options[var]
        # colorscale stores the colorscale (function) used in the map, default is viridis
        self.colorscale = mpl.colormaps.get_cmap(self.colorscale_options[colorscale]) 
        # colorscale name (string)
        self.colorscale_name = self.colorscale_options[colorscale]
        # country_center specifies whether or not to center the map on the selected country
        self.country_center = countryCenter
        # showFaults specifies whether or not to center the map on the selected country
        self.showFaults = showFaults
        # set color pallete for fault levels (light orange to dark orange)
        self.fault_colors = faultColors
        
    
    # method to get color for country based on relative position in the color scale (only used when a new trace is added to highlight a country)
    # method called in map1 method
    def rgb2hex(self, value):
        norm = self.colorscale(value)
        rgba = {"r": norm[0], "g": norm[1], "b": norm[2]}
        r = int(rgba['r'] * 255)
        g = int(rgba['g'] * 255)
        b = int(rgba['b'] * 255)
        return f'#{r:02x}{g:02x}{b:02x}'
    

    # method prints list of options for parameters: code, variable, style
    # method is called by user
    def printOptions(self, data):
        if(data == 'codes'):
            print("COUNTRY CODES")
            # select columns for country name and country code
            df = self.df[['COUNTRY', 'ISO3']].rename(columns = {'ISO3': 'CODE'})
            # set pandas DataFrame option to display all rows
            pd.set_option("display.max_rows", None) 
            # adds scrollbar next to the DataFrame
            display(HTML("<div style = 'height: 200px; overflow: auto; width: fit-content'>" +
                         df.style.to_html() + "</div>"))

        elif(data == 'variables'):
            print("VARIABLE DEFINITIONS \n")
            for key, value in self.var_dict.items():
                index = list(self.var_dict.keys()).index(key)
                print(' ' + str(index) + ': ' + key + value)
        
        elif(data == 'colorscales'):
            for i in range(len(self.colorscale_options)):
                print(' ' + str(i) + ': ' + str(self.colorscale_options[i]))
    

    # method sets zoom and center coordinates for a specific country
    def settings(self):
        if(self.code == 'ALL'):
            self.country_name = 'All Countries'
            self.zoom = 1
            self.center_lon = 0
            self.center_lat = 0
        elif(self.code != 'ALL'):
            self.index = list(self.df['ISO3']).index(self.code)
            self.country_name = self.df['COUNTRY'][self.index]
            self.zoom = 1
            self.center_lon = 0
            self.center_lat = 0
            if(self.country_center):
                self.zoom = self.df['zoom'][self.index]
                self.center_lon = self.df['center_lon'][self.index]
                self.center_lat = self.df['center_lat'][self.index]

    # map method: creates a world map
    # method is called by user
    def map(self):
        
        # call settings method to initialize values for zoom, center_lat, center_lon, country_name
        geoMap.settings(self)
        
        if(self.var == 'GDP PER CAPITA'):
            # set colorscalerange
            # set max threshold at the 95th percentile to exclude very large outliers
            range = [min(self.df[self.var]), self.df[self.var].quantile(.95)]
        else:
            range = [min(self.df[self.var]), self.df[self.var].quantile(1)]

        self.df['CODE'] = self.df['ISO3']
        # create chloropleth map
        fig = px.choropleth(
            # set df
            self.df, 
            # set location column
            locations = 'ISO3', 
            # set color column 
            color = self.df[self.var], 
            # set colorscale
            color_continuous_scale = self.colorscale_name,
            # set range for colorscale
            range_color = range,
            # set hover text
            hover_name = 'COUNTRY',
            hover_data = {'ISO3': False, 'CODE': True},
            # set map projection
            projection = 'natural earth', 
            # set map title
            title = self.var + ' - ' + self.country_name
            )

        # if showFaults = True, add a new trace with fault lines
        if(self.showFaults):

            fault_layer = px.line_geo(
                self.faultLines,
                lat = 'lat',
                lon = 'lon',
                # map colors to danger column
                color = 'danger',
                # set order for categories
                category_orders = {'danger': ['low', 'medium', 'high', 'very high']},
                # set color sequence
                color_discrete_sequence = self.fault_colors,
                # add hover data
                hover_data = {'lat': False, 'lon': False, 'danger': True}
                )
            
            # add each layer to a new map trace
            fig.add_trace( fault_layer.data[0] )   
            fig.add_trace( fault_layer.data[1] )   
            fig.add_trace( fault_layer.data[2] )  
            fig.add_trace( fault_layer.data[3] )  
            
            # add annotation to create a legend title
            fig.add_annotation(
                # add label
                text = "FAULT DANGER LEVEL",
                # remove arrow
                showarrow = False,
                # set y position
                yanchor = 'top', y = 1.02,
                # set x position
                xanchor = 'right', x = 1.037
                )

        # if a single country is selected, add a new trace with outlined country only
        if(self.code != 'ALL'):
            
            # create a new df with selected country only
            country_df = self.df[self.df['ISO3'] == self.code].reset_index(drop = True)

            ## get color for country
            # normalize the variable column and compute the country's rank value between 0-1 (i.e. country is the Xth percentile of all countries)
            self.color_var_norm = mpl.colors.Normalize(vmin = min(self.df[self.var]), vmax = self.df[self.var].quantile(.95))
            # call rgb2hex method to get the right hexcode for the country
            self.country_color = str(geoMap.rgb2hex(self, self.color_var_norm(float(country_df[self.var]))))

            ## create hover label for country
            # get country name
            trace_name = country_df.loc[0, 'COUNTRY']
            # create variable label 
            country_df['text'] = self.var + ': ' + country_df[self.var].round(2).astype(str)
            
            # add new trace to map with this country only
            fig2 = go.Figure(data = go.Choropleth(
                    # set location
                    locations = country_df['ISO3'],
                    # set color value to 0 to use custom color value
                    z = [0],
                    # use country_color to color the country (otherwise the outlined country is shaded white)
                    colorscale = [[0, self.country_color], [1, self.country_color]],
                    # add border outline
                    marker_line_color = '#fa1616',
                    marker_opacity = 1,
                    marker_line_width = 3,
                    # remove legend
                    showscale = False,
                    # set text for hover data
                    name = trace_name,
                    text = country_df['text']
                ))
            
            # add trace to map
            fig.add_trace(
                fig2.data[0]
            )


        # update map layout
        fig.update_layout(
            # set fig margin
            margin = {'l':0,'t':60,'b':40,'r':0},
            # set fig height and width
            height = 540,
            width = 1200,
            # set title positioning
            title_x = 0.48,
            title_y = 0.955,
            # set title font
            title_font = dict(family = 'Jost', size = 23, color = 'black'),
            # set legend position and lengend title font
            legend = dict(
                yanchor = 'top', y = 0.98,
                xanchor = 'right', x = 1,
                font = dict(size = 14, family = 'Jost')
            ),
            # set zoom and center coordinates
            geo = {
                'projection_scale' : self.zoom,
                'center': {'lat': self.center_lat, 'lon': self.center_lon}
                }
            )
        
        # update layout for legend title
        fig.update_annotations(
            font = dict(size = 14, family = 'Jost')
            )

        # update layout for colorbar
        fig.update_coloraxes(
            colorbar = dict(title = self.var),
            colorbar_tickfont = dict(size = 14, family = 'Jost'),
            colorbar_title = dict(font = dict(size = 14, family = 'Jost')),
            colorbar_len = 0.78,
            colorbar_y = 0.37, 
            colorbar_x = 0.87, 
            colorbar_xpad = 50
            )
        
        # show map fig
        return fig.show()
