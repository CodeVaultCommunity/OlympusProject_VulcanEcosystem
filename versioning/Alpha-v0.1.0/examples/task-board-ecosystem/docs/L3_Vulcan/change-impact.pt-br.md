# Exercício de impacto de mudanças

**Estado: análise ilustrativa, sem mudança implementada.** Código e fontes selecionadas mantêm a regra atual de título. O registro demonstra VUL-028, sem alterar silenciosamente L1/L2.

## Exemplo A — propor outro limite de título

| Responsabilidade | Artefato/identidade afetados | Ação necessária antes de declarar a nova realização |
| --- | --- | --- |
| Obrigação L1 | `AC-TASK-001-INVALID` na instância Atlas selecionada | Decidir a exigência e revisar a fonte autoritativa; preservar a identidade do caso quando seu significado permanecer |
| Programa L2 | `RULE-TASK-TITLE`, `ENT-TASK`, construção canônica e algoritmo relacionado | Rever invariante e premissas das capacidades afetadas |
| Verificação L2 | `BT-TASK-001`, `SC-TASK-001-INVALID` e expectativas de canal | Definir valores positivos/negativos de fronteira e resultados antes de aceitar atualização da fonte |
| Implementação L3 | `ValueObject_TaskTitle.__post_init__` | Realizar o limite canônico uma vez; ferramentas continuam construindo canonicamente |
| Interação L4 | Restrição do formulário em `Boundary_Http.renderPage` e contrato de canal identificado | Alinhar restrição apresentada ao usuário com a exigência de domínio |
| Verificações L3 | `Test_TaskCases.testCreateTask`, `testCanonicalValuesAndContext`, `Test_Boundaries.testBrowserPageAndHttpFailureProjection` | Atualizar cenários afetados, executar testes reais e revisar compatibilidade |
| Espelho L2 / evidência L3 | Fichas por arquivo e relatórios | Atualizar hashes depois da reconciliação semântica; registrar nova execução sem apagar o significado histórico |

Mudança de arquivo ou implementação não exige automaticamente novo ID de caso. Conservar o ID também não prova preservação comportamental. Divergência não resolvida continua pendente, sem declaração falsa de conformidade.

## Exemplo B — mover arquivo sem mudar comportamento

Uma futura mudança de localização de `UseCase_CreateTask.py` preserva `UC-TASK-001` e seus critérios. Atualize imports/composição, vínculo físico e localização no espelho L2, além da referência de organização L3. Execute avaliação estrutural e testes afetados. Se a mudança viola `usecases/<Domain>/`, corrija o movimento ou revise explicitamente o perfil; mudar apenas o hash não resolve a divergência.

O exercício não moveu arquivos nem alterou o limite de título. A evidência atual refere-se à implementação sem essas mudanças, incluída nesta edição.
