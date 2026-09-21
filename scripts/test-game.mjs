import assert from 'node:assert/strict';
import {freshState,start,move,pause,update} from '../game/model.mjs';
const s=freshState();start(s);move(s,-1);move(s,-1);assert.equal(s.lane,0);move(s,1);move(s,1);move(s,1);assert.equal(s.lane,2);
pause(s);update(s,.05);assert.equal(s.time,0);move(s,-1);assert.equal(s.lane,2);pause(s);
s.objects=[{lane:2,z:.999,kind:'commit'}];update(s,.05);assert.equal(s.score,10);assert.equal(s.combo,1);
s.combo=4;s.objects=[{lane:2,z:.999,kind:'commit'}];update(s,.05);assert.equal(s.score,30);
s.lives=1;s.objects=[{lane:2,z:.999,kind:'bug'}];assert.ok(update(s,.05).includes('over'));assert.equal(s.mode,'over');assert.equal(s.combo,0);
start(s);assert.equal(s.score,0);assert.equal(s.lives,3);assert.equal(s.best,30);s.time=44.99;s.spawn=1;assert.ok(update(s,.05).includes('won'));assert.equal(s.time,45);
console.log('Game model: movement, pause, collisions, combos, game over, restart, best score and victory passed.');
