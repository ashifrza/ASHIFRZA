"""Render the CODE / PLAY profile dashboard from real GitHub snapshots."""
import json, math, re
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET
import os
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
INK='#edf5ff';MUTED='#98abc6';CYAN='#62e7ff';VIOLET='#af98ff';LINE='#263650';BG='#0a1120';MONO='Consolas,monospace';SANS='Arial,Helvetica,sans-serif'
G=json.loads((ROOT/'data/github.json').read_text());C=json.loads((ROOT/'data/contributions.json').read_text())

def t(x,y,s,size=12,color=INK,font=MONO,extra=''):
 return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" {extra}>{escape(str(s))}</text>'

def frame(w,h,title):
 css='''@keyframes in{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}@keyframes hover{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}@keyframes flow{to{stroke-dashoffset:-100}}@keyframes pulse{0%,100%{opacity:.4}50%{opacity:1}}.enter{animation:in .8s ease-out both;animation-delay:var(--d,0s)}.float{animation:hover 6s ease-in-out infinite;animation-delay:var(--d,0s)}.flow{stroke-dasharray:5 12;animation:flow 5s linear infinite}.pulse{animation:pulse 3s ease-in-out infinite}@media(prefers-reduced-motion:reduce){*{animation:none!important}}'''
 if os.environ.get('STATIC')=='1':css+='*{animation:none!important}'
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><style>{css}</style>',f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="{BG}" stroke="{LINE}"/>']

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
  return f'<rect x="{x-4}" y="{y-4}" width="{size+8}" height="{size+8}" rx="8" fill="#e9f2ff"/>'+s
 return s

def hero():
 p=frame(960,480,'ASHIF RZA / Fullstack developer. React, Node.js and AI. Currently building HireEdge. No portrait; animated isometric software layers.')
 label(p,'AR','DEVELOPER WORKSPACE / ASHIF RZA')
 p += [t(930,32,'CODE  /  BUILD  /  PLAY',10,CYAN,extra='text-anchor="end"'),t(30,94,'FULLSTACK DEVELOPER',12,CYAN,extra='letter-spacing="2"'),'<g class="enter">',t(26,170,'ASHIF RZA',69,INK,SANS,'font-weight="900" letter-spacing="-3"'),t(30,225,'Ideas into interfaces.',29,INK,SANS,'font-weight="bold"'),t(30,265,'Interfaces into systems.',29,INK,SANS,'font-weight="bold"'),'</g>',t(30,306,'React / Next.js / Node.js / Python',14,MUTED),t(30,346,'NOW BUILDING',9,VIOLET),t(145,347,'HireEdge · AI interview prep',13,INK,SANS),t(30,375,'Open to roles · Bengaluru & remote',12,MUTED)]
 # Three floating slabs form a miniature isometric architecture.
 p += [f'<path class="flow" d="M747 125V385" stroke="{CYAN}" stroke-width="2"/>']
 for i,(y,name,color) in enumerate([(281,'DATA + AI',VIOLET),(218,'API / LOGIC',CYAN),(155,'INTERFACE','#b1c5ff')]):
  p += [f'<g class="float" style="--d:{i*-.7}s">',f'<path d="M602 {y}L746 {y-56}L896 {y}L748 {y+57}Z" fill="#152841" stroke="{color}"/>',f'<path d="M602 {y}V{y+22}L748 {y+80}V{y+57}Z" fill="#102038" stroke="#2b4564"/>',f'<path d="M748 {y+57}L896 {y}V{y+22}L748 {y+80}Z" fill="#0e192c" stroke="#2b4564"/>',t(748,y+67,name,10,color,extra='text-anchor="middle"'),f'<circle class="pulse" cx="{627+i*22}" cy="{y+12}" r="3" fill="{color}"/>','</g>']
 p += [t(748,392,'THE FULL STACK, IN MOTION',9,MUTED,extra='text-anchor="middle"'),f'<path d="M30 413H930" stroke="{LINE}"/>']
 for x,num,txt in [(30,G['public_repos'],'PUBLIC REPOS'),(265,C['stats']['total'],'CONTRIBUTIONS'),(525,G['followers'],'FOLLOWERS'),(760,G['stars'],'REPO STARS')]:
  p += [t(x,454,num,26,CYAN,SANS,'font-weight="bold"'),t(x+57,450,txt,9,MUTED)]
 save(p,'dashboard.svg')

def about():
 p=frame(960,260,'About Ashif: Fullstack developer with a mathematics background. Former frontend intern at Syntechxhub. Building responsive web applications, API integrations and AI-powered tools.')
 label(p,'01','THE DEVELOPER BEHIND THE REPOS')
 p += [t(30,91,'Curious by default. Builder by habit.',28,INK,SANS,'font-weight="bold"'),t(30,125,'I build responsive interfaces, connect APIs, and turn AI ideas into usable web apps.',14,MUTED,SANS)]
 for x,head,line1,line2 in [(30,'EXPERIENCE','Frontend Intern · Syntechxhub','Nov–Dec 2025 / React + Tailwind'),(350,'FOUNDATION','B.Sc. Mathematics','Ranchi University / 2021–2024'),(666,'FOCUS','Full-stack + applied AI','Interfaces / APIs / automation')]:
  p += [t(x,169,head,9,VIOLET),t(x,198,line1,14,INK,SANS),t(x,223,line2,11,MUTED)]
 save(p,'about.svg')

