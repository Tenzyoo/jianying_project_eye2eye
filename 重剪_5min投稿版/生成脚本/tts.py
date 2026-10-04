import sherpa_onnx, soundfile as sf, os, json, sys
sys.path.insert(0,'.'); import script
d='kokoro-en-v0_19/'
tts=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=d+'model.onnx',voices=d+'voices.bin',tokens=d+'tokens.txt',data_dir=d+'espeak-ng-data'),num_threads=4)))
VOICE={'N':3,'AI':4,'U':6}   # af_sarah / af_sky / am_michael
SPEED={'N':1.0,'AI':1.0,'U':1.0}
os.makedirs('tts',exist_ok=True); meta={}
for s in script.S:
    for i,l in enumerate(s['lines']):
        sp,txt=l[0],l[1]; t=l[2] if len(l)>2 else txt
        fn=f"tts/{s['id']}_{i}_{sp}.wav"
        a=tts.generate(t.replace('"',''),sid=VOICE[sp],speed=SPEED[sp])
        sf.write(fn,a.samples,a.sample_rate); meta[fn]=len(a.samples)/a.sample_rate
        print(fn, round(meta[fn],2), flush=True)
json.dump(meta,open('tts/meta.json','w'),indent=1)
print('TOTAL speech', round(sum(meta.values()),1))
