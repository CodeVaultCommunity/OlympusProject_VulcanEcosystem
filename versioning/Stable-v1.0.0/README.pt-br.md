# Vulcan Ecosystem · Stable-v1.0.0

O Vulcan é a realização executável L3 de um projeto Minerva Stable-v1.0.0.
Cada exemplo mantém a árvore Markdown distribuída completa do Minerva em
`docs/L2_MinervaBlueprints/`; nenhum resumo separado substitui esses módulos.

Cada módulo Minerva com modo `code` ou `test` possui exatamente um arquivo e
símbolo Python. `realization.json` registra a origem Markdown, referências do
Atlas, alvo, hash e modo de realização. O grafo do Vulcan preserva todo o grafo
do Minerva e acrescenta as arestas `realized_by` até o código.

Ferramentas abstratas viram protocolos; projetos de ferramentas concretas
viram adaptadores executáveis sobre implementações SQLite verificadas.
`Boundary` continua significando exclusivamente adaptador de interação que
expõe casos de uso. Cenários usam `observation_points`.

```powershell
vulcan-generate examples/minimal
vulcan-validate examples/minimal
python run_examples.py
python scripts/validate_ecosystem.py
```

Veja o [manual canônico em inglês](README.md) para o contrato e a estrutura.
Distribuído sob a [licença MIT](LICENSE).

