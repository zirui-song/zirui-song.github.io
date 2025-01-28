---
layout: archive
#title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
* Ph.D in Accounting, Massachusetts Institute of Technology, 2028 (expected)
* B.S. in Mathematics, Economics (Honors), and Statistics, University of Chicago, 2021

Work experience
======
* 2021-2023: Research Assistant
  * University of Chicago Booth School of Business
  * Supervisors: Professor Christian Leuz and Joao Granja
  
Languages
======
* Python, R, Stata, Matlab, Latex

Papers
======
  <ul>{% for post in site.papers reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
 