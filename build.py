"""Build a dependency-free GitHub Pages website from content.json."""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent
d = json.loads((ROOT / 'content.json').read_text())
BASE = 'https://yunfanch.github.io'


def nav(home=False):
    prefix = '' if home else 'index.html'
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><a class="wordmark" href="index.html" aria-label="Yunfan Chen home">Yunfan Chen<span class="wordmark-dot">.</span></a>
<nav aria-label="Main navigation"><a href="{prefix}#research">Research</a><a href="{prefix}#publications">Publications</a><a href="cv.html"{' aria-current="page"' if not home else ''}>CV</a><a class="nav-contact" href="{prefix}#contact">Get in touch <span aria-hidden="true">↗</span></a></nav></header>'''


def footer():
    return f'''<footer class="site-footer"><span>© 2026 Yunfan Chen</span><span>Ann Arbor, Michigan · Updated {e(d['updated'])}</span><a href="{d['github']}/yunfanch.github.io">Website source <span aria-hidden="true">↗</span></a></footer>'''


def shell(title, description, content, path='', home=False):
    structured = {'@context':'https://schema.org', '@type':'Person', 'name':d['name'], 'url':BASE+'/', 'image':BASE+'/'+d['photo'], 'jobTitle':'Ph.D. Candidate', 'affiliation':{'@type':'CollegeOrUniversity','name':d['institution']},'sameAs':[d['orcid'],d['github'],d['university_url']]}
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#153e46">
<link rel="canonical" href="{BASE}/{path}"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{BASE}/{path}"><meta property="og:image" content="{BASE}/{d['photo']}"><meta name="twitter:card" content="summary">
<link rel="stylesheet" href="assets/styles.css"><script src="assets/site.js" defer></script><script type="application/ld+json">{json.dumps(structured)}</script></head>
<body>{nav(home)}{content}{footer()}</body></html>'''


def author_text(p):
    return e(p['authors']).replace('Chen, Y.', '<strong>Chen, Y.</strong>')


def pub_html(p, cv=False):
    issue = f"({e(p['issue'])})" if p.get('issue') else ''
    return f'''<article class="publication" data-author="{'first' if p['first_author'] else 'co'}">
<div class="pub-year">{p['year']}</div><div><h3><a href="https://doi.org/{p['doi']}">{e(p['title'])}</a></h3>
<p class="authors">{author_text(p)}</p><p class="journal"><em>{e(p['journal'])}</em>, {p['volume']}{issue}, {e(p['pages'])}.</p>
<div class="pub-links"><a href="https://doi.org/{p['doi']}">Paper <span aria-hidden="true">↗</span></a><a href="assets/citations/{p['id']}.bib" download>BibTeX <span aria-hidden="true">↓</span></a>{'' if cv else '<details><summary>Overview</summary><p>'+e(p['summary'])+'</p></details>'}</div></div></article>'''


projects = ''
for i, p in enumerate(d['projects'], 1):
    if i == 1:
        projects += '<div class="research-stage" id="doctoral-research"><p class="eyebrow">University of Michigan / 2023–present</p><h3>Doctoral research</h3><p>Earth and Environmental Sciences · Advisor: Julia Cole</p></div>'
    if p.get('stage') == 'masters' and (i == 1 or d['projects'][i-2].get('stage') != 'masters'):
        projects += '<div class="research-stage" id="masters-research"><p class="eyebrow">Chinese Academy of Sciences / September 2020–June 2023</p><h3>Master’s research</h3><p>Research Assistant, State Key Laboratory of Tropical Oceanography<br>South China Sea Institute of Oceanology, Chinese Academy of Sciences · Advisor: Yan Du</p></div>'
    links = ''.join(f'<a class="text-link" href="{l["url"]}">{e(l["label"])} <span aria-hidden="true">↗</span></a>' for l in p['links'])
    projects += f'''<article class="research-row" id="{p['id']}"><div class="research-label"><span class="project-number">0{i}</span><p class="eyebrow">{e(p['category'])}</p></div><div class="research-body"><h4>{e(p['title'])}</h4><p class="research-question">{e(p['question'])}</p><p>{e(p['description'])}</p><p class="method-line">{e(p['methods'])}</p><div class="research-end"><span class="status">{e(p['status'])}</span>{links}</div></div></article>'''

