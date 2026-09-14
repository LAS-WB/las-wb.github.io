import csv,json
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE/'repository'
rows=list(csv.DictReader((ROOT/'data/sweep/sweep-results.csv').open(encoding='utf-8-sig')))
choices=[
 ('https://renanpresidente.com.br','Renan Santos','readable candidate site; repository pilot participant'),
 ('https://eduardoriedel.com.br/','Eduardo Riedel','readable candidate site with recorded PDF links; pilot participant'),
 ('https://timebarra.com.br/','Time Barra / Eder Mauro','candidate-linked site with recorded PDF link; pilot participant'),
 ('https://flaviobolsonaro.com.br','Flavio Bolsonaro','readable page with structured-data and crawler-policy signals'),
 ('https://acmneto.com.br/','ACM Neto','readable site in the plain-content category'),
 ('https://renanfilhodealagoas.com.br','Renan Filho','second plain-content site'),
 ('https://acir.com.br/','Acir Gurgacz','near-empty original extraction; audited party-coverage withdrawal'),
 ('https://orleansbrandao.com.br/','Orleans Brandao','zero-word original extraction'),
 ('https://www.paulabelmonte.com.br','Paula Belmonte','recorded bot challenge'),
 ('https://novo.org.br/noticias/candidatos-partido-novo-2026-veja-a-lista/','NOVO candidate listing','shared party-hosted candidacy evidence'),
 ('https://pco.org.br/2026/08/08/pco-define-candidaturas-em-18-estados-e-no-distrito-federal-para-as-eleicoes-de-2026/','PCO candidate listing','second party-hosted candidacy article'),
 ('https://site.eduardoriedel.com.br/COMUNIDADES/','Eduardo Riedel communities page','recorded HTTP 404; tests failure reporting'),
]
coverage=list(csv.DictReader((ROOT/'data/party-coverage-tiered.csv').open()))
manifest=[]
for n,(url,label,why) in enumerate(choices,1):
 match=next((r for r in rows if r['url'].rstrip('/')==url.rstrip('/')),None)
 source='data/sweep/sweep-results.csv'
 if not match:
  candidates=[r for r in coverage if url in r['evidence_urls'].split(' | ')]
  assert candidates,url
  match={'url':url,'candidates':' | '.join(r['ballot_name'] for r in candidates)}
  source='data/party-coverage-tiered.csv'
 manifest.append({'id':f'{n:02d}','label':label,'url':match['url'],'selection_reason':why,'source_file':source,'original':match})
(BASE/'selected-urls.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
with (BASE/'selected-urls.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['id','label','url','selection_reason','source_file'],lineterminator='\n');w.writeheader();w.writerows({k:r[k] for k in w.fieldnames} for r in manifest)
print('Selected 12 URLs; purposive variation sample, not representative or a candidate ranking.')
