# Execução e vida útil dos recursos

[Edição](../README.pt-br.md) · [English](execution.md)

## Modos dos aplicativos

Os caminhos abaixo são relativos a `examples/task-board-ecosystem/`. `launch.py` usa essa raiz como pasta de trabalho dos filhos. A entrada direta do TaskBoard também resolve `--db` relativo nessa raiz; caminho absoluto é preservado.

| App / modo | Entrada | Vida útil e conclusão observável | Dependências |
| --- | --- | --- | --- |
| TaskBoard / HTTP, padrão | `apps/TaskBoard/main.py --db PATH serve --host 127.0.0.1 --port 8765` | Processo até interrupção; `/health` identifica app e instância | Python local e caminho SQLite gravável |
| TaskBoard / CLI | `apps/TaskBoard/main.py --db PATH --token TOKEN create`, `list` ou `complete` | Uma invocação, com JSON ou erro/código explícito | Mesmo núcleo e banco; dispensa servidor HTTP |
| LegacyReports / HTTP, padrão | `apps/LegacyReports/reports.py --upstream URL serve --port 8766` | Serviço de relatórios até interrupção | Contrato HTTP público TaskBoard |
| LegacyReports / CLI | `apps/LegacyReports/reports.py --upstream URL report` | Um JSON ou erro de upstream; saída 0 ou 5 | Contrato HTTP público TaskBoard |

A seleção completa inicia os dois modos HTTP padrão, sem executar também a CLI. `list` descobre o registro de apps do launcher. O registro e os comandos são configuração Python do exemplo; Vulcan não obriga essa implementação nem um manifesto universal.

## Configuração

| Configuração | Padrão | Propriedade e significado |
| --- | --- | --- |
| Banco TaskBoard | `.runtime/tasks.sqlite3` na raiz do ecossistema | Arquivo de dados do operador; preservado no encerramento |
| `TASKBOARD_EDITOR_TOKEN` | `demo-editor` | Identidade didática com criação/leitura/conclusão |
| `TASKBOARD_READER_TOKEN` | `demo-reader` | Identidade de leitura; usada também pelo LegacyReports no upstream |
| `TASKBOARD_TOKEN` | Não definido | Padrão opcional da CLI TaskBoard; `--token` prevalece |
| `--task-port` | `8765` | Porta HTTP loopback, entre 1 e 65535 |
| `--report-port` | `8766` | Porta LegacyReports; diferente da anterior quando ambos executam |
| `--startup-timeout` | `10` segundos | Limite positivo e finito de prontidão por app |
| `--duration` | Não definido | Intervalo finito e não negativo depois da prontidão; ausente mantém execução |

Tokens de editor e leitor devem ser não vazios e diferentes. HTTP lê `Authorization: Bearer …`; a composição confiável resolve a identidade. Clientes não podem fornecer permissões ou contexto de ator no corpo. Código que constrói `Entity_ActorContext` diretamente integra a fronteira confiável dentro do processo; o exemplo não estabelece confiança em qualquer código carregado nesse processo. O contexto é congelado, valida tipos e recusa identidade não resolvida, desconhecida ou insuficiente. Prova de identidade de produção, rotação de token, TLS e implantação remota não foram avaliados.

## Inicialização, prontidão e falhas

`planApps` expande dependências numa ordem topológica determinística, informa apps desconhecidos e rejeita ciclos. Selecionar LegacyReports inclui TaskBoard. Ausência de dependência não é ignorada. Um identificador único da execução é passado aos dois processos filhos.

A prontidão exige `/health` com app esperado, `ready: true`, identificador da execução correspondente e filho ainda vivo. Serviço alheio numa porta ocupada não satisfaz essa condição. Aqui, prontidão significa composição inicial concluída e handler HTTP aceitando requisições; não promete disponibilidade futura de armazenamento ou upstream. Cada requisição continua tratando as falhas pertinentes.

Durante a inicialização, o launcher observa dependências já iniciadas; depois, observa todos os filhos. Falha de partida, timeout ou saída de um filho produzem falha não zero e limpeza dos demais filhos próprios. O registro não cria árvores de descendentes, containers externos ou daemons. Esses recursos exigiriam adaptador explícito de propriedade e vida útil, sem encerrar processos alheios pelo nome ou pela porta.

O launcher solicita encerramento dos filhos diretos, aguarda até três segundos por filho e força o encerramento de um filho próprio que não terminou. SIGTERM e Ctrl+C seguem a mesma limpeza. Interrupção não promete reversão de toda operação em andamento e nunca apaga o banco do operador. Conexões SQLite vivem por operação; handles de processos e recursos temporários dos testes têm liberação explícita.

## Projeções de falha

O contrato comportamental autoritativo está no [blueprint L2](../examples/task-board-ecosystem/docs/L2_MinervaBlueprints/blueprint.yaml). As projeções de canal estão em [Shared interaction](../examples/task-board-ecosystem/docs/Shared/interaction.pt-br.md). A CLI usa 0 para sucesso, 3 para recusa, 2 para erro de domínio/entrada, 4 para tarefa ausente e 5 para falha de armazenamento. Erros do parser/configuração também usam 2 e podem produzir instruções de uso em vez de JSON de domínio. LegacyReports reúne falhas de upstream no seu erro documentado, com saída 5.

A realização SQLite é síncrona. Não oferece identidade de job diferido, API de cancelamento, contrato de revisão otimista, transação entre bancos ou garantia de distinguir todo commit incerto possível. Uma exigência futura desses resultados precisa aparecer primeiro nas fontes L1/L2 e depois na implementação e nas verificações.

## Reproduzir o ciclo de vida

```bash
python run_examples.py test
python run_examples.py start --all --duration 1 --task-port 8875 --report-port 8876
```

A suíte verifica seleção completa e parcial, expansão de dependências, seleção inválida, ciclos, instância divergente, porta ocupada, limpeza após partida parcial e SIGTERM em POSIX. O fallback de encerramento forçado é verificado com um substituto controlado. Essa verificação não representa execução de todo comportamento possível de árvores de processos reais.
