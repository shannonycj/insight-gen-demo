"""Local verification of connected v3 video, approved voice, cues and source reuse.

Run after final render: python verify_connected.py
No API calls, credential reads, audio synthesis or rendering. Semantic acceptance
requires visual review and is deliberately not asserted by these checks.
"""
from __future__ import annotations
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
PRODUCTION = ROOT.parent
PROJECT = PRODUCTION.parent
QC = ROOT/'qc'
RESULTS = []
EXPECTED = {'voice_id': 'English_ConfidentWoman', 'model': 'speech-2.8-hd',
            'speed': 1.04, 'pitch': -1, 'volume': 1, 'sample_rate': 44100,
            'bitrate': 128000, 'channels': 1, 'key_name': 'MINIMAX_KEY_2'}
PCM_CACHE = {}


def binary(name):
    matches = list((PRODUCTION/'tools').rglob(name+'.exe'))
    if matches:
        return str(matches[0])
    result = shutil.which(name)
    if not result:
        raise FileNotFoundError(name+' not found')
    return result


def jread(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(value, message):
    if not value:
        raise AssertionError(message)


def check(name, fn):
    try:
        details = fn()
        row = {'name': name, 'passed': True, 'details': details}
    except Exception as exc:
        row = {'name': name, 'passed': False, 'error': str(exc)}
    RESULTS.append(row)
    print(('PASS: ' if row['passed'] else 'FAIL: ')+name, flush=True)
    if not row['passed']:
        print(row['error'], flush=True)


def probe(path, count=False):
    cmd = [binary('ffprobe'), '-v', 'error']
    if count:
        cmd += ['-count_frames']
    return json.loads(subprocess.check_output(cmd+['-show_streams', '-show_format', '-of', 'json', str(path)], encoding='utf-8'))


def decode(path):
    subprocess.run([binary('ffmpeg'), '-v', 'error', '-xerror', '-i', str(path), '-f', 'null', '-'], check=True, capture_output=True)


def pcm(path):
    key = str(path.resolve())
    if key not in PCM_CACHE:
        raw = subprocess.check_output([binary('ffmpeg'), '-v', 'error', '-i', str(path), '-map', '0:a:0', '-ac', '1', '-ar', '44100', '-f', 'f32le', '-'])
        PCM_CACHE[key] = np.frombuffer(raw, dtype='<f4').astype(np.float64)
    return PCM_CACHE[key]


def audio_match(reference, delivered, max_offset=2048):
    """Compare one sample grid; allow a small codec delay, never a time warp."""
    x, y = reference, delivered
    require(min(len(x), len(y)) > 44100, 'Audio comparison is too short')
    # FFT correlation finds a single codec-priming offset. No resampling or
    # variable alignment is permitted beyond ordinary 44.1k delivery decoding.
    n = min(len(x), len(y), 44100*10)
    xa, ya = x[:n]-np.mean(x[:n]), y[:n]-np.mean(y[:n])
    size = 1 << (2*n-1).bit_length()
    corr = np.fft.irfft(np.fft.rfft(ya, size)*np.conj(np.fft.rfft(xa, size)), size)
    lags = np.arange(-max_offset, max_offset+1)
    scores = corr[lags % size]
    lag = int(lags[int(np.argmax(scores))])
    if lag >= 0:
        a, b = x, y[lag:]
    else:
        a, b = x[-lag:], y
    length = min(len(a), len(b))
    a, b = a[:length], b[:length]
    require(float(np.std(a)) > 1e-5 and float(np.std(b)) > 1e-5, 'Audio unexpectedly silent')
    coefficient = float(np.corrcoef(a, b)[0, 1])
    coverage = length/len(x)
    require(coefficient > .99, f'Audio correlation {coefficient:.8f} does not establish unchanged master audio')
    require(coverage > .995, f'Audio overlap covers only {coverage:.6%} of reference')
    return {'correlation': coefficient, 'fixed_offset_samples': lag,
            'fixed_offset_seconds': lag/44100, 'reference_coverage': coverage,
            'comparison_method': 'One fixed sample grid and at most 2048 samples of codec offset; no tempo or dynamic-time alignment'}


def verify_export(name, seconds, frames, master):
    path = ROOT/name
    meta = probe(path, True)
    videos = [s for s in meta['streams'] if s['codec_type'] == 'video']
    audios = [s for s in meta['streams'] if s['codec_type'] == 'audio']
    require(len(videos) == 1 and len(audios) == 1, 'Export must contain exactly one video and one narration stream')
    v, a = videos[0], audios[0]
    require((v['width'], v['height']) == (1280, 720), 'Video dimensions differ')
    require(Fraction(v['r_frame_rate']) == 24, 'Video frame rate differs')
    require(int(v['nb_read_frames']) == frames, 'Decoded frame count differs')
    require(abs(float(v['duration'])-seconds) < .021, 'Video duration differs')
    require(a['codec_name'] == 'aac' and int(a['sample_rate']) == 44100 and a['channels'] == 1, 'Narration delivery must be one mono 44.1kHz AAC stream')
    decode(path)
    x, y = pcm(master), pcm(path)
    require(abs(len(x)/44100-seconds) < .002, 'Approved WAV master duration differs')
    require(abs(len(y)-len(x))/44100 < .05, 'Decoded narration length differs beyond codec padding')
    match = audio_match(x, y)
    return {'file': name, 'video_duration_seconds': float(v['duration']),
            'container_duration_seconds': float(meta['format']['duration']),
            'decoded_frames': frames, 'dimensions': [1280, 720], 'fps': '24/1',
            'audio_streams': 1, 'audio_sample_rate': 44100, 'audio_channels': 1,
            'full_decode': 'passed', 'approved_wav': str(master.relative_to(ROOT)).replace('\\', '/'),
            'approved_master_correlation': match, 'sha256': sha(path)}


def verify_voice_and_stems():
    lock = jread(ROOT/'audio/voice_lock.json')
    for key, expected in EXPECTED.items():
        require(lock[key] == expected, 'Voice lock differs at '+key)
    require(lock['speed_changes_per_segment_allowed'] is False and lock['post_tempo_retiming_allowed'] is False, 'Voice lock permits retiming')
    approved = PROJECT/lock['approved_source_audio']
    require(sha(approved) == lock['approved_source_sha256'], 'Approved source audio hash differs')
    settings_path = PRODUCTION/'voice_demo/settings_polished_american.json'
    require(sha(settings_path) == lock['voice_source_settings_sha256'], 'Approved source settings hash differs')
    settings = jread(settings_path)
    for key in ('voice_id', 'model', 'speed', 'pitch', 'volume', 'sample_rate', 'bitrate'):
        require(settings[key] == lock[key], 'Voice does not match approved sample settings: '+key)
    # A distributable archive deliberately excludes credential-selection files.
    # Their absence does not weaken the locked per-generation provenance below.
    selector = PRODUCTION/'credential_selection.json'
    if selector.is_file():
        require(jread(selector)['key_name'] == 'MINIMAX_KEY_2', 'Current project selector differs from key2')
        selector_status = 'Present; key name verified as MINIMAX_KEY_2'
    else:
        selector_status = 'Unavailable in offline package; recorded generation manifests remain required'
    manifests = [('demo', jread(ROOT/'audio/demo/demo_manifest.json')),
                 ('narrative', jread(ROOT/'audio/narrative/narrative_manifest.json'))]
    records, fingerprints = [], set()
    for folder, manifest in manifests:
        for key, expected in EXPECTED.items():
            require(manifest['voice_settings'][key] == expected, f'{folder} settings differ at {key}')
        for stem in manifest['stems']:
            path = ROOT/'audio'/folder/stem['file']
            require(sha(path) == stem['sha256'], 'Generated stem hash differs: '+stem['id'])
            require(stem.get('api_voice_id', stem.get('voice_id')) == EXPECTED['voice_id'], 'Stem voice differs')
            require(stem.get('api_speed', stem.get('speed')) == 1.04, 'Stem speed differs')
            require(stem.get('api_pitch', stem.get('pitch')) == -1, 'Stem pitch differs')
            require(stem['key_name'] == 'MINIMAX_KEY_2', 'Stem generation key differs')
            require(stem['tempo_adjustment'] == 1., 'Stem has a post-tempo change')
            fingerprints.add(stem['voice_fingerprint'])
            require(stem['text_sha256'] == hashlib.sha256(stem['text'].encode()).hexdigest(), 'Stem script hash differs')
            s = next(s for s in probe(path)['streams'] if s['codec_type'] == 'audio')
            require(int(s['sample_rate']) == 44100 and s['channels'] == 1, 'Stem audio format differs')
            decode(path)
            records.append({'id': stem['id'], 'natural_duration_seconds': stem['natural_duration_seconds'],
                            'voice_id': EXPECTED['voice_id'], 'speed': 1.04, 'pitch': -1,
                            'tempo_adjustment': 1., 'key_name': 'MINIMAX_KEY_2', 'full_decode': 'passed'})
    require(len(records) == 18 and len(fingerprints) == 1, 'Expected eighteen stems with one voice settings fingerprint')
    return {'approved_source_hash_matches': True, 'locked_settings': EXPECTED,
            'stem_count': len(records), 'one_settings_fingerprint': True, 'stems': records,
            'project_selector_metadata': selector_status,
            'key_verification_scope': 'Locked voice and per-stem generation metadata; project selector additionally checked when present. No secret credential files read'}


def normalize(text):
    text = text.lower().replace('’', "'")
    text = re.sub(r'\binsight\s*gen\b', 'insightgen', text)
    text = re.sub(r'\bc[\s-]*(?:sixty|60)\b', 'c60', text)
    text = re.sub(r'\bs\s+q\s+l\b', 'sql', text)
    # Keep English contractions intact, as in the recorded ASR comparison.
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text)


