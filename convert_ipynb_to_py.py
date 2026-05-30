import json
from pathlib import Path

root = Path(__file__).parent
paths = [
    'src/temporal_decay/temporal_decay_tokyo.ipynb',
    'src/temporal_decay/temporal_decay_kyoto.ipynb',
    'src/scaling/scaling_tokyo.ipynb',
    'src/scaling/scaling_kyoto.ipynb',
    'src/case/case_tokyo.ipynb',
    'src/case/case_kyoto.ipynb',
    'src/returner_explorer/returner_explorer_tokyo.ipynb',
    'src/returner_explorer/returner_explorer_kyoto.ipynb',
    'src/ratio/ratio_tokyo.ipynb',
    'src/ratio/ratio_kyoto.ipynb',
    'src/ratio/ratio_fukuoka_kumamoto_kagoshima.ipynb',
    'src/distance/distance_tokyo.ipynb',
    'src/distance/distance_kyoto.ipynb',
    'data/shapefile/extract_tokyo.ipynb',
    'data/shapefile/extract_four_cities.ipynb',
]

for rel_path in paths:
    ip = root / rel_path
    with ip.open('r', encoding='utf-8') as f:
        nb = json.load(f)

    lines = []
    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type', '')
        source = ''.join(cell.get('source', []))
        if cell_type == 'markdown':
            lines.append('#' + '-' * 78)
            for line in source.splitlines():
                lines.append('# ' + line)
            lines.append('#' + '-' * 78)
            lines.append('')
        elif cell_type == 'code':
            if source.strip():
                lines.append(source.rstrip())
            lines.append('')

    out_path = ip.with_suffix('.py')
    out_path.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')
    print(f'Wrote {out_path}')
