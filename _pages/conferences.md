---
layout: single
title: "Academic Conferences"
permalink: /conferences/
author_profile: true
---

<style>
.conference-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: bold;
  font-size: 0.9em;
}

.filter-select {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
  background-color: white;
}

.conference-section {
  margin-top: 2rem;
}

.conference-section h2 {
  font-size: 1.25em;
  color: #494e52;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

.conference-card {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 1.25rem;
  margin-bottom: 1rem;
  background-color: white;
  transition: box-shadow 0.2s ease;
}

.conference-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.conference-card__header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.conference-card__badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  font-size: 0.75em;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 3px;
}

.conference-card__badge--finance {
  background-color: #e3f2fd;
  color: #1565c0;
}

.conference-card__badge--accounting {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.conference-card__short-name {
  font-size: 0.85em;
  font-weight: bold;
  color: #666;
}

.conference-card__title {
  font-size: 1.1em;
  margin: 0 0 1rem 0;
}

.conference-card__title a {
  color: #1976d2;
  text-decoration: none;
}

.conference-card__title a:hover {
  text-decoration: underline;
}

.conference-card__details {
  font-size: 0.9em;
}

.conference-card__row {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}

.conference-card__row i {
  width: 1rem;
  text-align: center;
  color: #666;
}

.conference-card__deadline--soon {
  color: #f57c00;
  font-weight: bold;
}

.conference-card__deadline--soon .days-remaining {
  background-color: #fff3e0;
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
}

.conference-card__deadline--passed {
  color: #999;
}

.conference-card__deadline--passed .deadline-status {
  color: #d32f2f;
  font-style: italic;
}

.conference-card__notes {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px dashed #e0e0e0;
  font-size: 0.85em;
  color: #666;
  font-style: italic;
}

.conference-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #f0f0f0;
  font-size: 0.8em;
}

.conference-card__source {
  color: #999;
}

.conference-card__cfp-link {
  color: #1976d2;
  font-weight: bold;
}

@media (max-width: 768px) {
  .conference-filters {
    flex-direction: column;
  }
  .conference-card__footer {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
}
</style>

This page tracks upcoming submission deadlines for major Finance and Accounting academic conferences. Use the filters below to find conferences by field or deadline status.

<p style="font-size: 0.85em; color: #666;">
  <i class="fas fa-sync-alt"></i> Last updated: {{ site.data.conferences.metadata.last_updated | date: "%B %d, %Y" }}
</p>

<!-- Filter Controls -->
<div class="conference-filters">
  <div class="filter-group">
    <label for="field-filter">Field:</label>
    <select id="field-filter" class="filter-select">
      <option value="all">All Fields</option>
      <option value="finance">Finance</option>
      <option value="accounting">Accounting</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="status-filter">Status:</label>
    <select id="status-filter" class="filter-select">
      <option value="all">All</option>
      <option value="submissions_open">Submissions Open</option>
      <option value="submissions_closed">Submissions Closed</option>
      <option value="upcoming">Upcoming</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="category-filter">Category:</label>
    <select id="category-filter" class="filter-select">
      <option value="all">All Categories</option>
      <option value="major">Major Conferences</option>
      <option value="regional">Regional</option>
      <option value="specialized">Specialized</option>
    </select>
  </div>
</div>

<!-- Submissions Open Section -->
<div class="conference-section">
  <h2><i class="fas fa-clock"></i> Submissions Open</h2>

  {% assign sorted = site.data.conferences.conferences | sort: "submission_deadline" %}
  {% for conf in sorted %}
    {% if conf.status == "submissions_open" %}
      {% include conference-card.html conference=conf %}
    {% endif %}
  {% endfor %}
</div>

<!-- Upcoming (Submissions Closed or TBD) Section -->
<div class="conference-section">
  <h2><i class="fas fa-calendar"></i> Upcoming Conferences</h2>

  {% for conf in sorted %}
    {% if conf.status == "submissions_closed" or conf.status == "upcoming" %}
      {% include conference-card.html conference=conf %}
    {% endif %}
  {% endfor %}
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const fieldFilter = document.getElementById('field-filter');
  const statusFilter = document.getElementById('status-filter');
  const categoryFilter = document.getElementById('category-filter');
  const cards = document.querySelectorAll('.conference-card');

  function filterCards() {
    const field = fieldFilter.value;
    const status = statusFilter.value;
    const category = categoryFilter.value;

    cards.forEach(card => {
      const cardField = card.dataset.field;
      const cardStatus = card.dataset.status;
      const cardCategory = card.dataset.category;

      const matchField = field === 'all' || cardField === field;
      const matchStatus = status === 'all' || cardStatus === status;
      const matchCategory = category === 'all' || cardCategory === category;

      card.style.display = matchField && matchStatus && matchCategory ? 'block' : 'none';
    });
  }

  fieldFilter.addEventListener('change', filterCards);
  statusFilter.addEventListener('change', filterCards);
  categoryFilter.addEventListener('change', filterCards);
});
</script>
