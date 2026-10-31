---
layout: archive
#title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}
{% capture cv_url %}{{ cv_url }}?v={{ site.time | date: '%s' }}{% endcapture %}

<p><a href="{{ cv_url }}">Download CV (PDF)</a></p>

<object data="{{ cv_url }}" type="application/pdf" width="100%" height="1100px">
  <p>Your browser can't display the PDF here. <a href="{{ cv_url }}">Download it instead</a>.</p>
</object>