education = ''.join(f'<div class="education-row"><span class="date">{e(x["date"])}</span><div><h3>{e(x["degree"])}</h3><p>{e(x["school"])}</p><p class="muted">{e(x["detail"])}</p></div></div>' for x in d['education'])
awards = ''.join(f'<li><span class="date">{e(x["date"])}</span><div><strong>{e(x["title"])}</strong><p>{e(x["institution"])}</p></div></li>' for x in d['awards'])
manuscript = f'''<aside class="manuscript"><p class="eyebrow">Manuscript under review</p><h3>{e(d['manuscript']['title'])}</h3><p class="authors">{author_text(d['manuscript'])}</p><p class="muted">{e(d['manuscript']['status'])}</p><a class="text-link" href="https://github.com/yunfanch/WIO-SST-Reconstruction">Associated reconstruction code <span aria-hidden="true">↗</span></a><a class="text-link all-manuscripts" href="cv.html#manuscripts">All manuscripts &amp; work in progress <span aria-hidden="true">↗</span></a></aside>'''

home = f'''<main id="main">
<section class="hero section-wrap" aria-labelledby="name"><div class="hero-copy"><p class="eyebrow">{e(d['institution'])} / Earth &amp; Environmental Sciences</p><h1 id="name">Yunfan Chen<span class="accent">.</span></h1><p class="role">{e(d['role'])}</p><h2 class="hero-statement">Reading the ocean’s past.<br>Understanding a changing climate.</h2><p class="intro">{e(d['intro'])}</p><div class="hero-actions"><a class="button primary" href="#research">Explore my research <span aria-hidden="true">↓</span></a><a class="button secondary" href="cv.html">View academic CV <span aria-hidden="true">↗</span></a></div><div class="profile-links"><a href="mailto:{d['email']}">Email</a><span aria-hidden="true">/</span><a href="{d['orcid']}">ORCID</a><span aria-hidden="true">/</span><a href="{d['github']}">GitHub</a><span aria-hidden="true">/</span><a href="{d['university_url']}">U-M profile</a></div></div>
<figure class="portrait"><div class="portrait-frame"><img src="{d['photo']}" alt="Portrait of Yunfan Chen" width="3341" height="5012" fetchpriority="high"></div><figcaption><span class="small-caps">Based in</span>Ann Arbor, Michigan</figcaption><div class="photo-caption-rule" aria-hidden="true"></div></figure></section>
<div class="opportunity-strip section-wrap"><span class="availability-dot" aria-hidden="true"></span><p>{e(d['availability'])}</p><a href="mailto:{d['email']}?subject=Research%20opportunity">Let’s connect <span aria-hidden="true">↗</span></a></div>
<section id="research" class="section-wrap section-block" aria-labelledby="research-heading"><div class="section-heading"><div><p class="eyebrow">01 / Research</p><h2 id="research-heading">From coral archives<br>to climate dynamics.</h2></div><p>I connect evidence from the past with experiments in climate models to understand the mechanisms behind tropical climate variability.</p></div><nav class="research-jump" aria-label="Research stages"><a href="#doctoral-research">Doctoral research <span>3 projects ↓</span></a><a href="#masters-research">Master’s research <span>3 projects ↓</span></a></nav>{projects}</section>
<section class="approach-band"><div class="section-wrap approach-grid"><div><p class="eyebrow">Research approach</p><h2>Different evidence.<br>A connected picture.</h2></div><ol class="approach-list"><li><span>01</span><div><h3>Recover the record</h3><p>Use coral isotope and trace-element archives to extend the view beyond instrumental observations.</p></div></li><li><span>02</span><div><h3>Test the reconstruction</h3><p>Compare statistical methods and evaluate reconstructions against independent observations.</p></div></li><li><span>03</span><div><h3>Understand the mechanism</h3><p>Bring proxy evidence, reanalysis, and model ensembles together to investigate ocean–atmosphere processes.</p></div></li></ol></div></section>
<section id="publications" class="section-wrap section-block" aria-labelledby="publications-heading"><div class="section-heading"><div><p class="eyebrow">02 / Publications</p><h2 id="publications-heading">Selected publications.</h2></div><a class="text-link" href="{d['orcid']}">My ORCID record <span aria-hidden="true">↗</span></a></div><div class="publication-filters" role="group" aria-label="Filter publications" hidden><button class="filter active" data-filter="all" aria-pressed="true">All papers <span>{len(d['publications'])}</span></button><button class="filter" data-filter="first" aria-pressed="false">First author <span>{sum(p['first_author'] for p in d['publications'])}</span></button><button class="filter" data-filter="co" aria-pressed="false">Coauthored <span>{sum(not p['first_author'] for p in d['publications'])}</span></button></div><p id="publication-count" class="sr-only" aria-live="polite"></p><div id="publication-list">{''.join(pub_html(p) for p in d['publications'])}</div>{manuscript}</section>
<section id="about" class="background-section"><div class="section-wrap background-grid"><div><p class="eyebrow">03 / Background</p><h2>Training &amp;<br>recognition.</h2><p class="background-intro">My training spans physical oceanography, paleoclimatology, and climate modeling. At Michigan, I work with Professor Julia Cole.</p><a class="text-link" href="cv.html">View my academic CV <span aria-hidden="true">↗</span></a></div><div><h3 class="subsection-label">Education</h3>{education}<h3 class="subsection-label awards-label">Selected honors</h3><ul class="awards-list">{awards}</ul></div></div></section>
<section id="contact" class="section-wrap contact-section"><p class="eyebrow">04 / What’s next</p><div class="contact-grid"><div><h2>Let’s explore<br>the next questions.</h2><p>I’m interested in how external forcing, background climate conditions, and inter-basin interactions shape Indo-Pacific variability and its hydroclimate impacts.</p><p>I welcome conversations about postdoctoral and research opportunities, fellowships, and collaborations that bring paleoclimate evidence and climate dynamics together.</p></div><div class="contact-card"><span class="small-caps">Get in touch</span><a class="email-link" href="mailto:{d['email']}">{d['email']} <span aria-hidden="true">↗</span></a><p>Ph.D. expected May 2027<br>University of Michigan · Ann Arbor</p><a class="button primary" href="mailto:{d['email']}?subject=Postdoctoral%20or%20research%20opportunity">Start a conversation <span aria-hidden="true">↗</span></a></div></div></section></main>'''

