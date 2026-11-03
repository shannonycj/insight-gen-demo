"""Render opening and eight story cues with the exact approved voice lock.

Uses MINIMAX_KEY_2/global via the installed CLI. No individual speed changes,
speech cuts, post-tempo changes, music, sound effects or old narration.
"""
from __future__ import annotations
import csv,hashlib,json,subprocess,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIO=HERE.parent
ROOT=AUDIO.parent
START_OVERRIDES={'close':65.15}  # Main-approved: final wide is65–70; full4.667sclosingfitswithoutretiming.
sys.path.insert(0,str(AUDIO/'demo'))
import generate_demo as common

def save(m):
    (HERE/'narrative_manifest.json').write_text(json.dumps(m,indent=2),encoding='utf-8')

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    common.verify_key()
    story_path=ROOT/'edit/story.json'
    story=json.loads(story_path.read_text(encoding='utf-8-sig'))
    lock=json.loads((AUDIO/'voice_lock.json').read_text(encoding='utf-8-sig'))
    assert lock['voice_id']=='English_ConfidentWoman' and lock['speed']==1.04 and lock['pitch']==-1
    fingerprint=hashlib.sha256(json.dumps(lock,sort_keys=True).encode()).hexdigest()
    manifest_path=HERE/'narrative_manifest.json'
    m=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'voice_settings':lock,'voice_fingerprint':fingerprint,'source_story_sha256':common.h(story_path),'stems':[]}
    assert m['voice_fingerprint']==fingerprint,'Narrative voice changed; review existing takes before any new request'
    cues=[{'id':'opening','start':0,'end':14,'narration':story['opening']['narration'],'section':'opening'}]+[{**c,'section':'under_the_hood'} for c in story['under_the_hood']['cues']]
    for cue in cues:
        name=cue['id'];script=HERE/(name+'.txt');out=HERE/(name+'_raw.mp3')
        original=AUDIO/'scripts'/(name+'.txt')
        if original.is_file():
            assert original.read_text(encoding='utf-8-sig').strip()==cue['narration'],f'Script/story mismatch: {name}'
        script.write_text(cue['narration']+'\n',encoding='utf-8')
        text_hash=hashlib.sha256(cue['narration'].encode()).hexdigest()
        prior=next((r for r in m['stems'] if r['id']==name),None)
        if out.is_file():
            assert prior and prior['text_sha256']==text_hash and prior['voice_fingerprint']==fingerprint,f'Existing unattributed stem: {name}'
        else:
            args=[common.NODE,str(common.CLI),'speech','synthesize','--text-file',str(script),'--voice',lock['voice_id'],'--model',lock['model'],'--speed',str(lock['speed']),'--pitch',str(lock['pitch']),'--volume',str(lock['volume']),'--language',lock['language'],'--sample-rate',str(lock['sample_rate']),'--bitrate',str(lock['bitrate']),'--channels',str(lock['channels']),'--format',lock['format']]
            for p in lock['pronunciation']:args+=['--pronunciation',p]
            args+=['--out',str(out),'--region','global','--non-interactive','--quiet','--output','json']
            r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
            if r.returncode:raise RuntimeError(f'{name} CLI error {r.returncode}: {r.stderr or r.stdout}')
        info=common.probe(out);duration=float(info['format']['duration']);s=next(v for v in info['streams'] if v['codec_type']=='audio')
        assert int(s['sample_rate'])==lock['sample_rate'] and s['channels']==lock['channels']
        common.ff(['-i',out,'-f','null','-'])
        window=cue['end']-cue['start']
        row={'id':name,'section':cue['section'],'file':out.name,'text':cue['narration'],'text_sha256':text_hash,'voice_fingerprint':fingerprint,'voice_id':lock['voice_id'],'speed':lock['speed'],'pitch':lock['pitch'],'volume':lock['volume'],'key_name':'MINIMAX_KEY_2','natural_duration_seconds':duration,'nominal_start_seconds':cue['start'],'nominal_end_seconds':cue['end'],'nominal_window_seconds':window,'window_overrun_seconds':max(0,duration-window),'tempo_adjustment':1.0,'full_decode':'passed','sha256':common.h(out)}
        if prior:m['stems'][m['stems'].index(prior)]=row
        else:m['stems'].append(row)
        save(m)
        print(f'{name}: {duration:.3f}s / {window}s window; overrun {max(0,duration-window):.3f}s',flush=True)
    outputs={};placements_all=[]
    for section,target,basename in [('opening',14,'insightgen_opening_approved_voice'),('under_the_hood',70,'insightgen_underthehood_approved_voice')]:
        stems=[r for r in m['stems'] if r['section']==section]
        cursor=0.;placements=[];args=[];filters=[];labels=[]
        for i,row in enumerate(stems):
            preferred=START_OVERRIDES.get(row['id'],float(row['nominal_start_seconds'])) if section=='under_the_hood' else float(row['nominal_start_seconds'])
            start=max(preferred,cursor);end=start+row['natural_duration_seconds'];cursor=end+.12
            placements.append({'id':row['id'],'section':section,'actual_start_seconds':round(start,6),'actual_end_seconds':round(end,6),'shift_from_nominal_start_seconds':round(start-row['nominal_start_seconds'],6)})
            args+=['-i',HERE/row['file']]
            filters.append(f'[{i}:a]adelay={round(start*1000)}:all=1[a{i}]');labels.append(f'[a{i}]')
        duration=max(float(target),placements[-1]['actual_end_seconds'])
        filters.append(''.join(labels)+f'amix=inputs={len(stems)}:normalize=0,apad,atrim=duration={duration:.6f}[out]')
        wav=HERE/(basename+'.wav');mp3=HERE/(basename+'.mp3')
        common.ff(args+['-filter_complex',';'.join(filters),'-map','[out]','-ar','44100','-ac','1','-c:a','pcm_s16le',wav])
        common.ff(['-i',wav,'-ar','44100','-ac','1','-c:a','libmp3lame','-b:a','128k',mp3])
        common.ff(['-i',wav,'-f','null','-']);common.ff(['-i',mp3,'-f','null','-'])
        outputs[section]={'wav':wav.name,'mp3':mp3.name,'target_duration_seconds':target,'actual_content_duration_seconds':duration,'wav_duration_seconds':float(common.probe(wav)['format']['duration']),'mp3_encoded_duration_seconds':float(common.probe(mp3)['format']['duration']),'no_tempo_retiming':True,'speech_trimmed':False,'wav_sha256':common.h(wav),'mp3_sha256':common.h(mp3),'full_decode':'passed'}
        placements_all+=placements
    m.update(masters=outputs,placements=placements_all,all_audio_uses_identical_approved_voice_speed=True,no_speech_retiming=True,window_overruns=[{'id':r['id'],'overrun_seconds':r['window_overrun_seconds']} for r in m['stems'] if r['window_overrun_seconds']>0])
    save(m)
    rows=[{**{k:row[k] for k in ('id','section','file','nominal_start_seconds','nominal_end_seconds','natural_duration_seconds','window_overrun_seconds')},**p,'voice_id':lock['voice_id'],'speed':lock['speed'],'pitch':lock['pitch']} for row,p in zip(m['stems'],placements_all)]
    with (HERE/'narrative_cues_actual.csv').open('w',encoding='utf-8',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    with (HERE/'actual_cues.csv').open('w',encoding='utf-8',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    current_story=json.loads(story_path.read_text(encoding='utf-8-sig'))
    assert current_story['opening']['narration']==story['opening']['narration'] and [c['narration'] for c in current_story['under_the_hood']['cues']]==[c['narration'] for c in story['under_the_hood']['cues']],'Narration changed during synthesis; review audio before updating cue metadata'
    current_story['audio_actuals']={'voice_lock':'../audio/voice_lock.json','synthesis_speed':lock['speed'],'speech_retimed':False,'cue_placements':[{'id':p['id'],'section':p['section'],'actual_start':p['actual_start_seconds'],'actual_end':p['actual_end_seconds'],'shift_from_planned_start':p['shift_from_nominal_start_seconds']} for p in placements_all],'opening_master_seconds':outputs['opening']['actual_content_duration_seconds'],'underhood_master_seconds':outputs['under_the_hood']['actual_content_duration_seconds'],'note':'Plannedvisualcutlistandnarrationwindowsarepreserved; closingactualstart65.15approvedtoretainfullspeechin70s.'}
    story_path.write_text(json.dumps(current_story,indent=2),encoding='utf-8')
    print(json.dumps({'master_durations':{k:v['actual_content_duration_seconds'] for k,v in outputs.items()},'overruns':m['window_overruns']},indent=2),flush=True)

if __name__=='__main__':main()
