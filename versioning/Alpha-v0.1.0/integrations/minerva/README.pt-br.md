# Minerva → Vulcan: procedimento de realização manual

[English](README.md) · [Modelo](../../README.pt-br.md) · [Exemplos canônicos](../../examples/README.pt-br.md)

Alvos: Minerva Alpha-v0.1.0 / perfil YAML 0.1.0 e Vulcan Alpha-v0.1.0. Este guia descreve as decisões de tradução; não implementa um tradutor. Os três programas de exemplo foram escritos e revisados como realizações concretas.

1. Selecionar edição-fonte, ID/revisão do documento, origem Atlas e hashes exatos. Preservar o blueprint original como snapshot de entrada. Registrar dúvidas das fontes antes de escrever código.
2. Inventariar casos, políticas dos atores, entidades, ferramentas, dependências, cenários ADVS e apoios compartilhados. Manter identidades de casos e critérios; um canal não cria outro caso lógico.
3. Selecionar aplicativos, perfis e adaptações de linguagem. Alocar casos em domínios declarados, validade canônica em entidades, capacidades de infraestrutura em ferramentas e seleção/injeção concreta na composição.
4. Registrar nomes operacionais, representações, ausência/falhas e injeções técnicas. Preservar ordem de validação, texto exato, composição com o mesmo contexto e certeza das gravações. Documentar desvios semânticos propostos e encaminhar revisão da fonte; observações de código não substituem intenção silenciosamente.
5. Escrever o núcleo invocável e os canais selecionados. Escolher recursos/transações que cumpram as garantias da fonte. Declarar confiança da identidade, propriedade/vida útil dos recursos, configuração, prontidão e encerramento.
6. Implementar cada cenário ADVS e apoio compartilhado. Manter mapeamento para caminho e símbolo do teste; distinguir teste escrito de execução observada. Acrescentar testes de canais e execução separadamente.
7. Descrever cada arquivo-fonte selecionado no espelho L2. Manter a extensão completa (`Entity_Task.py.yaml`). Observações incluem hashes e símbolos léxicos; não inferem requisitos dos interessados. Composição/evidência L3 permanece em `docs/L3_Vulcan/`.
8. Executar avaliação estrutural, validador Minerva selecionado, cenários e verificações dos canais. Registrar ausências, falhas, testes ignorados e resultados incertos. Revisar mudanças das fontes e atualizar observações afetadas antes de criar nova execução de evidência.

| Elemento Minerva | Local / decisão concreta |
| --- | --- |
| Identidade, algoritmo e autorização do caso | `apps/<App>/usecases/Main/UseCase_*.py`; um método invocável por caso selecionado. `Main` é a pasta concreta de domínio; estes blueprints não selecionam domínio nomeado. |
| Invariantes e transições das entidades | `entities/Entity_*.py`; value objects encapsulados opcionais. |
| Capacidade e garantia de falha da ferramenta | `tools/Tool_Sqlite*Store.py`; transações/bloqueio em `support/SqliteResource.py`. |
| Dependências abstratas | Injeção por construtor escolhida em `composition/AppComposition.py`; cancelamento de reserva recebe a consulta e encaminha o mesmo contexto. |
| task_identifier operacional | Parâmetro/campo nativo `task_id`; valor preservado exatamente. |
| Quadro autorizado | `board_id` da instância concreta da ferramenta, fixado na composição; cada caso TaskBoard verifica o contexto confiável correspondente. |
| Identidade do teste comportamental e cenário | `docs/L3_Vulcan/test-bindings.json` e IDs de subtestes; sete testes lógicos podem ter vários métodos nativos. |
| ADPM/ADVS projetadas | Original exato em `verification/sources/minerva/`; revisão L2 local `<fonte>-vulcan-1` acrescenta observações sem mudar comportamento pretendido. |
| Execução | `verification/runs/<id>/` imutável, com hashes de entradas/fontes, ambiente e resultados de subtestes. Executar testes não reescreve o blueprint. |

O blueprint local é `mixed`: ADPM e intenção dos cenários são projeto herdado; espelhos por arquivo são observações das fontes. Assinaturas nativas e passos léxicos descrevem implementação, enquanto tipagem operacional e contratos semânticos continuam na ADPM. A decisão de revisão pendente pelo responsável é preservada.

O validador externo Minerva é selecionado por `--minerva-edition`. Edição/perfil declarados e hashes das fontes são registrados; dependências ausentes ou edição incompatível impedem aprovação completa. A validação é de leitura e não implementa este procedimento de derivação. Ela confere o catálogo declarado; não interpreta/prova independentemente cada requisito Atlas.
