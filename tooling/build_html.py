from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
template=ROOT/'tooling/web_template.html'
engine=(ROOT/'verification/blend.js').read_text()
destination=ROOT/'web/index.html';destination.parent.mkdir(exist_ok=True)
destination.write_text(template.read_text().replace('/* INSERT_BLEND_ENGINE */',engine),encoding='utf-8')
print(destination)
