---
layout: page
permalink: /projects/
title: projects
description: Overview of my main research themes and ongoing projects.
nav: true
nav_order: 3
---

<div class="row row-cols-1 row-cols-md-2">
  {% assign projects = site.projects | sort: "importance" %}
  {% for project in projects %}
    {% include projects.liquid %}
  {% endfor %}
</div>


