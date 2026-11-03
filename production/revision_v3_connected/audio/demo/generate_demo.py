"""Generate unchanged demo-v2 narration with the approved, locked system voice.

Uses the saved MiniMax CLI key after locally comparing it with MINIMAX_KEY_2.
No secrets in files/logs. No tempo changes, speech cuts, music or sound effects.
Resume skips only stems whose source/settings fingerprint matches the manifest.
"""
from __future__ import annotations
import csv, hashlib, json, re, shutil, subprocess, sys, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIO=HERE.parent
PROJECT=HERE.parents[3]
PRODUCTION=PROJECT/'production'
VOICE_SOURCE=PRODUCTION/'voice_demo/settings_polished_american.json'
APPROVED_AUDIO=PRODUCTION/'voice_demo/insightgen_polished_american_demo.mp3'
SOURCE=PROJECT/'insightGen_demo_voiceover_v2.txt'
BOUNDARIES=[0,12,23,33,47,58,67,80,92,99]
MANIFEST=HERE/'demo_manifest.json'
CLI=Path.home()/'AppData/Roaming/npm/node_modules/mmx-cli/dist/mmx.mjs'
NODE=shutil.which('node')

def h(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def binary(name): return str(next((PRODUCTION/'tools').rglob(name+'.exe')))
def ff(args):
    r=subprocess.run([binary('ffmpeg'),'-hide_banner','-loglevel','error','-y',*map(str,args)],capture_output=True,text=True,encoding='utf-8')
    if r.returncode:raise RuntimeError(r.stderr)
def probe(path):
    return json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(path)],encoding='utf-8'))
def save(data):
    MANIFEST.write_text(json.dumps(data,indent=2),encoding='utf-8')
def verify_key():
    env=(PROJECT/'.env').read_text(encoding='utf-8-sig')
    match=re.search(r'^\s*(?:export\s+)?MINIMAX_KEY_2\s*=\s*(.*?)\s*$',env,re.M)
    if not match:raise RuntimeError('MINIMAX_KEY_2 missing from project .env')
    selected=match.group(1).strip().strip('"').strip("'")
    cfg=json.loads((Path.home()/'.mmx/config.json').read_text(encoding='utf-8-sig'))
    if cfg.get('api_key')!=selected:raise RuntimeError('CLI saved credential does not match MINIMAX_KEY_2; no request sent')
    return True

