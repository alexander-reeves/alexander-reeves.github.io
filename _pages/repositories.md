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
      <div class="repo">
        <a href="{{ repo.url }}" target="_blank">
          <div class="card hoverable">
            <div class="card-body">
              <h3 class="card-title text-lowercase">
                <i class="fa-brands fa-gitlab"></i> {{ repo.name }}
              </h3>
              <p class="card-text">{{ repo.description }}</p>
              <div class="row ml-1 mr-1 p-0">
                <div class="col-sm-12 p-0">
                  <div class="repo-meta-data">
                    <p class="meta-row">
                      <span class="meta-info mr-2">
                        <i class="fa-solid fa-code-branch"></i>
                        <span class="text-muted">{{ repo.organization }}</span>
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </a>
      </div>
    {% endfor %}
  {% endif %}
</div>
