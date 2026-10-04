"""Structural checks of deliverables. Native compilation requires each platform SDK."""
from pathlib import Path
import re
import json
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from math import isclose

ROOT=Path(__file__).resolve().parents[1]
md=(ROOT/'reports/Report_Toyota_Aygo_E85_SP98.md').read_text()
pdf=PdfReader(ROOT/'reports/Report_Toyota_Aygo_E85_SP98.pdf')
assert len(pdf.pages)==16
texts=[p.extract_text() or '' for p in pdf.pages]
assert all(len(t)>500 for t in texts)
joined='\n'.join(texts)
for required in ('10.9375','31.666666','23.333333','58.33','54','no guarantee'):
    assert required.lower() in joined.lower(),required
assert len([a for p in pdf.pages for a in p.get('/Annots',[])]) >= 8
for bad in ('PLACEHOLDER','URL_IMAGE','[Link here]','INSERT_BLEND_ENGINE'):
    assert bad not in md
engine=(ROOT/'verification/blend.js').read_text().strip()
html=(ROOT/'web/index.html').read_text()
embedded=html.split('/* ENGINE_START */',1)[1].split('/* ENGINE_END */',1)[0].strip()
assert embedded==engine
assert 'INSERT_BLEND_ENGINE' not in html
assert '<html lang="en">' in html
ET.parse(ROOT/'android/app/src/main/AndroidManifest.xml')
assert 'android.permission.INTERNET' not in (ROOT/'android/app/src/main/AndroidManifest.xml').read_text()
ET.parse(ROOT/'ios/AygoBlend.xcodeproj/xcshareddata/xcschemes/AygoBlend.xcscheme')
pbx=(ROOT/'ios/AygoBlend.xcodeproj/project.pbxproj').read_text()
definitions=re.findall(r'^\s*([A-F0-9]{24}) = \{',pbx,re.M)
assert len(definitions)==len(set(definitions))
references=set(re.findall(r'\b[A-F0-9]{24}\b',pbx))
assert references==set(definitions)
for filename in ('AygoBlendApp.swift','ContentView.swift','BlendEngine.swift'):
    assert (ROOT/'ios/AygoBlend'/filename).is_file()
assert (ROOT/'ios/AygoBlendTests/BlendEngineTests.swift').is_file()
assert (ROOT/'android/app/src/test/java/com/cylae/aygoblend/BlendEngineTest.kt').read_text().count('@Test')==20
assert (ROOT/'ios/AygoBlendTests/BlendEngineTests.swift').read_text().count('    func test')==20
vectors=json.loads((ROOT/'verification/test_vectors.json').read_text())
assert len(vectors)==18
# Independently verify the central E30 equation with Decimal arithmetic.
from decimal import Decimal,localcontext
with localcontext() as context:
    context.prec=45
    c=Decimal(35);r=c/3;a=c-r
    x=(c*Decimal('.30')-r*Decimal('.05')-a*Decimal('.05'))/Decimal('.80')
    assert abs(x-Decimal('10.9375'))<Decimal('1e-40')
    y=a-x
    ethanol=(r*Decimal('.05')+x*Decimal('.85')+y*Decimal('.05'))/c
    assert abs(ethanol-Decimal('.30'))<Decimal('1e-40')
result=dict(status='passed',pdfPages=len(pdf.pages),pdfLinks=len([a for p in pdf.pages for a in p.get('/Annots',[])]),
            sourceVectors=18,nativeTestsPerPlatform=20,xcodeObjects=len(definitions),embeddedEngineIdentical=True,
            nativeCompilation='not_run_in_authoring_environment')
print(json.dumps(result,ensure_ascii=False))
