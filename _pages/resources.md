---
layout: page
permalink: /resources/
---

# Utah Specific Resources
 - [Volume Traffic Map](https://unifiedplan.org/traffic-volume-map/) - This app shows traffic volume forecasts on Utah's highways and major roads.
 - [Household and Job Viewer](https://unifiedplan.org/utah-household-job-forecast-map/) - This app shows the distribution of population, households, and employment by major sector, annually through 2050.
 - [Model One-Pagers & Documentation](Model one-pagers and documentation) - This page contains one-pagers and documentation for the all of Utah's travel demand models.
 - [2023 Utah Household Travel Survey Resources](https://unifiedplan.org/household-travel-surveys/)

<br>

----------------------------------------------

# General Resources

### Travel Demand Model Practices
 - [Travel Forecasting Resource](https://tfresource.org) - a collection of best practices for travel demand forecasting and travel survey methods.
 - [Introduction to Urban Travel Demand Forecasting](https://libraryarchives.metro.net/dpgtl/usdot/1977-an-introduction-to-urban-travel-demand-forecasting-a-self-instructional-text.pdf) - relevant self-instructional text on principles of travel demand forecasting
 - [NCHRP Report 716- Travel Demand Forecasting: Parameters and Techniques](https://transportation.ky.gov/Planning/Documents/Travel%20Demand%20Forecasting.pdf)
 - [Travel Model Validation and Reasonableness Checking Manual](https://www.fhwa.dot.gov/planning/tmip/publications/other_reports/validation_and_reasonableness_2010/fhwahep10042.pdf)
 - [Ohio DOT CUBE Highway Network Coding Refresher](https://transportation.ohio.gov/static/Programs/StatewidePlanning/Modeling-Forecasting/Highway_Training%202016.ppt )

### Travel Surveys
 - [2023 Utah Household Travel Survey Resources](https://unifiedplan.org/household-travel-surveys/)
 - [National Household Travel Survey](https://nhts.ornl.gov/)

### Socioeconomic Data and Trends
 - [Kem C. Garner Policy Institute Demographics](https://gardner.utah.edu/demographics/) - Utah demographic estimates and population projections
 - [Population Data housed at Texas A&M](https://trerc.tamu.edu/data/population/) - easy interface for pulling County, MSA, and State historical data for anywhere in the country
 - [Employment (Bureau of Labor Statistics) Data housed at Texas A&M](https://trerc.tamu.edu/data/employment-bls/) - easy interface for pulling County, MSA, and State historical data for anywhere in the country
 - [Household and Job Viewer](https://unifiedplan.org/utah-household-job-forecast-map/) - This app shows the distribution of population, households, and employment by major sector, annually through 2050.

<br>

----------------------------------------------

# Blog Posts
<div id="archives">
  {% for category in site.categories %}
    {% unless category[0] == "Meetings" or category[0] == "UserSpotlight" %}
      <div class="archive-group">
        {% capture category_name %}{{ category | first }}{% endcapture %}
        <div id="#{{ category_name | slugize }}"></div>
        <p></p>
        
        <h4 class="category-head">{{ category_name }}</h4>
        <a name="{{ category_name | slugize }}"></a>
        <ul>
          {% for post in site.categories[category_name] %}
            <li><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
          {% endfor %}
        </ul>
      </div>
    {% endunless %}
  {% endfor %}
</div>