def stack():
 p=frame(960,310,'Technology stack with original Devicon logos: React, Next.js, TypeScript, JavaScript, Tailwind CSS, Node.js, Express, Python, Flask, MongoDB, MySQL, Git, WordPress, Bootstrap, HTML5, CSS3.')
 label(p,'02','THE TOOLBOX / ACTUAL TECH, ACTUAL LOGOS')
 items=[('react','React'),('nextjs','Next.js'),('typescript','TypeScript'),('javascript','JavaScript'),('tailwindcss','Tailwind'),('nodejs','Node.js'),('express','Express'),('python','Python'),('flask','Flask'),('mongodb','MongoDB'),('mysql','MySQL'),('git','Git'),('wordpress','WordPress'),('bootstrap','Bootstrap'),('html5','HTML5'),('css3','CSS3')]
 for i,(slug,name) in enumerate(items):
  col,row=i%8,i//8;x=30+col*113;y=72+row*112
  p += [f'<g class="enter" style="--d:{i*.035}s">',f'<rect x="{x}" y="{y}" width="105" height="97" rx="10" fill="#111e31" stroke="{LINE}"/>',icon(slug,x+36,y+16,32),t(x+52,y+77,name,11,INK,extra='text-anchor="middle"'),'</g>']
 save(p,'stack.svg')

def activity():
 p=frame(960,220,'Public repository language composition by GitHub language bytes, excluding forks and this profile repository. This is code composition, not a proficiency score.')
 label(p,'03','REPOSITORY SIGNAL / PUBLIC GITHUB DATA')
 langs=G['language_bytes'];total=sum(langs.values()) or 1
 colors=['#62e7ff','#af98ff','#ffbc7a','#89edbc','#f188bd','#7389ad']
 p += [t(30,82,'What the codebase says.',24,INK,SANS,'font-weight="bold"'),t(930,79,'SYNC '+G['as_of']+' UTC',9,MUTED,extra='text-anchor="end"')]
 x=30
 for i,(name,count) in enumerate(langs.items()):
  width=900*count/total;p.append(f'<rect x="{x:.2f}" y="108" width="{width:.2f}" height="15" fill="{colors[i%6]}"/>');x+=width
 for i,(name,count) in enumerate(langs.items()):
  x=30+(i%3)*303;y=153+(i//3)*25
  p += [f'<circle cx="{x+3}" cy="{y-4}" r="3" fill="{colors[i%6]}"/>',t(x+15,y,f'{name}  {count/total:.1%}',11,MUTED)]
 p.append(t(30,205,'Language bytes across non-fork public projects; excludes this profile. Not a skill rating.',9,MUTED))
 save(p,'languages.svg')

def repos():
 featured=[('Keystro','AI-powered typing practice.','JavaScript-powered web experience.'),('Clientora','Customer relationship management.','A TypeScript application for client workflows.'),('Emotion_Detection','Exploring emotion detection with Python.','Computer vision and applied machine learning.'),('VideoWithAi','A Next.js project.','TypeScript across the application.')]
 byname={r['name']:r for r in G['repos']}
 for i,(name,one,two) in enumerate(featured):
  r=byname.get(name)
  if not r:raise ValueError('Featured repository missing: '+name)
  p=frame(465,184,f"{name}: {one} {r['language']}. {r['stargazers_count']} stars, {r['forks_count']} forks. Updated {r['pushed_at'][:10]}.")
  p += [t(22,30,f'REPO / 0{i+1}',9,VIOLET),t(439,30,'↗',19,CYAN,extra='text-anchor="end"'),t(22,64,name,24,INK,SANS,'font-weight="bold"'),t(22,95,one,13,MUTED,SANS),t(22,117,two,12,MUTED,SANS),f'<path d="M22 135H443" stroke="{LINE}"/>',t(22,160,r['language'] or 'Docs',10,CYAN),t(183,160,f"STARS {r['stargazers_count']} / FORKS {r['forks_count']}",9,MUTED),t(443,160,r['pushed_at'][:10],9,MUTED,extra='text-anchor="end"')]
  save(p,f'repo-{i+1}.svg')

def arcade():
 p=frame(960,274,'Play Commit Dash. A keyboard and touch controlled 3D-style browser runner. Collect green commits, dodge red bugs and survive 45 seconds. Opens the playable game in a separate page.')
 label(p,'05','BREAK THE SCROLL / PLAY SOMETHING')
 p += [t(30,107,'COMMIT DASH',47,INK,SANS,'font-weight="900" letter-spacing="-2"'),t(30,145,'Ship commits. Dodge bugs. Keep the build alive.',15,MUTED,SANS),'<rect x="30" y="175" width="208" height="46" rx="8" fill="#62e7ff"/>',t(51,204,'LAUNCH THE GAME  ↗',13,BG,extra='font-weight="bold"'),t(30,246,'45 SECONDS / KEYBOARD + TOUCH / LOCAL HIGH SCORE',9,MUTED)]
 for i in range(5):
  p.append(f'<path d="M{622+i*50} 76L{535+i*95} 246" stroke="#28445d"/>')
 for y in [107,138,178,230]:p.append(f'<path class="flow" d="M570 {y}H930" stroke="#24485e"/>')
 for x,y,c in [(706,147,CYAN),(837,115,'#ff728b'),(760,219,VIOLET)]:
  p += [f'<g class="float"><path d="M{x} {y-19}l22 10v23l-22 11-22-11v-23Z" fill="#112c41" stroke="{c}" stroke-width="2"/><path d="M{x-22} {y-9}l22 10 22-10M{x} {y+1}v24" stroke="{c}" fill="none"/></g>']
 save(p,'arcade.svg')

if __name__=='__main__':
 hero();about();stack();activity();repos();arcade()
