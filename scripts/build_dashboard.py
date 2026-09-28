"""Render the GLASS NOTES profile from real GitHub snapshots."""
import json, math, re, base64
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET
import os
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
INK='#f3eee2';MUTED='#b0b0a4';CYAN='#ed9d79';VIOLET='#afc4af';LINE='#444940';BG='#131815';MONO='Consolas,monospace';SANS='Arial,Helvetica,sans-serif'
G=json.loads((ROOT/'data/github.json').read_text());C=json.loads((ROOT/'data/contributions.json').read_text())

def t(x,y,s,size=12,color=INK,font=MONO,extra=''):
 return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" {extra}>{escape(str(s))}</text>'

def frame(w,h,title):
 css='''@keyframes in{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}@keyframes tilt{0%,100%{transform:translate(0,0) rotate(-2deg) scale(.99)}50%{transform:translate(-4px,-7px) rotate(2deg) scale(1.015)}}@keyframes sheen{0%,15%{transform:translateX(-450px);opacity:0}35%,55%{opacity:.7}80%,100%{transform:translateX(1100px);opacity:0}}@keyframes flow{to{stroke-dashoffset:-100}}@keyframes pulse{0%,100%{opacity:.4}50%{opacity:.8}}.enter{animation:in .9s ease-out both;animation-delay:var(--d,0s)}.portrait{transform-origin:751px 239px;animation:tilt 9s ease-in-out infinite}.sheen{animation:sheen 12s ease-in-out infinite;pointer-events:none}.flow{stroke-dasharray:5 12;animation:flow 5s linear infinite}.pulse{animation:pulse 6s ease-in-out infinite}@media(prefers-reduced-motion:reduce){*{animation:none!important}.sheen{display:none}}'''
 if os.environ.get('STATIC')=='1':css+='*{animation:none!important}.sheen{display:none}'
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><style>{css}</style>',
 '<defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="#303b33"/><stop offset=".5" stop-color="#1b221e"/><stop offset="1" stop-color="#20201d"/></linearGradient><linearGradient id="edge" x2="1" y2="1"><stop stop-color="#ffffff" stop-opacity=".38"/><stop offset=".4" stop-color="#d3ddc9" stop-opacity=".05"/><stop offset="1" stop-color="#d3ddc9" stop-opacity=".22"/></linearGradient><linearGradient id="glass" x2=".7" y2="1"><stop stop-color="#ffffff" stop-opacity=".11"/><stop offset="1" stop-color="#ffffff" stop-opacity=".025"/></linearGradient><linearGradient id="shine"><stop stop-color="#ffffff" stop-opacity="0"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".12"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient><radialGradient id="warm"><stop stop-color="#bf5d37" stop-opacity=".22"/><stop offset="1" stop-color="#bf5d37" stop-opacity="0"/></radialGradient><radialGradient id="sage"><stop stop-color="#9abca5" stop-opacity=".14"/><stop offset="1" stop-color="#9abca5" stop-opacity="0"/></radialGradient></defs>',
 f'<defs><clipPath id="panel"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="26"/></clipPath></defs>',
 f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="26" fill="url(#surface)" stroke="url(#edge)"/>',
 f'<g clip-path="url(#panel)"><ellipse cx="{w*.94}" cy="{h*.13}" rx="{w*.6}" ry="{h*.9}" fill="url(#warm)"/><ellipse cx="0" cy="{h}" rx="{w*.55}" ry="{h}" fill="url(#sage)"/></g>']


