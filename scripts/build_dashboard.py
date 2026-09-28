"""Render the FIELDNOTES profile from real GitHub snapshots."""
import json, math, re
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET
import os
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
INK='#222622';MUTED='#686b61';CYAN='#c44928';VIOLET='#437161';LINE='#d5d5c8';BG='#f4f2e8';MONO='Consolas,monospace';SANS='Arial,Helvetica,sans-serif'
G=json.loads((ROOT/'data/github.json').read_text());C=json.loads((ROOT/'data/contributions.json').read_text())

def t(x,y,s,size=12,color=INK,font=MONO,extra=''):
 return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" {extra}>{escape(str(s))}</text>'

def frame(w,h,title):
 css='''@keyframes spin{to{transform:rotate(360deg)}}.spin{transform-origin:770px 194px;animation:spin 32s linear infinite}@keyframes in{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}@keyframes hover{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}@keyframes flow{to{stroke-dashoffset:-100}}@keyframes pulse{0%,100%{opacity:.4}50%{opacity:1}}.enter{animation:in .8s ease-out both;animation-delay:var(--d,0s)}.float{animation:hover 6s ease-in-out infinite;animation-delay:var(--d,0s)}.flow{stroke-dasharray:5 12;animation:flow 5s linear infinite}.pulse{animation:pulse 3s ease-in-out infinite}@media(prefers-reduced-motion:reduce){*{animation:none!important}}'''
 if os.environ.get('STATIC')=='1':css+='*{animation:none!important}'
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><style>{css}</style>',f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="2" fill="{BG}" stroke="{LINE}"/>']

def save(p,name): (OUT/name).write_text('\n'.join(p+['</svg>'])+'\n',encoding='utf-8')

def label(p,n,title,w=960):
 p += [t(30,32,n,10,CYAN),t(65,32,title,10,MUTED),f'<path d="M30 47H{w-30}" stroke="{LINE}"/>']

