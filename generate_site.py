#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from datetime import datetime
import copy
import yaml
import mistune
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "_data"
TEMPLATES = ROOT / "templates"
OUTPUT = ROOT / "index.html"

md = mistune.create_markdown(escape=False)

def load_yaml(name: str):
    with open(DATA / name, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def initials(name: str) -> str:
    parts = [p for p in name.split() if p]
    return ''.join(p[0] for p in parts[:2]).upper()

def fmt_date(date_text: str) -> str:
    if not date_text:
        return ''
    try:
        return datetime.strptime(date_text, '%Y-%m-%d').strftime('%a %b %d').replace(' 0', ' ')
    except ValueError:
        return date_text

def md_html(text: str | None) -> str:
    return md(text or '')

def prepare_syllabus(syllabus: dict) -> dict:
    s = copy.deepcopy(syllabus)
    s['intro_html'] = md_html(s.get('intro_markdown', ''))
    for sec in s.get('sections', []):
        sec['markdown_html'] = md_html(sec.get('markdown', '')) if sec.get('markdown') else ''
        sec['bullet_items_html'] = [md_html(item).removeprefix('<p>').removesuffix('</p>\n').removesuffix('</p>') for item in sec.get('bullet_items', [])]
        sec['grade_scale_intro_html'] = md_html(sec.get('grade_scale_intro', '')) if sec.get('grade_scale_intro') else ''
        for sub in sec.get('subsections', []) or []:
            sub['markdown_html'] = md_html(sub.get('markdown', ''))
    return s

def prepare_people(people: dict) -> dict:
    out = copy.deepcopy(people)
    for group in ['faculty', 'staff']:
        for p in out.get(group, []):
            p['initials'] = initials(p.get('name', ''))
    return out

def prepare_schedule(schedule: dict) -> dict:
    out = copy.deepcopy(schedule)
    for week in out.get('weeks', []):
        for entry in week.get('entries', []):
            entry['date_display'] = fmt_date(entry.get('date', ''))
    return out

def prepare_announcements(ann: dict) -> list[dict]:
    items = ann.get('items', []) or []
    active = [a for a in items if a.get('active')]
    return active if active else items[:0]

def main() -> None:
    course = load_yaml('course.yml')
    nav = load_yaml('navigation.yml')
    resources = load_yaml('resources.yml')
    ann = load_yaml('announcements.yml')
    assignments = load_yaml('assignments.yml')
    people = prepare_people(load_yaml('people.yml'))
    schedule = prepare_schedule(load_yaml('schedule.yml'))
    syllabus = prepare_syllabus(load_yaml('syllabus.yml'))

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('index.html.j2')
    html = template.render(
        course=course,
        nav=nav,
        resources=resources,
        active_announcements=prepare_announcements(ann),
        assignments=assignments,
        people=people,
        schedule=schedule,
        syllabus=syllabus,
    )
    OUTPUT.write_text(html, encoding='utf-8')
    print(f'Wrote {OUTPUT}')

if __name__ == '__main__':
    main()
