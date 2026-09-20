---
layout: page
permalink: /repositories/
title: code
description: Research code I have written or contributed to.
nav: true
nav_order: 5
---

Most of my work ends up as code. These are the pieces that are public and usable by someone other than me — the rest lives on [GitHub](https://github.com/alexander-reeves).

<div class="repo-grid">
  {% for repo in site.data.repositories.repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>
