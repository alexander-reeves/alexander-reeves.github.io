---
layout: page
permalink: /repositories/
title: repositories
nav: true
nav_order: 4
---

## GitHub Repositories

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% if site.data.repositories.github_repos %}
    {% for repo in site.data.repositories.github_repos %}
      {% include repository/repo.liquid repository=repo %}
    {% endfor %}
  {% endif %}
  
  {% if site.data.repositories.gitlab_repos %}
    {% for repo in site.data.repositories.gitlab_repos %}
      <div class="repo p-2">
        <a href="{{ repo.url }}">
          <div class="card hoverable">
            <div class="card-body">
              <h5 class="card-title">
                <i class="fa-brands fa-gitlab"></i> {{ repo.name }}
              </h5>
              <p class="card-text">
                {{ repo.description }}
              </p>
              <p class="card-text">
                <small class="text-muted">
                  <i class="fa-solid fa-code-branch"></i> {{ repo.organization }}
                </small>
              </p>
            </div>
          </div>
        </a>
      </div>
    {% endfor %}
  {% endif %}
</div>
