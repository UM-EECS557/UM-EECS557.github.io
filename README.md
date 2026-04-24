# EECS 557 Communication Networks

This version is meant for the workflow you asked for:

1. edit semester content in `_data/*.yml`
2. run one command to regenerate `index.html`
3. preview locally with any static server or by opening `index.html`

## Files you will usually edit

- `_data/course.yml` — term, description, contact, meeting info
- `_data/navigation.yml` — top links and utility links
- `_data/announcements.yml` — announcements
- `_data/assignments.yml` — project cards and due dates
- `_data/people.yml` — instructor and staff
- `_data/resources.yml` — Canvas, Piazza, Office Hours, calendar, recordings, request forms
- `_data/schedule.yml` — week-by-week schedule and final exam
- `_data/syllabus.yml` — syllabus sections and policies

## Regenerate the page

From the site root, run:

```bash
./build.sh
```

or:

```bash
python3 generate_site.py
```

That rewrites `index.html` from the YAML files.

## Preview locally

Any of these work:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

You can also open `index.html` directly in a browser.

## GitHub Pages

This package is already static, so you can upload it directly to GitHub Pages.
No Jekyll build is required for the generated `index.html`.

## Semester rollover checklist

- update `_data/course.yml`
- replace URLs in `_data/navigation.yml` and `_data/resources.yml`
- update announcements in `_data/announcements.yml`
- update projects in `_data/assignments.yml`
- update staff in `_data/people.yml`
- update lecture/lab/quiz/project dates in `_data/schedule.yml`
- update policies in `_data/syllabus.yml` if needed
- run `./build.sh`
- commit the regenerated `index.html`