def record_rows(records):
    return ''.join(f'<div class="education-row"><span class="date">{e(x["date"])}</span><div><h3>{e(x["title"])}</h3><p>{e(x.get("institution", ""))}</p><p>{e(x.get("description", ""))}</p></div></div>' for x in records)


def manuscript_rows(records):
    return ''.join(f'<article class="cv-manuscript"><h3>{e(x["title"])}</h3><p class="authors">{author_text(x)}</p><p class="muted">{e(x["status"])}</p></article>' for x in records)


cv = f'''<main id="main" class="section-wrap cv-page"><div class="cv-top"><div><p class="eyebrow">Academic record / {e(d['updated'])}</p><h1>Curriculum vitae.</h1><p class="cv-name">Yunfan Chen</p><p>Ph.D. Candidate, Earth and Environmental Sciences<br>University of Michigan · Ann Arbor, Michigan<br><a href="mailto:{d['email']}">{d['email']}</a> · <a href="{d['orcid']}">ORCID</a> · <a href="{d['github']}">GitHub</a></p></div><button class="button primary print-button" hidden>Print / save as PDF <span aria-hidden="true">↓</span></button></div>
<div class="cv-opportunity">{e(d['availability'])}</div>
<section class="cv-section"><h2>Research interests</h2><p>Climate variability; tropical climate dynamics; ocean–atmosphere interactions; paleoclimate proxies; coral paleoclimatology; climate modeling.</p></section>
<section class="cv-section"><h2>Education</h2>{education}<h3 class="cv-subheading">Certificates &amp; additional training</h3>{record_rows(d['training'])}</section>
<section class="cv-section"><h2>Peer-reviewed publications</h2>{''.join(pub_html(p, True) for p in d['publications'])}</section>
<section id="manuscripts" class="cv-section"><h2>Manuscripts under review</h2>{manuscript_rows(d['manuscripts_under_review'])}<h3 class="cv-subheading">Manuscripts in preparation</h3>{manuscript_rows(d['manuscripts_in_preparation'])}</section>
<section class="cv-section"><h2>Research experience</h2>{record_rows(d['research_experience'])}</section>
<section class="cv-section"><h2>Teaching experience</h2>{record_rows(d['teaching'])}</section>
<section class="cv-section"><h2>Selected conference presentations</h2>{record_rows(d['conferences'])}</section>
<section class="cv-section"><h2>Laboratory &amp; fieldwork experience</h2>{record_rows(d['lab_and_field'])}</section>
<section class="cv-section"><h2>Fellowships &amp; funding</h2>{record_rows(d['fellowships'])}</section>
<section class="cv-section"><h2>Honors &amp; awards</h2>{record_rows(d['honors'])}</section>
<section class="cv-section"><h2>Methods &amp; technical skills</h2><dl class="skills">{''.join('<dt>'+e(k)+'</dt><dd>'+e(v)+'</dd>' for k,v in d['skills'].items())}</dl></section>
<section class="cv-section"><h2>Patents &amp; inventions</h2>{record_rows(d['patents'])}</section>
<section class="cv-section"><h2>Open research software</h2><h3><a href="https://github.com/yunfanch/WIO-SST-Reconstruction">WIO-SST-Reconstruction</a></h3><p>MATLAB code for multi-method reconstruction of western Indian Ocean sea surface temperature from coral geochemical proxies, with independent calibration and verification.</p></section></main>'''

