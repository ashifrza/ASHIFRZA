"""SIGNAL / an animated, self-contained GitHub profile. No external assets."""
import json
import os
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = os.environ.get('STATIC') == '1'
INK, MUTED, LINE, LIME, PURPLE = '#f0efe8', '#999da7', '#292d36', '#d8ff62', '#a79bff'
MONO = 'Consolas,monospace'
SANS = 'Arial,Helvetica,sans-serif'


def text(x,y,value,size=12,color=INK,font=MONO,extra=''):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" {extra}>{escape(str(value))}</text>'


def frame(height,title,desc):
    css = '''
    @keyframes arrive{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
    @keyframes orbit{to{transform:rotate(360deg)}}
    @keyframes scan{0%,100%{transform:translateY(0);opacity:0}12%,80%{opacity:.8}90%{transform:translateY(286px);opacity:0}}
    @keyframes packet{0%{stroke-dashoffset:180;opacity:0}12%,80%{opacity:1}100%{stroke-dashoffset:-320;opacity:0}}
    @keyframes draw{from{stroke-dashoffset:900}to{stroke-dashoffset:0}}
    .enter{animation:arrive .8s cubic-bezier(.16,1,.3,1) both;animation-delay:var(--d,0s)}
    .orbit{transform-origin:744px 229px;animation:orbit 38s linear infinite}
    .orbit-back{transform-origin:744px 229px;animation:orbit 54s linear infinite reverse}
    .scan{animation:scan 7s ease-in-out infinite}
    .packet{stroke-dasharray:30 500;animation:packet 5s linear infinite}
    .trace{stroke-dasharray:900;animation:draw 2.4s ease-out both}
    @media(prefers-reduced-motion:reduce){*{animation:none!important}.scan,.packet{display:none}.trace{stroke-dasharray:none}}
    '''
    if STATIC:
        css += '*{animation:none!important}.scan,.packet{display:none}.trace{stroke-dasharray:none}'
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
        f'<style>{css}</style>',
        '<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#242831" stroke-width=".5"/></pattern><radialGradient id="halo"><stop stop-color="#343645" stop-opacity=".65"/><stop offset="1" stop-color="#0c0e13" stop-opacity="0"/></radialGradient></defs>',
        f'<rect width="960" height="{height}" rx="18" fill="#0c0e13"/>',
        f'<rect x=".5" y=".5" width="959" height="{height-1}" rx="18" fill="none" stroke="{LINE}"/>']


def write(parts,name):
    (ROOT/name).write_text('\n'.join(parts+['</svg>'])+'\n',encoding='utf-8')


