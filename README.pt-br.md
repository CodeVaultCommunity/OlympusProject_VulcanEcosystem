<p align="center"><img src="assets/vulcan-banner-pt-br.png" alt="Vulcan Ecosystem · Olympus Project" width="100%"></p>

# Vulcan Ecosystem

[English](README.md) · [Stable-v1.0.0](versioning/Stable-v1.0.0/README.pt-br.md) · [Verificação](versioning/Stable-v1.0.0/verification/RELEASE.pt-br.md)

O Vulcan é a realização executável OAL L3 do Minerva. A Stable-v1.0.0 consome
toda a árvore Markdown distribuída e liga cada alvo `code` ou `test` a um
arquivo e símbolo Python rastreável.

Cada exemplo contém a fonte Minerva, o ledger `realization.json`, um grafo de
conhecimento combinado, código executável e testes de contrato. Ferramentas
abstratas viram protocolos; projetos de ferramentas concretas viram adaptadores
SQLite verificados.

`Boundary` continua significando somente adaptador de interação que expõe casos
de uso. Cenários e instrumentação usam `observation_points`.

```powershell
cd versioning/Stable-v1.0.0
python -m pip install -e .
python run_examples.py
python scripts/validate_ecosystem.py
```

Os exemplos possuem 31 mapeamentos Minerva → código e 50 testes funcionais. A
auditoria transversal confirma payload Atlas sem perda, árvores Minerva
idênticas, símbolos/métodos/hashes válidos e ligações completas no grafo.

A edição histórica [Alpha-v0.1.0](versioning/Alpha-v0.1.0/README.pt-br.md)
permanece disponível. Concepção e autoria: Douglas de Oliveira Alkimim.
[Licença MIT](LICENSE) · [Guia de contribuição](CONTRIBUTING.pt-br.md).
