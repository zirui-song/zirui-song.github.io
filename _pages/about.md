---
permalink: /
title: "Welcome"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

<style>
.home-section h2 {
  font-size: 1.1em;
  color: #5a7a9b;
  border-bottom: 1px solid #d6e3ed;
  padding-bottom: 6px;
  margin-top: 2em;
  margin-bottom: 1em;
  font-weight: 600;
  letter-spacing: 0.02em;
}
.home-section .paper {
  margin-bottom: 1.4em;
}
.home-section .paper-title {
  font-size: 0.95em;
  font-weight: 600;
  color: #3a3a3a;
  margin: 0;
  line-height: 1.5;
}
.home-section .paper-authors {
  font-size: 0.85em;
  color: #6b6b6b;
  margin: 2px 0 0 0;
  line-height: 1.5;
}
.home-section .paper-authors a {
  color: #6b8fad;
  text-decoration: none;
}
.home-section .paper-authors a:hover {
  text-decoration: underline;
}
.home-section .paper-links {
  font-size: 0.82em;
  margin: 3px 0 0 0;
}
.home-section .paper-links a {
  color: #7a9bb5;
  text-decoration: none;
  margin-right: 10px;
}
.home-section .paper-links a:hover {
  color: #5a7a9b;
  text-decoration: underline;
}
.home-section .paper-presentations {
  font-size: 0.82em;
  color: #7a7a7a;
  margin: 3px 0 0 0;
  line-height: 1.6;
}
.home-section .paper-note {
  font-size: 0.82em;
  color: #9aabba;
  font-style: italic;
  margin: 3px 0 0 0;
}
.home-section .teaching-item {
  font-size: 0.9em;
  color: #4a4a4a;
  margin-bottom: 0.6em;
  line-height: 1.5;
}
.home-section .teaching-detail {
  font-size: 0.82em;
  color: #6b6b6b;
}
.home-section p.intro {
  font-size: 0.92em;
  color: #4a4a4a;
  line-height: 1.7;
}
.home-section .cv-link {
  font-size: 0.88em;
}
.home-section .cv-link a {
  color: #6b8fad;
  text-decoration: none;
}
.home-section .cv-link a:hover {
  color: #5a7a9b;
  text-decoration: underline;
}
</style>

<div class="home-section">

<p class="intro">
Hello! My name is <strong>Zirui Song</strong>. I am a second-year PhD student at <strong>MIT Sloan</strong>. Previously I worked at Chicago Booth after graduating from the University of Chicago with degrees in Mathematics, Economics (Honors), and Statistics.
</p>

<p class="intro">
My research interests are <strong>Banking</strong>, <strong>Debt Contracting</strong>, and <strong>Corporate Finance</strong>.
</p>

<p class="cv-link"><a href="/cv/">Curriculum Vitae</a></p>

<h2>Working Papers</h2>

{% assign working_papers = site.research | where: "category", "working_paper" | sort: "date" | reverse %}
{% for post in working_papers %}
<div class="paper">
  <p class="paper-title">"{{ post.title }}"</p>
  {% if post.authors %}
  <p class="paper-authors">
    {% for author in post.authors %}{% if author.name %}{% if author.url %}<a href="{{ author.url }}">{{ author.name }}</a>{% else %}{{ author.name }}{% endif %}{% else %}{{ author }}{% endif %}{% if forloop.last == false %}, {% endif %}{% endfor %}
  </p>
  {% endif %}
  {% if post.ssrnurl %}
  <p class="paper-links"><a href="{{ post.ssrnurl }}">[SSRN]</a></p>
  {% endif %}
  {% if post.presentations %}
  <p class="paper-presentations">Presented at: {% for pres in post.presentations %}{{ pres.name }}{% if pres.coauthor %}*{% endif %}{% if forloop.last == false %}, {% endif %}{% endfor %}</p>
  {% endif %}
</div>
{% endfor %}

<h2>Work in Progress</h2>

{% assign wip_papers = site.research | where: "category", "wip" | sort: "date" | reverse %}
{% for post in wip_papers %}
<div class="paper">
  <p class="paper-title">"{{ post.title }}"</p>
  {% if post.authors %}
  <p class="paper-authors">
    {% for author in post.authors %}{% if author.name %}{% if author.url %}<a href="{{ author.url }}">{{ author.name }}</a>{% else %}{{ author.name }}{% endif %}{% else %}{{ author }}{% endif %}{% if forloop.last == false %}, {% endif %}{% endfor %}
  </p>
  {% endif %}
  {% if post.ssrnurl %}
  <p class="paper-links"><a href="{{ post.ssrnurl }}">[SSRN]</a></p>
  {% endif %}
  {% if post.presentations %}
  <p class="paper-presentations">Presented at: {% for pres in post.presentations %}{{ pres.name }}{% if pres.coauthor %}*{% endif %}{% if forloop.last == false %}, {% endif %}{% endfor %}</p>
  {% endif %}
</div>
{% endfor %}

<p style="font-size: 0.78em; color: #9aabba; margin-top: 0.5em;">* presented by coauthor</p>

{% assign subsumed_papers = site.research | where: "category", "subsumed" | sort: "date" | reverse %}
{% if subsumed_papers.size > 0 %}
<h2>Subsumed Papers</h2>

{% for post in subsumed_papers %}
<div class="paper">
  <p class="paper-title">"{{ post.title }}"</p>
  {% if post.authors %}
  <p class="paper-authors">
    {% for author in post.authors %}{% if author.name %}{% if author.url %}<a href="{{ author.url }}">{{ author.name }}</a>{% else %}{{ author.name }}{% endif %}{% else %}{{ author }}{% endif %}{% if forloop.last == false %}, {% endif %}{% endfor %}
  </p>
  {% endif %}
  <p class="paper-note">Subsumed by "{{ post.subsumed_by }}"</p>
</div>
{% endfor %}
{% endif %}

<h2>Teaching</h2>

<div class="teaching-item">
  <strong>TA for 15.511 Corporate Financial Accounting (EMBA)</strong><br>
  <span class="teaching-detail">MIT Sloan, Spring 2026 — Professor Nemit Shroff</span>
</div>

<div class="teaching-item">
  <strong>TA for 15.511 Corporate Financial Accounting</strong><br>
  <span class="teaching-detail">MIT Sloan, Summer 2025 — Professor S.P. Kothari</span>
</div>

<div class="teaching-item">
  <strong>TA for 15.511 Corporate Financial Accounting</strong><br>
  <span class="teaching-detail">MIT Sloan, Summer 2024 — Professor S.P. Kothari</span>
</div>

</div>