(ROOT / 'index.html').write_text(shell('Yunfan Chen | Coral Paleoclimate & Climate Dynamics', 'Yunfan Chen is a Ph.D. candidate at the University of Michigan studying Indo-Pacific climate variability through coral records and climate models.', home, home=True))
(ROOT / 'cv.html').write_text(shell('Academic CV | Yunfan Chen', 'Academic CV: publications, education, research, teaching, fellowships, and technical skills of Yunfan Chen, University of Michigan.', cv, 'cv.html'))
(ROOT / '404.html').write_text(shell('Page not found | Yunfan Chen', 'Return to Yunfan Chen’s academic website.', '<main id="main" class="section-wrap error-page"><p class="eyebrow">404 / Page not found</p><h1>Back to familiar waters.</h1><p>This page may have moved.</p><a class="button primary" href="/">Return to the homepage ↗</a></main>', '404.html'))
for p in d['publications']:
    authors = p['authors'].replace(', & ', ' and ').replace('., ', '. and ')
    fields = {'title':'{'+p['title']+'}', 'author':authors, 'journal':p['journal'], 'year':str(p['year']), 'volume':p['volume'], 'pages':p['pages'].replace('–','--'), 'doi':p['doi']}
    if p.get('issue'): fields['number'] = p['issue']
    bib = '@article{' + p['id'] + ',\n' + ',\n'.join('  '+k+' = {'+v+'}' for k,v in fields.items()) + '\n}\n'
    (ROOT / 'assets' / 'citations' / (p['id']+'.bib')).write_text(bib)
(ROOT / '.nojekyll').touch()
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+'/'+p+'</loc></url>' for p in ['', 'cv.html'])+'</urlset>\n')
print(f"Built index.html, cv.html, 404.html and {len(d['publications'])} BibTeX citations.")
