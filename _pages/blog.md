---
layout: page
permalink: /blog/
title: blog
description: Some random thoughts about things I like.
nav: false
nav_order: 1
---

<div class="post">
  <header class="post-header">
    <h1 class="post-title">{{ site.blog_name }}</h1>
    <p class="post-description">{{ site.blog_description }}</p>
  </header>

  <article>
    <div class="news">
      {% assign posts_size = site.posts | size %}
      {% if posts_size > 0 %}
        <div class="table-responsive">
          <table class="table table-sm table-borderless">
            {% assign posts = site.posts | sort: "date" | reverse %}
            {% for post in posts %}
              <tr>
                <th scope="row" style="width: 20%">{{ post.date | date: '%b %d, %Y' }}</th>
                <td>
                  {% if post.redirect == blank %}
                    <a class="news-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
                  {% elsif post.redirect contains '://' %}
                    <a class="news-title" href="{{ post.redirect }}" target="_blank">{{ post.title }}</a>
                    <svg width="2rem" height="2rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
                      <path
                        d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9"
                        class="icon_svg-stroke"
                        stroke="#999"
                        stroke-width="1.5"
                        fill="none"
                        fill-rule="evenodd"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      ></path>
                    </svg>
                  {% else %}
                    <a class="news-title" href="{{ post.redirect | relative_url }}">{{ post.title }}</a>
                  {% endif %}
                  {% if post.description %}
                    <br>
                    <span class="text-muted">{{ post.description }}</span>
                  {% endif %}
                </td>
              </tr>
            {% endfor %}
          </table>
        </div>
      {% else %}
        <p>No posts so far...</p>
      {% endif %}
    </div>
  </article>
</div>