def icon(name,x,y,size=32):
 s=(OUT/'logos'/f'{name}.svg').read_text(encoding='utf-8')
 root=ET.fromstring(s)
 # Keep native logo paths; namespace IDs to avoid gradients colliding.
 s=re.sub(r'<\?xml[^>]*>|<!DOCTYPE[^>]*>','',s).strip()
 s=re.sub(r'<svg\b[^>]*>',f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{root.attrib.get("viewBox","0 0 128 128")}">',s,count=1)
 ids=re.findall(r'\bid="([^"]+)"',s)
 for ident in ids:
  s=s.replace(f'id="{ident}"',f'id="{name}-{ident}"').replace(f'#{ident})',f'#{name}-{ident})').replace(f'"#{ident}"',f'"#{name}-{ident}"')
 if name in ('nextjs','express','flask','mysql','wordpress'):
  return f'<rect x="{x-4}" y="{y-4}" width="{size+8}" height="{size+8}" rx="8" fill="#ffffff"/>'+s
 return s

def hero():
 p=frame(960,500,'FIELDNOTES / Ashif Rza, Fullstack Developer. Animated editorial profile with public GitHub statistics.')
 label(p,'AR','FIELDNOTES / THE WORK OF ASHIF RZA')
 p += [t(930,32,'SOFTWARE / NOTES / EXPERIMENTS',10,MUTED,extra='text-anchor="end"'),t(32,91,'FULLSTACK DEVELOPER',11,CYAN,extra='letter-spacing="2"'),
       '<g class="enter">',t(25,195,'ASHIF',116,INK,SANS,'font-weight="900" letter-spacing="-7"'),t(25,299,'RZA.',116,INK,SANS,'font-weight="900" letter-spacing="-7"'),'</g>',
       t(32,344,'Code, craft & a little curiosity.',27,INK,'Georgia,serif','font-style="italic"'),t(32,378,'React interfaces. Node.js APIs. Applied AI.',13,MUTED),
       '<path d="M586 75V400" stroke="#d5d5c8"/>',
       '<circle cx="770" cy="194" r="115" fill="#e8e7da"/>','<circle cx="770" cy="194" r="87" fill="none" stroke="#d1d2c2"/>',
       '<g class="spin">']
 for a in range(0,360,30):
  p.append(f'<rect x="760" y="101" width="20" height="186" rx="2" fill="#c44928" transform="rotate({a} 770 194)"/>')
 p += ['</g>','<circle cx="770" cy="194" r="31" fill="#f4f2e8"/>',t(770,202,'&lt;/&gt;'.replace('&lt;','<').replace('&gt;','>'),21,INK,extra='text-anchor="middle"'),
       t(770,345,'BUILD / LEARN / REPEAT',11,VIOLET,extra='text-anchor="middle" letter-spacing="1"'),t(770,375,'A practice, not a finish line.',13,MUTED,'Georgia,serif','text-anchor="middle" font-style="italic"'),
       '<path d="M30 412H930" stroke="#d5d5c8"/>']
 for x,num,txt in [(32,G['public_repos'],'PUBLIC REPOS'),(266,C['stats']['total'],'CONTRIBUTIONS'),(505,G['followers'],'FOLLOWERS'),(743,G['stars'],'REPO STARS')]:
  p += [t(x,458,num,32,INK,SANS,'font-weight="bold"'),t(x+81,453,txt,9,MUTED)]
 p.append(t(930,486,'DATA SNAPSHOT / '+G['as_of'],8,MUTED,extra='text-anchor="end"'))
 save(p,'dashboard.svg')

def about():
 p=frame(960,266,'About Ashif: fullstack developer, former frontend intern at Syntechxhub, mathematics graduate. Current focus is HireEdge.')
 label(p,'01','A SHORT INTRODUCTION')
 p += [t(30,102,'I like making',35,INK,'Georgia,serif','font-style="italic"'),t(30,145,'things work.',35,INK,'Georgia,serif','font-style="italic"'),
       t(345,87,'I build responsive interfaces, connect APIs,',17,INK,SANS),t(345,113,'and turn AI ideas into usable web applications.',17,INK,SANS),t(345,145,'Currently building HireEdge, an AI interview-prep platform.',12,MUTED)]
 for x,head,line1,line2 in [(30,'EXPERIENCE','Frontend Intern / Syntechxhub','Nov–Dec 2025'),(345,'FOUNDATION','B.Sc. Mathematics','Ranchi University / 2021–2024'),(666,'NEXT CHAPTER','Open to fullstack roles','Bengaluru + remote')]:
  p += [t(x,189,head,9,CYAN),t(x,216,line1,13,INK,SANS),t(x,240,line2,10,MUTED)]
 save(p,'about.svg')

def stack():
 p=frame(960,310,'Technology stack with original Devicon logos: React, Next.js, TypeScript, JavaScript, Tailwind CSS, Node.js, Express, Python, Flask, MongoDB, MySQL, Git, WordPress, Bootstrap, HTML5, CSS3.')
 label(p,'02','TOOLS OF THE TRADE')
 items=[('react','React'),('nextjs','Next.js'),('typescript','TypeScript'),('javascript','JavaScript'),('tailwindcss','Tailwind'),('nodejs','Node.js'),('express','Express'),('python','Python'),('flask','Flask'),('mongodb','MongoDB'),('mysql','MySQL'),('git','Git'),('wordpress','WordPress'),('bootstrap','Bootstrap'),('html5','HTML5'),('css3','CSS3')]
 for i,(slug,name) in enumerate(items):
  col,row=i%8,i//8;x=30+col*113;y=72+row*112
  p += [f'<g class="enter" style="--d:{i*.035}s">',f'<rect x="{x}" y="{y}" width="105" height="97" rx="2" fill="#ebeadd" stroke="{LINE}"/>',icon(slug,x+36,y+16,32),t(x+52,y+77,name,11,INK,extra='text-anchor="middle"'),'</g>']
 save(p,'stack.svg')

def activity():
 p=frame(960,220,'Public repository language composition by GitHub language bytes, excluding forks and this profile repository. This is code composition, not a proficiency score.')
 label(p,'04','THE CODE / PUBLIC REPOSITORIES')
 langs=G['language_bytes'];total=sum(langs.values()) or 1
 colors=['#c44928','#437161','#c79446','#657483','#a07476','#aaa693']
 p += [t(30,82,'A footprint in code.',24,INK,SANS,'font-weight="bold"'),t(930,79,'SYNC '+G['as_of']+' UTC',9,MUTED,extra='text-anchor="end"')]
 x=30
 for i,(name,count) in enumerate(langs.items()):
  width=900*count/total;p.append(f'<rect x="{x:.2f}" y="108" width="{width:.2f}" height="15" fill="{colors[i%6]}"/>');x+=width
 for i,(name,count) in enumerate(langs.items()):
  x=30+(i%3)*303;y=153+(i//3)*25
  p += [f'<circle cx="{x+3}" cy="{y-4}" r="3" fill="{colors[i%6]}"/>',t(x+15,y,f'{name}  {count/total:.1%}',11,MUTED)]
 p.append(t(30,205,'Language bytes across non-fork public projects; excludes this profile. Not a skill rating.',9,MUTED))
 save(p,'languages.svg')

def repos():
 featured=[('Keystro','AI-powered typing practice.','JavaScript-powered web experience.'),('Clientora','Customer relationship management.','TypeScript for client workflows.'),('Emotion_Detection','Emotion detection with Python.','Computer vision + machine learning.'),('VideoWithAi','A Next.js project.','TypeScript across the application.')]
 byname={r['name']:r for r in G['repos']}
 for i,(name,one,two) in enumerate(featured):
  r=byname.get(name)
  if not r:raise ValueError('Featured repository missing: '+name)
  p=frame(465,215,f"{name}: {one} {r['language']}. {r['stargazers_count']} stars, {r['forks_count']} forks. Updated {r['pushed_at'][:10]}.")
  p += [f'<rect x="1" y="1" width="463" height="6" fill="{CYAN if i%2==0 else VIOLET}"/>','<g class="enter">',t(22,39,f'0{i+1} / SELECTED WORK',9,MUTED),t(440,40,'↗',22,CYAN,extra='text-anchor="end"'),t(22,88,name,26,INK,SANS,'font-weight="bold" letter-spacing="-.7"'),t(22,119,one,14,MUTED,'Georgia,serif','font-style="italic"'),t(22,143,two,11,MUTED),'</g>',f'<path d="M22 166H443" stroke="{LINE}"/>',t(22,192,r['language'] or 'Docs',10,VIOLET),t(169,192,f"STARS {r['stargazers_count']} / FORKS {r['forks_count']}",9,MUTED),t(443,192,r['pushed_at'][:10],9,MUTED,extra='text-anchor="end"')]
  save(p,f'repo-{i+1}.svg')

def arcade():
 p=frame(960,242,'Play Commit Dash. A 45-second runner with keyboard and touch controls. Opens the existing game on a separate page.')
 label(p,'06','A SMALL DISTRACTION')
 p += [t(30,112,'All work? No thanks.',38,INK,'Georgia,serif','font-style="italic"'),t(30,152,'Collect commits. Dodge bugs. Beat your best.',14,MUTED),t(30,213,'COMMIT DASH / 45 SECONDS / KEYBOARD + TOUCH',9,VIOLET),
       '<rect x="631" y="83" width="267" height="86" fill="#222622"/>',t(665,135,'PLAY A ROUND',17,'#f4f2e8',extra='font-weight="bold"'),t(869,138,'↗',29,'#f4f2e8',extra='text-anchor="end"'),
       '<path class="flow" d="M632 196H899" stroke="#c44928" stroke-width="2"/>']
 save(p,'arcade.svg')

if __name__=='__main__':
 hero();about();stack();activity();repos();arcade()
