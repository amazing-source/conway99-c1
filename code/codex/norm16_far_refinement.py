"""Apply note253 to the archived 15 forests, preserving their identifiers."""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

source = json.loads((ROOT/'data/codex_norm16_far_forest.json').read_text())
forests = [f for f in source['forests'] if f['isolates'] > 0]
ids = {f['id'] for f in forests}
configurations = [c for c in source['configurations_27'] if c['far_forest_id'] in ids]
result = {'scope': 'Necessary refined list from note253: an isolated vertex in Z is forced. Not SRG completions.',
          'source': 'codex_norm16_far_forest.json', 'proof': 'notes/253_CODEX_NORM16_SOMMET_LOINTAIN_ISOLE.md',
          'removed_forest_ids': [f['id'] for f in source['forests'] if f['id'] not in ids],
          'forests': forests, 'configurations_27': configurations,
          'forest_count_by_edges_D': dict(Counter(str(f['edges_D']) for f in forests)),
          'seidel_rank_counts': dict(sorted(Counter(str(c['seidel_rank_mod7']) for c in configurations).items()))}
(ROOT/'data/codex_norm16_far_forest_refined.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'forests': len(forests), 'configurations': len(configurations),
                  'removed': result['removed_forest_ids'], 'seidel_ranks': result['seidel_rank_counts']}))