def verify_words_and_cues():
    story = jread(ROOT/'edit/story.json')
    demo = jread(ROOT/'audio/demo/demo_manifest.json')
    narrative = jread(ROOT/'audio/narrative/narrative_manifest.json')
    paragraphs = re.split(r'\n\s*\n', (PROJECT/'insightGen_demo_voiceover_v2.txt').read_text(encoding='utf-8-sig').strip())
    require([s['text'] for s in demo['stems']] == paragraphs, 'Demo paragraphs changed')
    expected_narrative = [story['opening']['narration']]+[c['narration'] for c in story['under_the_hood']['cues']]
    require([s['text'] for s in narrative['stems']] == expected_narrative, 'Opening/underhood script differs from produced stems')
    boundaries = [s['nominal_start_seconds'] for s in demo['stems']]+[demo['stems'][-1]['nominal_end_seconds']]
    require(boundaries == [0,12,23,33,47,58,67,80,92,99], 'Demo reference boundaries differ')
    wav = ROOT/'audio/demo/insightgen_demo_v2_approved_voice.wav'
    require(abs(float(probe(wav)['format']['duration'])-101.283356) < .002, 'Demo master length differs')
    over = [{'id': s['id'], 'overrun_seconds': s['window_overrun_seconds']} for s in demo['stems'] if s['window_overrun_seconds'] > .001]
    require([r['id'] for r in over] == ['demo_07', 'demo_09'], 'Unexpected demo overrun set')
    require(demo['recording_sync'].lower().find('unavailable') >= 0 and demo['overrun_requires_owner_review'] is True, 'Recording alignment limitation is not recorded')
    qdir = ROOT/'audio/narrative/qc'
    expected = (qdir/'expected_all_narration.txt').read_text(encoding='utf-8-sig')
    recognized = jread(qdir/'all_narration_transcription.json')
    a, b = normalize(expected), normalize(recognized['text'])
    require(a == b and len(a) == 392, 'Independent normalized ASR wording comparison differs')
    require(recognized['n_speakers'] == 1, 'ASR did not detect one speaker')
    index = jread(qdir/'asr_source_index.json')
    require(len(index['source_files']) == 18, 'ASR source index must cover all eighteen stems')
    for row in index['source_files']:
        require(sha(ROOT/'audio'/row['path']) == row['sha256'], 'ASR source stem changed after transcription')
    return {'demo_unchanged': True, 'reference_boundaries_seconds': boundaries,
            'demo_master_seconds': 101.283356, 'demo_window_overruns': over,
            'recording_alignment': 'Owner review required; complete revised recording unavailable',
            'normalized_expected_words': len(a), 'normalized_recognized_words': len(b),
            'normalized_asr_differences': 0, 'asr_source_stems': 18, 'asr_speakers': 1,
            'manual_listening': 'Not performed by verifier'}


