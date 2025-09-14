---
layout: default
permalink: /cv/
title: cv
nav: true
nav_order: 5
cv_pdf: Alex_CV_academic.pdf
description: This is my latest CV as of 14.09.2025. Please get in touch if you would like something more up-to-date.
---

<div class="post">
  <header class="post-header">
    <h1 class="post-title">
      {{ page.title }}
      {% if page.cv_pdf %}
        <a
          href="{{ page.cv_pdf | prepend: 'assets/pdf/' | relative_url}}"
          target="_blank"
          rel="noopener noreferrer"
          class="float-right"
          ><i class="fa-solid fa-file-pdf"></i
        ></a>
      {% endif %}
    </h1>
    {% if page.description %}
      <p class="post-description">{{ page.description }}</p>
    {% endif %}
  </header>

  <article>
    <div class="cv">
      {% if page.cv_pdf %}
        <div class="card mt-3 p-3">
          <h3 class="card-title font-weight-medium">Curriculum Vitae</h3>
          <div>
            <p>Click the PDF icon above to download my CV, or view it below:</p>
            <iframe src="{{ page.cv_pdf | prepend: 'assets/pdf/' | relative_url}}" width="100%" height="800px" style="border: none;"></iframe>
          </div>
        </div>
      {% endif %}
    </div>
  </article>
</div>
