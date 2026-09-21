export function freshState(best=0){return {mode:'ready',lane:1,time:0,score:0,lives:3,combo:0,best,objects:[],spawn:0.55};}
export function start(s){Object.assign(s,freshState(s.best),{mode:'running'});}
export function move(s,d){if(s.mode==='running')s.lane=Math.max(0,Math.min(2,s.lane+d));}
export function pause(s){if(s.mode==='running')s.mode='paused';else if(s.mode==='paused')s.mode='running';}
export function update(s,dt,random=Math.random){
 if(s.mode!=='running')return [];
 dt=Math.max(0,Math.min(dt,.05));s.time+=dt;s.spawn-=dt;const events=[];
 const speed=.34+Math.min(s.time/45,1)*.22;
 if(s.spawn<=0){s.objects.push({lane:Math.floor(random()*3),z:0,kind:random()<.65?'commit':'bug'});s.spawn=.72-Math.min(s.time/45,1)*.21;}
 for(const o of s.objects){o.z+=dt*speed;if(o.z>=1&&!o.done){o.done=true;if(o.lane===s.lane){if(o.kind==='commit'){s.combo++;s.score+=10*(s.combo>=5?2:1);events.push('commit');}else{s.lives--;s.combo=0;events.push('bug');}}}}
 s.objects=s.objects.filter(o=>o.z<1.2);
 if(s.lives<=0){s.mode='over';events.push('over');}
 else if(s.time>=45){s.time=45;s.mode='won';events.push('won');}
 s.best=Math.max(s.best,s.score);return events;
}
