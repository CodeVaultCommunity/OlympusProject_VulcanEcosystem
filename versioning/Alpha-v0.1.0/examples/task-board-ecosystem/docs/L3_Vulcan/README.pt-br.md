# Realização do ecossistema TaskBoard — L3

[English](README.md) · [Registro de realização](realization.json) · [Exemplo](../../README.pt-br.md)

Este documento registra a organização e a operação concretas. Programa, fluxos, contratos, cenários e espelho por arquivo canônicos estão em [Minerva L2](../L2_MinervaBlueprints/blueprint.yaml). L1 é [a instância Atlas reconstruída](../L1_AtlasSpecifications/task-board.atlas.json), não o exemplo Task Board publicado independentemente. A projeção da interação continua [identificada como L4](../Shared/interaction.pt-br.md).

## Inventário e perfil

| App | Organização interna | Modos | Escopo avaliado |
| --- | --- | --- | --- |
| TaskBoard | Vulcan Architecture em Python; composição, testes e boundaries L4 como suporte | HTTP padrão e CLI direta | 14 fontes Python inspecionadas, três casos selecionados e verificações complementares |
| LegacyReports | Estilo procedural/de módulo; funções e handler no mesmo `reports.py` | HTTP padrão e CLI de relatório | Integração pública e ciclo de vida; sem conformidade interna Vulcan Architecture |

O código reside em `apps/`. Não existe biblioteca abstrata obrigatória. O legado permanece multiunidade, descrito fielmente pelo Minerva. Hashes e descrições de membros permanecem autoritativos em L2, sem repetição neste documento.

## Composição concreta

`apps/TaskBoard/composition/AppComposition.py` seleciona `Tool_SqliteTaskStore` para `TOL-TASK-STORE` e constrói as realizações de `UC-TASK-001`, `UC-TASK-002` e `UC-TASK-003`. Cada caso recebe o store diretamente. A entrada principal entrega os casos preparados e o resolvedor confiável de contexto à boundary selecionada.

A geração UUID, SQLite e ordem de inserção são escolhas vinculadas ao blueprint selecionado. A ferramenta constrói a entidade canonicamente antes da inserção; essa construção não foi transferida para o caso de criação. A entidade delega validade de título ao value object interno. O [relatório estrutural](../../../../verification/structure.json) registra o grafo concreto; Minerva registra seu significado lógico.

Conexões SQLite são abertas e fechadas por operação. O arquivo persiste entre composições e pertence ao operador. Servidores HTTP possuem sockets; o launcher possui apenas os processos diretos que cria. A recusa de domínio precede o acesso ao store nos casos, enquanto a composição de infraestrutura pode preparar o schema antes das requisições.

## Execução e integração

`launch.py` na raiz descobre os apps e inicia todos os modos padrão ou um subconjunto. Sua política expande LegacyReports para incluir TaskBoard, rejeita ciclos e verifica instâncias pelo metadado de saúde. Limpa filhos próprios após falha de partida, interrupção ou saída de filho gerenciado. Não controla daemons externos nem apaga o banco.

LegacyReports consome a operação HTTP pública do TaskBoard com identidade de leitura, sem imports privados ou acesso direto ao banco. A representação de transporte está em [interação](../Shared/interaction.pt-br.md). O [guia de execução](../../../../guides/execution.pt-br.md) descreve comandos, pasta de trabalho, configuração, prontidão, conclusão e encerramento dos modos.

## Fontes, rastreabilidade e evidências

A realização seleciona Minerva Blueprints `Alpha-v0.1.0`, perfil YAML `0.1.0`, documento `MINERVA-TASKBOARD`, revisão `1`. O blueprint seleciona Atlas `Stable-v1.0.0`, documento `ATLAS-VULCAN-TASKBOARD`, revisão `1`. [Fontes congeladas e hashes](../../../../verification/source-baselines.json) ficam na edição.

Os vínculos comportamentais são `BT-TASK-001` → `Test_TaskCases.testCreateTask`, `BT-TASK-002` → `testListTasks` e `BT-TASK-003` → `testCompleteTask`. Os demais testes apoiam ordem de autorização, valores canônicos, falhas selecionadas, canais, integração e ciclo de vida. Critérios e cenários esperados permanecem na ADVS; [execution.json](../../../../verification/execution.json) informa a execução real. [minerva.json](../../../../verification/minerva.json) registra a verificação L2/vínculo de código separada.

O escopo não inclui interação completa no navegador, C/Go, Docker, identidade de produção, transações distribuídas ou CI hospedada. O [exercício de impacto](change-impact.pt-br.md) mostra como preservar responsabilidades numa mudança. Aprovar estrutura ou schema não amplia silenciosamente essas declarações.