def verify_sources_and_typography():
    story = jread(ROOT/'edit/story.json')
    cuts = story['visual_cutlist']
    require(cuts[0]['start'] == 0 and cuts[-1]['end'] == 70, 'Cutlist must span seventy seconds')
    for a, b in zip(cuts, cuts[1:]):
        require(a['end'] == b['start'], 'Visual cutlist has a gap or overlap')
    groups, sources = {}, []
    # Resolve portable repository-relative story sources, not machine-specific
    # absolute paths in optional render caches. Opening's 0-10s excerpt is fixed
    # by render_connected.prepare; new connectors use their complete video span.
    excerpts = [{'id': 'opening', 'source': 'v2/film/clean/shot1.mp4',
                 'source_range': [0, 10], 'start': 0, 'end': 14}]+cuts
    for cut in excerpts:
        name, source = cut['id'], cut['source']
        if source.startswith('v2/'):
            path = (PRODUCTION/'revision_v2'/source[3:]).resolve()
        elif source.startswith('new/'):
            path = (ROOT/'raw'/source[4:]).resolve()
        else:
            raise AssertionError('Unknown source prefix: '+source)
        text = str(path).replace('\\', '/').lower()
        require('/revision_v3_cinematic/' not in text and '/rejected/' not in text, 'Rejected v3 imagery is a source')
        allowed = path.is_relative_to((PRODUCTION/'revision_v2').resolve()) or path.is_relative_to((ROOT/'raw').resolve())
        require(allowed, 'Unexpected source outside v2 or new handoff plates')
        require(path.is_file(), 'Source plate missing')
        video = next(s for s in probe(path)['streams'] if s['codec_type'] == 'video')
        source_duration = float(video['duration'])
        start, end = cut.get('source_range', [0, source_duration])
        require(0 <= start < end <= source_duration+.001, 'Invalid or unavailable source interval')
        cache_path = ROOT/'clean'/(name+'.json')
        if cache_path.is_file():
            cache = jread(cache_path)
            require(all(abs(a-b) < .001 for a, b in zip(cache['source_range'], [start, end])), 'Render-cache source interval differs from cutlist')
            require(cache['target_seconds'] == cut['end']-cut['start'], 'Render-cache target duration differs from cutlist')
        for prior_start, prior_end in groups.setdefault(text, []):
            require(min(end, prior_end)-max(start, prior_start) <= .0001, 'A source interval is repeated')
        groups[text].append((start, end))
        sources.append({'id': name, 'source': str(path.relative_to(PRODUCTION)).replace('\\', '/'), 'source_range': [start, end], 'source_duration_seconds': source_duration, 'target_seconds': cut['end']-cut['start'], 'render_cache_available': cache_path.is_file()})
    typ = jread(ROOT/'edit/typography_audit.json')
    require(typ['all_fit'] and typ['items'] and all(t['fits'] for t in typ['items']), 'Typography exceeds checked bounds')
    actions = jread(ROOT/'edit/semantic_actions.json')
    require(actions['same_updated_skill']['lands_in_skill_foundry_library'] >= actions['validation_before_release'], 'Skill returns before validation')
    require(actions['same_updated_skill']['receiving_run_reacts'][-1] > actions['same_updated_skill']['copy_enters_next_agent_run'][-1], 'Receiving next run does not react after entry')
    return {'contiguous_visual_seconds': 70, 'source_excerpts_do_not_repeat': True,
            'rejected_v3_imagery_excluded': True, 'sources': sources,
            'checked_text_items': len(typ['items']), 'all_typography_within_bounds': True,
            'semantic_scope': 'Recorded action timing only; actual visible handoffs require separate visual review'}


