<p align="center"><img src="assets/vulcan-banner-pt-br.png" alt="Vulcan Ecosystem · Olympus Project · Alpha-v0.1.0" width="100%"></p>

# Vulcan Ecosystem

[English](README.md) · [Manual da edição](versioning/Alpha-v0.1.0/README.pt-br.md) · [Verificação](versioning/Alpha-v0.1.0/verification/RELEASE.pt-br.md)

**Um modelo reutilizável OAL L3 / ADI para organizar e realizar aplicações em código.** Parte do Olympus Project, junto ao Atlas Specifications (L1) e Minerva Blueprints (L2). Esta introdução ilustrada aponta para o manual normativo inglês da edição e sua tradução portuguesa.

<img src="assets/vulcan-oal-position-pt-br.png" alt="Vulcan nas camadas OAL" width="900">

Atlas especifica comportamento requerido; Minerva modela o programa e sua verificação; Vulcan organiza implementação, composição, execução e evidências concretas. L4 define escolhas de interação. Referência: [OAL Stable-v1.0.0](https://github.com/CodeVaultCommunity/OAL_OpenAnalysisLayers), com [fontes exatas fixadas](versioning/Alpha-v0.1.0/verification/source-baselines.json).

<img src="assets/vulcan-model-pt-br.png" alt="Ecossistema e perfil arquitetural opcional" width="900">

Aplicativos declaram sua arquitetura. O perfil opcional Vulcan Architecture organiza casos de uso, ferramentas, entidades e value objects; outras arquiteturas participam por contratos públicos. Nenhuma biblioteca de apoio, classe-base ou container é exigido.

## Comece pelos mesmos exemplos do Atlas e Minerva

| Exemplo | Foco |
| --- | --- |
| [minimal](versioning/Alpha-v0.1.0/examples/minimal/README.pt-br.md) | Submissão de requisição, identidade exata, validação e persistência. |
| [composition](versioning/Alpha-v0.1.0/examples/composition/README.pt-br.md) | Consulta/criação/cancelamento de reserva e composição preservando contexto. |
| [task-board](versioning/Alpha-v0.1.0/examples/task-board/README.pt-br.md) | IDs informados pelo chamador, isolamento por quadro, conflitos de revisão e listagem consistente. |

O antigo TaskBoard divergente permanece apenas como fixture técnica de integração legada e inicialização. Os exemplos principais preservam os bytes canônicos do Atlas e as identidades correspondentes do Minerva.

```sh
cd versioning/Alpha-v0.1.0
python run_examples.py evaluate
python run_examples.py test
python run_examples.py start --example task-board --all --duration 10
```

Python 3.11+. Esses comandos L3 usam a biblioteca padrão. Integração completa exige também `requirements.txt` e uma edição Minerva externa explícita: veja o [manual](versioning/Alpha-v0.1.0/README.pt-br.md#início-rápido). Cada verificação registra ambiente, hashes das fontes e cenários executados.

<img src="assets/vulcan-workflow-pt-br.png" alt="Modelo selecionado, realização concreta e evidência observada" width="900">

[integrations/](versioning/Alpha-v0.1.0/integrations/README.pt-br.md) explica a derivação manual Minerva–Vulcan. Contém apenas documentação; nenhum tradutor ou gerador foi implementado. YAML por arquivo pertence a L2; L3 registra organização, recursos, execução e evidência.

## Organização do repositório

```text
L3-VulcanEcosystem/
├── README.md / README.pt-br.md
├── AGENTS.md / CLAUDE.md
├── CHANGELOG.md / VERSION / CONTENT-SHA256.json
├── LICENSE
├── assets/                 # illustrated introductions
├── docs/                   # maintenance, contribution, citation and acknowledgements
├── scripts/                # repository and distribution checks
└── versioning/Alpha-v0.1.0/
    ├── README.md / README.pt-br.md
    ├── specification/      # identified rules and OAL alignment
    ├── profiles/           # optional Vulcan Architecture profile
    ├── integrations/       # explanation only: Minerva → Vulcan
    ├── guides/ / templates/
    ├── examples/           # minimal, composition, task-board
    ├── scripts/ / tests/   # assessor, evidence runner, technical fixtures
    └── verification/       # requirements, source baselines, reviews, runs
```

A edição permanece **Alpha-v0.1.0**, melhorada no lugar antes da publicação. [Regras](versioning/Alpha-v0.1.0/specification/README.pt-br.md), [alinhamento OAL](versioning/Alpha-v0.1.0/specification/OAL-ALIGNMENT.pt-br.md), [requisitos](versioning/Alpha-v0.1.0/verification/REQUIREMENTS.pt-br.md) e [histórico](CHANGELOG.md) separam obrigações das fontes, decisões de projeto e verificações observadas.

## Integridade e contribuição

`CONTENT-SHA256.json` na raiz inventaria os bytes exatos da entrega. O [procedimento de entrega](docs/releasing.pt-br.md) explica preparação, verificação e commits locais. Testes são observações delimitadas, sem representar aceite dos interessados ou certificação de projetos futuros. Configuração de CI hospedada não demonstra que houve execução hospedada.

Concepção e autoria: Douglas de Oliveira Alkimim. Preparação e revisão técnica assistidas por IA. Veja [licença MIT](LICENSE), [citação](docs/CITATION.cff), [proveniência das imagens](assets/README.pt-br.md) e [contribuição](docs/CONTRIBUTING.pt-br.md).
