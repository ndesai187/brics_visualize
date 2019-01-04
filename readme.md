# BRICS visualization based on World Bank Data

### Goal
This utility was created as demo project during my python course at NUS, Singapore. I always had an idea to create such utility. however, I lacked means to do it before.
Python is excellent with large scale data handling. You can still do it in Java, C or any other language. But, you will end up putting lot of efforts in writing code) 
So, here is what tool does:

* Raw data is taken from World Banks open data source.
* You are allowed to choose 5 countries of your choice. (the initial idea was to focus on BRICS nations - but now the tool is generic)
* The utility produces following graphs after processing this data
    1. GDP Statistics
        * GDP per Capita over years (scatter plot)
        * GDP % growth rate over years (scatter plot)
        * Total GDP by country for year 2017 (bubble map)
        * [Click here to see output from utility](http://htmlpreview.github.com/?https://github.com/ndesai187/brics_visualize/blob/master/target/BRICS_visualise_GDP.html)
        
    2. Unemployment vs Public Private Partnership (PPP)
        * Scatter plot with multiple Y axis on left and right
        * [Click here to see output from utility](http://htmlpreview.github.com/?https://github.com/ndesai187/brics_visualize/blob/master/target/BRICS_visualise_PPP.html)
    
    3. GDP vs Neighborhood Fragility Index (NFI)
        * Scatter plot with multiple Y axis on left and right
        * [Click here to see output from utility](http://htmlpreview.github.com/?https://github.com/ndesai187/brics_visualize/blob/master/target/BRICS_visualise_nfi.html)

### Libraries used: numpy, pandas, plotly, matplotlib

### Developed by : Nirav Desai