def hero():
    profile=json.loads((ROOT/'profile.json').read_text())
    portrait=json.loads((ROOT/'data/portrait.json').read_text())
    p=frame(510,'ASHIF RZA / Fullstack Developer','Ashif Rza builds full-stack web applications with React, Node.js and AI. An ASCII portrait is surrounded by animated orbital paths.')
    p += ['<rect x="526" y="53" width="410" height="375" fill="url(#grid)"/>','<circle cx="744" cy="229" r="215" fill="url(#halo)"/>',
          text(32,34,'A/R',14,LIME,extra='font-weight="bold"'),text(89,34,'ENGINEER / CREATOR',10,MUTED),text(928,34,'PORTFOLIO SYSTEM  •  01',10,MUTED,extra='text-anchor="end"'),
          f'<path d="M32 51H928" stroke="{LINE}"/>']
    p += ['<g class="enter">',text(32,98,'HELLO, WORLD. I\'M',12,LIME,extra='letter-spacing="2"'),
          text(25,205,'ASHIF',112,INK,SANS,'font-weight="900" letter-spacing="-7"'),
          text(25,312,'RZA',112,INK,SANS,'font-weight="900" letter-spacing="-7"'),
          '<rect x="255" y="291" width="21" height="21" fill="#d8ff62"/>','</g>',
          '<g class="enter" style="--d:.18s">',text(33,354,profile['role'],23,INK,SANS),
          text(33,388,'Interfaces with intent.',14,MUTED),text(33,410,'APIs with purpose. AI in the mix.',14,MUTED),'</g>']
    # Independent orbit layers leave the portrait perfectly still and readable.
    p += [f'<circle cx="744" cy="229" r="163" fill="none" stroke="{LINE}"/>',
          f'<g class="orbit"><circle cx="744" cy="229" r="176" fill="none" stroke="{PURPLE}" stroke-opacity=".7" stroke-dasharray="125 981"/><circle cx="920" cy="229" r="4" fill="{LIME}"/></g>',
          f'<g class="orbit-back"><circle cx="744" cy="229" r="151" fill="none" stroke="{LIME}" stroke-opacity=".4" stroke-dasharray="36 220"/></g>',
          '<defs><clipPath id="face"><ellipse cx="744" cy="231" rx="127" ry="142"/></clipPath></defs>',
          '<g clip-path="url(#face)">']
    for i,row in enumerate(portrait):
        p += [f'<g class="enter" style="--d:{.2+i*.017:.3f}s">',text(623,100+i*4.05,row,4.1,'#d0d1d7',extra='xml:space="preserve" textLength="242" lengthAdjust="spacingAndGlyphs"'),'</g>']
    p += [f'<path class="scan" d="M613 91H875" stroke="{LIME}" stroke-width="1.5"/>','</g>',
          text(576,426,'FIG.01',9,PURPLE),text(927,426,'HUMAN BEHIND THE CODE',9,MUTED,extra='text-anchor="end"'),
          f'<path d="M32 451H928" stroke="{LINE}"/>',
          text(32,484,'REACT  /  NODE.JS  /  AI',11,LIME),text(928,484,'ashifrza.in   ↗',13,INK,extra='text-anchor="end"')]
    write(p,'hero.svg')


def systems():
    p=frame(285,'From interface to intelligence','Frontend: React, Next.js, TypeScript. Backend: Node.js, Express, Flask. Data: MongoDB, MySQL and AI APIs. Projects include AI stock prediction and image generation and classification.')
    p += [text(32,35,'02 / THE BUILD SYSTEM',10,LIME),text(32,76,'From interface to intelligence.',29,INK,SANS,'font-weight="bold" letter-spacing="-.5"'),text(928,35,'ONE DEVELOPER. THE WHOLE STACK.',9,MUTED,extra='text-anchor="end"')]
    items=[(32,'01','INTERFACE','React / Next.js','TypeScript / Tailwind'),(347,'02','ENGINE','Node.js / Express','Flask / REST APIs'),(662,'03','INTELLIGENCE','MongoDB / MySQL','AI APIs / Python')]
    for i,(x,n,title,line1,line2) in enumerate(items):
        p += [f'<g class="enter" style="--d:{i*.16}s">',f'<rect x="{x}" y="104" width="266" height="119" rx="9" fill="#12151c" stroke="{LINE}"/>',text(x+17,130,n,10,PURPLE),text(x+48,130,title,11,LIME),text(x+17,166,line1,15,INK,SANS),text(x+17,194,line2,11,MUTED),'</g>']
        if i<2:
            d=f'M{x+266} 164H{x+315}'
            p += [f'<path d="{d}" stroke="{LINE}" fill="none"/>',f'<path class="packet" d="{d}" stroke="{LIME}" stroke-width="2" fill="none" style="animation-delay:{i*.6}s"/>']
    p += [text(32,259,'BUILT:',10,PURPLE),text(89,259,'AI stock prediction',11,MUTED),text(371,259,'Image generation + classification',11,MUTED)]
    write(p,'systems.svg')


def links():
    for filename, label in [('portfolio','EXPLORE PORTFOLIO'),('linkedin','LET\'S CONNECT'),('email','SAY HELLO')]:
        parts=['<svg xmlns="http://www.w3.org/2000/svg" width="220" height="52" viewBox="0 0 220 52">',
               f'<title>{escape(label)}</title>',
               '<rect x=".5" y=".5" width="219" height="51" rx="8" fill="#12151c" stroke="#333941"/>',
               text(18,31,label,11,LIME),text(200,32,'↗',19,INK,extra='text-anchor="end"')]
        write(parts,f'link-{filename}.svg')


if __name__=='__main__':
    hero()
    systems()
    links()