def main():
    if not NODE or not CLI.is_file():raise RuntimeError('Installed Node/mmx CLI not found')
    verify_key()
    source_settings=json.loads(VOICE_SOURCE.read_text(encoding='utf-8-sig'))
    assert source_settings['voice_id']=='English_ConfidentWoman' and source_settings['speed']==1.04 and source_settings['pitch']==-1
    lock={k:source_settings[k] for k in ('voice_id','model','speed','pitch','volume','sample_rate','bitrate')}
    lock.update(channels=1,format='mp3',language='English',key_name='MINIMAX_KEY_2',
        pronunciation=['InsightGen/Insight Jen','C-sixty/see sixty','SQL/S Q L','AOF/A O F'],
        approved_source_audio='production/voice_demo/insightgen_polished_american_demo.mp3',
        approved_source_sha256=h(APPROVED_AUDIO),voice_source_settings_sha256=h(VOICE_SOURCE),
        speed_changes_per_segment_allowed=False,post_tempo_retiming_allowed=False,
        approved_voice_cloning=False)
    AUDIO.mkdir(parents=True,exist_ok=True)
    lock_path=AUDIO/'voice_lock.json'
    if lock_path.exists() and json.loads(lock_path.read_text(encoding='utf-8'))!=lock:
        raise RuntimeError('Existing voice lock differs; refusing to silently change voice settings')
    lock_path.write_text(json.dumps(lock,indent=2),encoding='utf-8')
    approved=dict(source_settings)
    approved.update(approved_by_user=True,original_generation_key_name=approved.pop('key_name'),active_key_name='MINIMAX_KEY_2',approved_audio_sha256=h(APPROVED_AUDIO))
    (AUDIO/'approved_voice_settings.json').write_text(json.dumps(approved,indent=2),encoding='utf-8')
    paragraphs=re.split(r'\r?\n\s*\r?\n',SOURCE.read_text(encoding='utf-8-sig').strip())
    assert len(paragraphs)==9
    fingerprint=hashlib.sha256(json.dumps(lock,sort_keys=True).encode()).hexdigest()
    m=json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {'voice_settings':lock,'voice_fingerprint':fingerprint,'source_script':'insightGen_demo_voiceover_v2.txt','source_sha256':h(SOURCE),'stems':[]}
    if m['voice_fingerprint']!=fingerprint or m['source_sha256']!=h(SOURCE):raise RuntimeError('Existing manifest fingerprint differs')
    for i,text in enumerate(paragraphs,1):
        name=f'demo_{i:02}'
        script=HERE/(name+'.txt');out=HERE/(name+'.mp3')
        script.write_text(text+'\n',encoding='utf-8')
        text_hash=hashlib.sha256(text.encode()).hexdigest()
        prior=next((r for r in m['stems'] if r['id']==name),None)
        if out.exists():
            if not prior or prior['text_sha256']!=text_hash or prior.get('voice_fingerprint')!=fingerprint:raise RuntimeError(f'{name}: existing audio cannot be attributed to locked voice')
        else:
            cmd=[NODE,str(CLI),'speech','synthesize','--text-file',str(script),'--voice',lock['voice_id'],'--model',lock['model'],'--speed',str(lock['speed']),'--pitch',str(lock['pitch']),'--volume',str(lock['volume']),'--language',lock['language'],'--sample-rate',str(lock['sample_rate']),'--bitrate',str(lock['bitrate']),'--channels','1','--format','mp3']
            for pron in lock['pronunciation']:cmd+=['--pronunciation',pron]
            cmd+=['--out',str(out),'--region','global','--non-interactive','--quiet','--output','json']
            r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
            if r.returncode:raise RuntimeError(f'{name}: CLI failed {r.returncode}: {r.stderr or r.stdout}')
        data=probe(out);duration=float(data['format']['duration'])
        ff(['-i',out,'-f','null','-'])
        window=BOUNDARIES[i]-BOUNDARIES[i-1]
        record={'id':name,'file':out.name,'text':text,'text_sha256':text_hash,'voice_fingerprint':fingerprint,'api_voice_id':lock['voice_id'],'api_speed':lock['speed'],'api_pitch':lock['pitch'],'key_name':'MINIMAX_KEY_2','natural_duration_seconds':duration,'nominal_start_seconds':BOUNDARIES[i-1],'nominal_end_seconds':BOUNDARIES[i],'nominal_window_seconds':window,'window_overrun_seconds':max(0,duration-window),'full_decode':'passed','sha256':h(out),'tempo_adjustment':1.0}
        if prior:m['stems'][m['stems'].index(prior)]=record
        else:m['stems'].append(record)
        save(m)
        print(f'{name}: natural {duration:.3f}s / window {window}s / overrun {max(0,duration-window):.3f}s',flush=True)
    # Schedule the full, unchanged speech without overlaps or tempo manipulation.
    # Nominal cue starts are preserved wherever natural duration permits them.
    cursor=0.;placements=[]
    for row in m['stems']:
        start=max(float(row['nominal_start_seconds']),cursor)
        end=start+row['natural_duration_seconds']
        placements.append({'id':row['id'],'actual_start_seconds':round(start,6),'actual_end_seconds':round(end,6),'shift_from_nominal_start_seconds':round(start-row['nominal_start_seconds'],6)})
        cursor=end+.12
    duration=max(99.,placements[-1]['actual_end_seconds'])
    command=[];filters=[];labels=[]
    for i,(row,placement) in enumerate(zip(m['stems'],placements)):
        command+=['-i',HERE/row['file']]
        delay=round(placement['actual_start_seconds']*1000)
        filters.append(f'[{i}:a]adelay={delay}:all=1[a{i}]');labels.append(f'[a{i}]')
    filters.append(''.join(labels)+f'amix=inputs=9:normalize=0,apad,atrim=duration={duration:.6f}[out]')
    wav=HERE/'insightgen_demo_v2_approved_voice.wav'
    ff(command+['-filter_complex',';'.join(filters),'-map','[out]','-ar','44100','-ac','1','-c:a','pcm_s16le',wav])
    master=HERE/'insightgen_demo_v2_approved_voice.mp3'
    ff(['-i',wav,'-ar','44100','-ac','1','-c:a','libmp3lame','-b:a','128k',master])
    ff(['-i',master,'-f','null','-'])
    m.update(placements=placements,master={'file':master.name,'natural_speed_retained':True,'tempo_adjustment':1.0,'planned_nominal_duration_seconds':99,'scheduled_content_duration_seconds':duration,'encoded_duration_seconds':float(probe(master)['format']['duration']),'sha256':h(master),'full_decode':'passed'},master_wav={'file':wav.name,'duration_seconds':float(probe(wav)['format']['duration']),'format':'PCM signed16-bit,44100Hz,mono','sha256':h(wav)},all_stems_same_voice_and_speed=True,recording_sync='Owner-held recording unavailable; all timings require review',overrun_requires_owner_review=any(r['window_overrun_seconds']>0 for r in m['stems']))
    save(m)
    with (HERE/'demo_cues_actual.csv').open('w',encoding='utf-8',newline='') as out:
        rows=[{**{k:row[k] for k in ('id','file','nominal_start_seconds','nominal_end_seconds','natural_duration_seconds','window_overrun_seconds')},**placement,'voice_id':lock['voice_id'],'speed':lock['speed'],'pitch':lock['pitch']} for row,placement in zip(m['stems'],placements)]
        writer=csv.DictWriter(out,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    print(f'Approved-voice demo master: {duration:.3f}s content; no speech trimmed or sped up.',flush=True)

if __name__=='__main__':main()