def glass(x,y,w,h,r=18):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#glass)" stroke="url(#edge)"/>'

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
 p=frame(960,565,'ASHIF RZA / Fullstack Developer. Illustrated portrait with automatic tilt. Dark glass-style README with terracotta, sage and cream.')
 label(p,'AR','GLASS NOTES / ASHIF RZA')
 p += [t(930,32,'BUILD / LEARN / REPEAT',10,VIOLET,extra='text-anchor="end"'),
       glass(30,73,237,30,15),'<circle cx="47" cy="88" r="3" fill="#afc4af"/>',t(61,92,'FULLSTACK DEVELOPER',10,INK),
       '<g class="enter">',t(27,195,'ASHIF',98,INK,SANS,'font-weight="900" letter-spacing="-5"'),t(27,285,'RZA.',98,INK,SANS,'font-weight="900" letter-spacing="-5"'),'</g>',
       t(32,329,'Code, craft & a little curiosity.',27,INK,'Georgia,serif','font-style="italic"'),t(32,363,'React interfaces. Node.js APIs. Applied AI.',13,MUTED),
       glass(30,394,474,45,16),t(48,421,'NOW',10,CYAN),t(97,421,'HireEdge / AI interview preparation',12,INK)]
 image_data=base64.b64encode((OUT/'portrait.png').read_bytes()).decode('ascii')
 p += ['<circle cx="751" cy="244" r="174" fill="url(#warm)"/>',
       '<g class="portrait">',glass(569,71,363,350,44),
       '<defs><clipPath id="portrait-circle"><circle cx="751" cy="237" r="145"/></clipPath></defs>',
       f'<image x="606" y="92" width="290" height="290" href="data:image/png;base64,{image_data}" clip-path="url(#portrait-circle)"/>',
       '<circle cx="751" cy="237" r="145" fill="none" stroke="#f3eee2" stroke-opacity=".35"/>',
       '<path d="M587 118Q587 88 620 88H808" fill="none" stroke="#ffffff" stroke-opacity=".22" stroke-width="2"/>',
       '<g clip-path="url(#portrait-circle)"><path class="sheen" d="M0 50H95L245 420H150Z" fill="url(#shine)"/></g>',
       t(751,405,'THE HUMAN BEHIND THE CODE',9,VIOLET,extra='text-anchor="middle" letter-spacing="1"'),'</g>',
       '<path d="M30 464H930" stroke="#444940"/>']
 for x,num,txt in [(30,G['public_repos'],'PUBLIC REPOS'),(263,C['stats']['total'],'CONTRIBUTIONS'),(496,G['followers'],'FOLLOWERS'),(729,G['stars'],'REPO STARS')]:
  p += [glass(x,481,201,59,17),t(x+17,520,num,27,INK,SANS,'font-weight="bold"'),t(x+87,516,txt,8,VIOLET)]
 p.append(t(930,556,'DATA SNAPSHOT / '+G['as_of'],8,MUTED,extra='text-anchor="end"'))
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
  p += [f'<g class="enter" style="--d:{i*.035}s">',f'<rect x="{x}" y="{y}" width="105" height="97" rx="18" fill="url(#glass)" stroke="url(#edge)"/>',icon(slug,x+36,y+16,32),t(x+52,y+77,name,11,INK,extra='text-anchor="middle"'),'</g>']
 save(p,'stack.svg')

def activity():
 p=frame(960,220,'Public repository language composition by GitHub language bytes, excluding forks and this profile repository. This is code composition, not a proficiency score.')
 label(p,'04','THE CODE / PUBLIC REPOSITORIES')
 langs=G['language_bytes'];total=sum(langs.values()) or 1
 colors=['#e49c79','#afc4af','#cfb277','#a2acbe','#c595a1','#888e83']
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
  p += [f'<path d="M24 14H441" stroke="{CYAN if i%2==0 else VIOLET}" stroke-opacity=".5"/>','<g class="enter">',t(22,39,f'0{i+1} / SELECTED WORK',9,MUTED),t(440,40,'↗',22,CYAN,extra='text-anchor="end"'),t(22,88,name,26,INK,SANS,'font-weight="bold" letter-spacing="-.7"'),t(22,119,one,14,MUTED,'Georgia,serif','font-style="italic"'),t(22,143,two,11,MUTED),'</g>',f'<path d="M22 166H443" stroke="{LINE}"/>',t(22,192,r['language'] or 'Docs',10,VIOLET),t(169,192,f"STARS {r['stargazers_count']} / FORKS {r['forks_count']}",9,MUTED),t(443,192,r['pushed_at'][:10],9,MUTED,extra='text-anchor="end"')]
  save(p,f'repo-{i+1}.svg')

def arcade():
 p=frame(960,242,'Play Commit Dash. A 45-second runner with keyboard and touch controls. Opens the existing game on a separate page.')
 label(p,'06','A SMALL DISTRACTION')
 p += [t(30,112,'All work? No thanks.',38,INK,'Georgia,serif','font-style="italic"'),t(30,152,'Collect commits. Dodge bugs. Beat your best.',14,MUTED),t(30,213,'COMMIT DASH / 45 SECONDS / KEYBOARD + TOUCH',9,VIOLET),
       glass(631,83,267,86,25),t(665,135,'PLAY A ROUND',17,'#f4f2e8',extra='font-weight="bold"'),t(869,138,'↗',29,'#f4f2e8',extra='text-anchor="end"'),
       '<path class="flow" d="M632 196H899" stroke="#ed9d79" stroke-width="2"/>']
 save(p,'arcade.svg')

if __name__=='__main__':
 hero();about();stack();activity();repos();arcade()