def main():
    required = [ROOT/'insightgen_v3_connected_opening_narrated.mp4', ROOT/'insightgen_v3_connected_underthehood_narrated.mp4']
    if not all(p.is_file() for p in required):
        print('Verification deferred: final narrated exports are not both ready.', file=sys.stderr)
        return 2
    QC.mkdir(exist_ok=True)
    check('opening_export_and_unchanged_approved_master', lambda: verify_export(required[0].name, 14, 336, ROOT/'audio/narrative/insightgen_opening_approved_voice.wav'))
    check('underhood_export_and_unchanged_approved_master', lambda: verify_export(required[1].name, 70, 1680, ROOT/'audio/narrative/insightgen_underthehood_approved_voice.wav'))
    check('eighteen_stems_one_approved_voice_and_speed', verify_voice_and_stems)
    check('unchanged_demo_and_all_words_transcribed', verify_words_and_cues)
    check('source_variety_non_repetition_and_typography', verify_sources_and_typography)
    report = {'verified_at_utc': datetime.now(timezone.utc).isoformat(),
              'all_technical_checks_passed': all(r['passed'] for r in RESULTS), 'checks': RESULTS,
              'verification_api_calls': 0, 'secret_credential_files_read': False,
              'semantic_acceptance': 'Not asserted by technical checks; inspect business agency, concrete artifact handoffs and validated return in the actual final frames',
              'unverified': ['Owner-held revised recording and its cue synchronization', 'Final assembled whole-film joins', 'Human listening and final owner visual approval']}
    target = QC/'verification.json'
    target.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('Report: '+str(target), flush=True)
    return 0 if report['all_technical_checks_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
