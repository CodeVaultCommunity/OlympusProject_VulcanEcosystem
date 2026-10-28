# Ecossistema TaskBoard — realização executável

[English](README.md) · [Manual da edição](../../README.pt-br.md)

Este ecossistema Vulcan instanciado contém dois apps. TaskBoard adota Vulcan Architecture; LegacyReports mantém interior procedural. Ambos podem executar juntos ou pelo subconjunto necessário. O código não depende de framework Vulcan.

## Executar nesta pasta

```bash
python launch.py list
python launch.py start --all
python launch.py start --apps TaskBoard
python launch.py start --apps LegacyReports --duration 2
```

TaskBoard usa `http://127.0.0.1:8765/`; relatórios usam `http://127.0.0.1:8766/report`. O launcher seleciona somente loopback. Tokens didáticos padrão são `demo-editor` e `demo-reader`; configuração e confiança estão no [guia de execução](../../guides/execution.pt-br.md). Ctrl+C encerra os filhos próprios e preserva o banco.

## Superfícies diretas dos casos

```bash
python apps/TaskBoard/main.py --token demo-editor create --title "Ler o contrato"
python apps/TaskBoard/main.py --token demo-reader list
python apps/TaskBoard/main.py --token demo-editor complete TASK_ID
python apps/LegacyReports/reports.py report
```

O relatório exige o serviço HTTP público TaskBoard ativo; a CLI TaskBoard pode operar diretamente sem servidor. Seus comandos compartilham o banco selecionado. `--db` relativo é resolvido nesta raiz do ecossistema.

## Ler as fontes por camada

| Localização | Conteúdo |
| --- | --- |
| [Atlas L1](docs/L1_AtlasSpecifications/README.pt-br.md) | Casos e critérios reconstruídos especificamente para o exemplo |
| [Blueprint Minerva L2](docs/L2_MinervaBlueprints/blueprint.yaml) | Contratos de programa/ADVS, fontes e grafos |
| `docs/L2_MinervaBlueprints/apps/` | Um YAML por arquivo de código, incluindo as unidades reais do legado |
| [Vulcan L3](docs/L3_Vulcan/README.pt-br.md) | Inventário, perfis, composição concreta, recursos, execução e evidências |
| [Interação Shared, L4](docs/Shared/interaction.pt-br.md) | Botões, rotas e comandos ligados aos casos preparados e handlers reais |

O blueprint foi reconstruído a partir da implementação didática e de sua fonte Atlas específica. Não presume que o Task Board publicado pelo Atlas tenha entradas, geração de identidade ou atualização equivalentes.

A verificação completa usa `python run_examples.py verify` na raiz da edição, ou caminho absoluto para esse script a partir de outra pasta. Somente a suíte dos apps pode ser executada aqui:

```bash
python -m unittest discover -s apps/TaskBoard/tests -p 'Test_*.py' -v
```

São 19 métodos na suíte dos apps; a edição completa também verifica o avaliador estrutural. [Verificação](../../verification/README.pt-br.md) identifica relatórios autoritativos e limites. A demonstração não inclui implantação, identidade de produção, Docker ou testes completos de navegador.
