## `geoMap` python package

The `geoMap` class allows users to visualize the seismic risk profiles of countries and territories around the world. Whether for academic research, business analytics, or educational purposes, `geoMap` provides a platform to enhance the understanding of complex spatial relationships and promote informed decision-making processes. 

### Functions:

#### \_\_init\_\_ Method:
*Use this method to create a geoMap object for mapping.*

Parameters:
  - `code`: Country code for the map (default is 'ALL').
  - `var`: Index of the selected variable (default is 3).
  - `colorscale`: Index of the selected colorscale (default is 0).
  - `countryCenter`: Boolean to specify whether to center the map on the selected country.
  - `showFaults`: Boolean to specify whether to show fault lines on the map.

#### printOptions Method:
*Use this method to see what options are available for customizing your geoMap object.*

Parameters:
  - `data`: String indicating the type of options to print (`'codes'`, `'variables'` or `'colorscales'`).

Prints:
  - List of country codes, variable options, or color scales.

#### map Method:
*Once you have created your geoMap object, call this method to draw a map.*

Parameters:
 - None

Returns:
 - Choropleth map using Plotly Express.


## Example Maps
Hovering over a fault will display the fault's danger level. Hovering over a country will display the country's name, code, and value for the variable of interest.

### 1: World Map (Default)

`code = 'ALL'` (world map)

`var = 3` (countries colored according to variable 3: GDP per capita)

`countryCenter = True` (map is centered on the specified country - in this case, all)

`colorscale = 0` (viridis)

```
gm1 = geoMap()
gm1.map()
```

![World Map - All Countries](https://github.com/sazhu24/geoMap/blob/main/plots/map1.png)


### 2: Japan

`code = 'JPN'` (Japan)

`var = 4` (countries colored according to variable 4: total number of buildings)

`countryCenter = True` (map is centered on the specified country)

`colorscale = 1` (Blues)

```
gm2 = geoMap(code = 'JPN', var = 4, countryCenter = True, colorscale = 1)
gm2.map()
```

![World Map - Selected Country: JAPAN](https://github.com/sazhu24/geoMap/blob/main/plots/map2.png)


### 3: Colombia

`code = 'COL'` (Colombia)

`var = 1` (countries colored according to variable 1: Population Density (Log Scale))

`countryCenter = False` (map is not centered on the specified country)

`colorscale = 2` (Purples)

```
gm3 = geoMap(code = 'COL', var = 1, countryCenter = False, colorscale = 2)
gm3.map()
```

![World Map - Selected Country: COLUMBIA](https://github.com/sazhu24/geoMap/blob/main/plots/map3.png)


### 4: Haiti

`code = 'HTI'` (Haiti)

`var = 3` (countries colored according to variable 3: GDP per Capita)

`countryCenter = True` (map is centered on the specified country)

`colorscale = 0` (viridis)

```
gm4 = geoMap(code = 'HTI', var = 3, colorscale = 0)
gm4.map()
```

![World Map - Selected Country: COLUMBIA](https://github.com/sazhu24/geoMap/blob/main/plots/map4.png)


### 5: Indonesia

`code = 'ALL'` (world map)

`var = 5` (countries colored according to variable 5: Government Effectiveness)

`countryCenter = True` (map is centered on the specified country)

`colorscale = 1` (Blues)

```
gm5 = geoMap(code = 'IDN', var = 5, showFaults = True, colorscale = 1)
gm5.map()
```

![World Map - Selected Country: COLUMBIA](https://github.com/sazhu24/geoMap/blob/main/plots/map5.png)




## Data Sources

  - Fault Lines from the Global Block Model

**Country Variables**

  - Population [(World Bank, 2021)](https://data.worldbank.org/indicator/SP.POP.TOTL)
  - Population Density [(World Bank, 2021)](https://data.worldbank.org/indicator/EN.POP.DNST)
  - GDP [(World Bank, 2021)](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)
  - GDP per Capita [(World Bank, 2021)](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD)
  - Government Effectiveness [(World Bank, 2021)](https://data.worldbank.org/indicator/GE.PER.RNK)
  - Buildings Total [(Yepes-Estrada et al., 2023)](https://github.com/gem/global_exposure_model/blob/main/World/Exposure_Adm0_Summary.csv)


