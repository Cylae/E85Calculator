"""Run native tests on an available iPhone simulator. No signed device build."""
from pathlib import Path
import subprocess
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
result=subprocess.run(['xcrun','simctl','list','devices','available','--json'],capture_output=True,text=True,check=True)
devices=json.loads(result.stdout)['devices']
candidates=[d for runtime,items in devices.items() if 'iOS' in runtime
            for d in items if d.get('isAvailable') and 'iPhone' in d['name']]
if not candidates:raise SystemExit('No iPhone simulator available. Install an iOS runtime in Xcode.')
selected=candidates[0]
print('Simulator: '+selected['name'],flush=True)
subprocess.run(['xcodebuild','-project',str(ROOT/'ios/AygoBlend.xcodeproj'),'-scheme','AygoBlend',
    '-destination','platform=iOS Simulator,id='+selected['udid'],'-derivedDataPath',str(ROOT/'DerivedData'),
    'CODE_SIGNING_ALLOWED=NO','test'],check=True)
