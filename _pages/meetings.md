---
layout: page
title: Meetings
permalink: meetings
---

<span style="color: #006EA0; font-style: italic; font-weight: bold;">Our next meeting will be held at {{ site.meeting.location }} on {{ site.meeting.date }} at {{ site.meeting.time }}.</span>

<br>

<div id="archives">
  {% for category in site.categories %}
    {% assign has_meetings_category = false %}
    {% assign has_user_spotlight_category = false %}
    {% for post in category[1] %}
      {% if post.categories contains "Meetings" %}
        {% assign has_meetings_category = true %}
      {% endif %}
      {% if post.categories contains "UserSpotlight" %}
        {% assign has_user_spotlight_category = true %}
      {% endif %}
    {% endfor %}
    
    {% if has_meetings_category or has_user_spotlight_category %}
      <div class="archive-group">
        {% capture category_name %}{{ category | first }}{% endcapture %}
        <div id="#{{ category_name | slugize }}"></div>
        <p></p>
        
        <h3 class="category-head">{{ category_name }}</h3>
        <a name="{{ category_name | slugize }}"></a>
        <ul>
          {% for post in site.categories[category_name] %}
            {% if post.categories contains "Meetings" or post.categories contains "UserSpotlight" %}
              <li><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
            {% endif %}
          {% endfor %}
        </ul>
      </div>
    {% endif %}
  {% endfor %}
</div>