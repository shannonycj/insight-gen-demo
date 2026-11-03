"""Build or independently verify the self-contained repository-relative handoff ZIP."""
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
ARCHIVE=PROJECT/'production/insightgen_v3_connected_package.zip'
MANIFEST=ROOT/'package_manifest.json'
CHECKSUMS=ROOT/'package_checksums.sha256'
SAFE_EXT={'.py','.md','.txt','.json','.csv','.png','.jpg','.jpeg','.mp4','.mp3','.wav'}

def sha_file(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
    return h.hexdigest()

def relative(path):return path.relative_to(PROJECT).as_posix()

def select_files():
    files=set()
    for name in ['README.md','requirements.txt','render_connected.py','assemble_connected.py','build_handoff_docs.py','verify_delivery.py','verify_connected.py','build_package.py','generation_manifest.json']:
        p=ROOT/name
        if not p.is_file():raise FileNotFoundError(p)
        files.add(p)
    for kind in ['opening','underthehood']:
        for sound in ['narrated','silent']:files.add(ROOT/f'insightgen_v3_connected_{kind}_{sound}.mp4')
    for folder in ['assets','raw','prompts','docs','edit','audio','qc','frames','overlays']:
        for p in (ROOT/folder).rglob('*'):
            if not p.is_file() or p.suffix.lower() not in SAFE_EXT:continue
            if '__pycache__' in p.parts or any(x.startswith('.') for x in p.relative_to(ROOT).parts):continue
            if p.name=='under_concat.txt' or (folder=='frames' and (p.name.startswith('base_') or p.name.startswith('opening_base_'))):continue
            files.add(p)
    for n in range(1,5):files.add(PROJECT/f'production/revision_v2/film/clean/shot{n}.mp4')
    for n in range(5,8):files.add(PROJECT/f'production/revision_v2/film_refined/clean/shot{n}.mp4')
    for name in ['insightGen_demo_narration_v2.md','insightGen_demo_voiceover_v2.txt']:files.add(PROJECT/name)
    for name in ['insightgen_polished_american_demo.mp3','settings_polished_american.json']:files.add(PROJECT/'production/voice_demo'/name)
    for p in files:
        if not p.is_file():raise FileNotFoundError(p)
        name=relative(p).lower()
        if any(term in name for term in ['/.env','credential','__pycache__','/revision_v3_cinematic/','/rejected/']):raise RuntimeError('Excluded path selected: '+name)
        if p.suffix.lower() not in SAFE_EXT:raise RuntimeError('Unexpected file type: '+name)
        if p.suffix.lower() in {'.py','.md','.json','.csv','.txt'}:
            data=p.read_text(encoding='utf-8-sig')
            if re.search(r'\b(?:sk-[A-Za-z0-9_-]{35,}|MINIMAX_KEY_[12]\s*[=:]\s*[\"\']?[A-Za-z0-9_-]{35,})',data):
                raise RuntimeError('Possible embedded secret in selected text file: '+name)
    return sorted(files,key=relative)

def verify(path):
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:raise RuntimeError('ZIP CRC test failed')
        names=z.namelist()
        if len(names)!=len(set(names)):raise RuntimeError('Duplicate archive paths')
        for n in names:
            p=Path(n)
            if n.startswith('/') or '..' in p.parts or ':' in n:raise RuntimeError('Unsafe archive path')
        manifest_name='production/revision_v3_connected/package_manifest.json'
        checksum_name='production/revision_v3_connected/package_checksums.sha256'
        manifest=json.loads(z.read(manifest_name))
        expected={r['path']:r for r in manifest['payload_files']}
        if set(names)!=set(expected)|{manifest_name,checksum_name}:raise RuntimeError('Unexpected or missing package member')
        for n,info in expected.items():
            data=z.read(n)
            if len(data)!=info['bytes'] or hashlib.sha256(data).hexdigest()!=info['sha256']:raise RuntimeError('Payload hash mismatch: '+n)
        sums={line[66:]:line[:64] for line in z.read(checksum_name).decode('utf-8').splitlines()}
        if set(sums)!=set(expected)|{manifest_name}:raise RuntimeError('Checksum coverage mismatch')
        for n,h in sums.items():
            if hashlib.sha256(z.read(n)).hexdigest()!=h:raise RuntimeError('Checksum mismatch: '+n)
    return {'integrity':'passed','zip_crc_test':'passed','all_payload_sha256':'passed','all_checksum_entries':'passed','file_count':len(names),'payload_file_count':len(expected),'zip_bytes':path.stat().st_size,'zip_sha256':sha_file(path)}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',type=Path);p.add_argument('--list',action='store_true');p.add_argument('--semantic-report',type=Path);a=p.parse_args()
    if a.verify:print(json.dumps(verify(a.verify.resolve()),indent=2));return
    files=select_files()
    if a.list:print(json.dumps({'payload_file_count':len(files),'payload_bytes':sum(p.stat().st_size for p in files),'paths':[relative(p) for p in files]},indent=2));return
    if not a.semantic_report or not a.semantic_report.resolve().is_relative_to((ROOT/'qc').resolve()) or not a.semantic_report.is_file():p.error('Final independent semantic report under qc/ is required before archiving.')
    report=json.loads((ROOT/'qc/verification.json').read_text())
    if not report['all_technical_checks_passed']:p.error('Independent technical checks have not passed.')
    semantic=json.loads(a.semantic_report.read_text())
    if semantic.get('status')!='PASS':p.error('Independent semantic review is not yet PASS.')
    for row in report['checks']:
        details=row.get('details',{})
        if details.get('file') and details.get('sha256'):
            if sha_file(ROOT/details['file'])!=details['sha256']:p.error('Independent QC is stale for '+details['file'])
    gen=ROOT/'generation_manifest.json';generation=json.loads(gen.read_text())
    if not all(v['status']=='succeeded' and (ROOT/v['file']).is_file() for v in generation['video_requests']):p.error('A generated connector is incomplete.')
    generation['planned_next_video']=None
    generation['status']='completed'
    generation['completion_scope']='Both generated connectors, 14-second opening and 70-second explainer narrated/silent exports, and approved fixed-speed narration are complete. Independent technical and sampled semantic checks passed.'
    generation['verification_reports']=['qc/verification.json','qc/semantic_review.json','edit/delivery_verification.json']
    generation['owner_held_recording_status']='Unavailable; recording alignment, complete UI framing and whole-film joins remain unverified.'
    gen.write_text(json.dumps(generation,indent=2)+'\n',encoding='utf-8')
    manifest={'created_at_utc':datetime.now(timezone.utc).isoformat(),'path_base':'Repository root after extraction','archive':relative(ARCHIVE),'payload_file_count':len(files),'archive_file_count_including_checksum_files':len(files)+2,'semantic_report':relative(a.semantic_report.resolve()),'self_reference_policy':'Manifest excludes itself and package_checksums.sha256. Checksum list covers payload and manifest; it excludes itself.','excluded':'Conformed intermediate/cache files, combined clean picture duplicate, logs, bytecode, binaries, credential files, .env and rejected revisions','payload_files':[{'path':relative(p),'bytes':p.stat().st_size,'sha256':sha_file(p)} for p in files]}
    MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    CHECKSUMS.write_text('\n'.join(sha_file(p)+'  '+relative(p) for p in files+[MANIFEST])+'\n',encoding='utf-8')
    pending=ARCHIVE.with_suffix('.building.zip')
    with zipfile.ZipFile(pending,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for file in files+[MANIFEST,CHECKSUMS]:
            z.write(file,relative(file),compress_type=zipfile.ZIP_STORED if file.suffix.lower() in {'.mp4','.mp3','.png','.jpg','.jpeg'} else zipfile.ZIP_DEFLATED)
    pending.replace(ARCHIVE)
    result=verify(ARCHIVE)
    ARCHIVE.with_suffix('.zip.sha256').write_text(result['zip_sha256']+'  '+ARCHIVE.name+'\n',encoding='utf-8')
    ARCHIVE.with_suffix('.integrity.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
