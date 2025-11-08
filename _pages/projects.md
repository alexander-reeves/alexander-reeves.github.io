---
layout: page
permalink: /projects/
title: Projects
description: Overview of my main research themes and ongoing projects.
---

<div class="row row-cols-1 row-cols-md-2">
  {% assign projects = site.projects %}
  {% for project in projects %}
    {% include projects.liquid %}
  {% endfor %}
</div>


