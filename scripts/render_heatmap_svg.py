"""Render actual contribution counts in the SIGNAL design language."""
from datetime import date, timedelta
import json
from make_showcase import ROOT, frame, text, write, INK, MUTED, LINE, LIME, PURPLE, SANS


def main():
    data=json.loads((ROOT/'data/contributions.json').read_text())
    days,stats=data['days'],data['stats']
    p=frame(346,'The work, in public',f"{stats['total']} contributions. Current streak {stats['current_streak']} days, longest streak {stats['longest_streak']} days in the displayed period. Updated {data['as_of']} UTC.")
    p += [text(32,35,'03 / THE WORK, IN PUBLIC',10,LIME),text(928,35,f"SYNCED {data['as_of']} UTC",9,MUTED,extra='text-anchor="end"'),text(32,79,'Small commits. Real progress.',28,INK,SANS,'font-weight="bold" letter-spacing="-.5"')]
    for x,value,label in [(32,stats['total'],'CONTRIBUTIONS'),(347,f"{stats['current_streak']}d",'CURRENT STREAK'),(662,f"{stats['longest_streak']}d",'LONGEST IN WINDOW')]:
        p += [text(x,127,value,31,LIME,SANS,'font-weight="bold"'),text(x+88,125,label,9,MUTED)]
    p += [f'<path d="M32 145H928" stroke="{LINE}"/>']
    first=date.fromisoformat(days[0]['date'])
    origin=first-timedelta(days=(first.weekday()+1)%7)
    weeks=((date.fromisoformat(days[-1]['date'])-origin).days//7)+1
    step=868/weeks
    palette=['#1d222b','#38432c','#657d36','#a3c94c',LIME]
    for day in days:
        dt=date.fromisoformat(day['date'])
        col,row=divmod((dt-origin).days,7)
        x,y=58+col*step,180+row*16
        if dt.day==1 and col<weeks-2:
            p.append(text(x,169,dt.strftime('%b').upper(),8,MUTED))
        p.append(f'<g class="enter" style="--d:{(col+row)*.018:.3f}s"><rect x="{x:.2f}" y="{y}" width="{step-4:.2f}" height="12" rx="2" fill="{palette[day["level"]]}"><title>{day["date"]}: {day["count"]} contributions</title></rect></g>')
    for row,label in [(1,'M'),(3,'W'),(5,'F')]:
        p.append(text(32,190+row*16,label,8,MUTED))
    p += [text(32,318,f"{days[0]['date']} / {days[-1]['date']}",9,MUTED),text(382,318,'DAILY SYNC / PUBLIC GITHUB DATA',9,PURPLE),text(758,318,'LESS',8,MUTED)]
    for i,color in enumerate(palette):
        p.append(f'<rect x="{794+i*17}" y="308" width="12" height="12" rx="2" fill="{color}"/>')
    p.append(text(889,318,'MORE',8,MUTED))
    write(p,'contrib-heatmap.svg')


if __name__=='__main__':
    main()
