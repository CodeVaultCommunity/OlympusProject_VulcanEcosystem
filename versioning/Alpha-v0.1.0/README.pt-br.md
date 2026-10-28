# Vulcan Ecosystem — Alpha-v0.1.0

[English](README.md) · [Regras](specification/README.pt-br.md) · [Alinhamento OAL](specification/OAL-ALIGNMENT.pt-br.md) · [Verificação](verification/README.pt-br.md)

**Vulcan é um modelo reutilizável OAL L3 / ADI para organizar e realizar aplicações em código.** O manual inglês é normativo; este é sua tradução coordenada. Esta é a mesma Alpha-v0.1.0 ainda não publicada, melhorada no lugar. Não constitui nova versão nem plataforma de produção.

## Modelo e responsabilidades

Atlas L1 especifica contratos externamente significativos. Minerva L2 especifica o programa, a ADVS e as descrições por arquivo. Vulcan L3 realiza esses contratos, compõe colaboradores concretos e registra evidências de execução. Escolhas de interação pertencem a L4, inclusive código HTTP/CLI no artefato concreto. As [fontes fixadas](verification/source-baselines.json) identificam OAL Stable-v1.0.0, Atlas Stable-v1.0.0 e os insumos Minerva Alpha selecionados.

Um ecossistema DEVE ter `apps/`, pastas identificáveis dos aplicativos e um mecanismo funcional de entrada na raiz. Cada aplicativo declara linguagem, arquitetura, modos, operações públicas e escopo avaliado. Outras arquiteturas podem participar sem adotar [Vulcan Architecture](profiles/vulcan-architecture/README.pt-br.md). Bibliotecas, classes-base abstratas, containers e frameworks de injeção são opcionais.

## Organização

| Local no ecossistema instanciado | Responsabilidade |
| --- | --- |
| `apps/<App>/` | Código concreto da aplicação e testes. |
| `docs/L1_AtlasSpecifications/` | Contratos canônicos externamente significativos. |
| `docs/L2_MinervaBlueprints/` | Blueprint projetado e espelho de observação por arquivo. |
| `docs/L3_Vulcan/` | Organização, composição, execução, vínculos e referências de evidência. |
| `docs/Shared/` | Explicações compartilhadas, proveniência e escolhas L4 identificadas. |
| `launch.py` ou outra entrada na raiz | Registro/descoberta explícitos; modos padrão de todos ou seleção de aplicativos. |

Os nomes de documentação e `docs/` na raiz são recomendações. Outros locais devem manter a informação recuperável. A organização editorial deste repositório separa `specification/`, `profiles/`, `integrations/`, `guides/`, `templates/`, `examples/`, `scripts/`, `tests/` e `verification/` dentro da edição.

## Regras de referência

As [regras VUL-001 a VUL-030](specification/README.pt-br.md) identificam obrigações e seus escopos. As do perfil se aplicam somente aos aplicativos que o adotam. Descoberta pode usar um registro explícito; adicionar uma pasta não registra automaticamente um aplicativo. Consulte [execução](guides/execution.pt-br.md) para inicialização, propriedade de recursos e falhas.

## Início rápido

Use Python 3.11 ou superior. Aplicações, avaliação estrutural e testes usam a biblioteca padrão. A partir desta edição:

```sh
python run_examples.py list
python run_examples.py evaluate
python run_examples.py test
python run_examples.py start --example task-board --all --duration 10
```

Para a verificação completa entre modelos, instale `requirements.txt` e selecione explicitamente a edição externa compatível do Minerva:

```sh
python -m pip install -r requirements.txt
python run_examples.py verify --minerva-edition /caminho/L2-MinervaBlueprints/versioning/Alpha-v0.1.0
```

Não há validador embutido em `vendor/`. Minerva ausente ou incompatível produz integração inconclusiva e saída geral diferente de zero. O comando valida artefatos existentes; não traduz nem gera modelos/código. Cada verificação cria um diretório único em `verification/runs/`; `--report-dir` exige local novo/vazio.

## Exemplos canônicos

| Exemplo | Origem e propósito |
| --- | --- |
| [minimal](examples/minimal/README.pt-br.md) | Submissão de requisição: código exato, quantidade positiva, recusa de duplicata e gravações incertas. |
| [composition](examples/composition/README.pt-br.md) | Consulta/criação/cancelamento de reserva: composição com o mesmo contexto e gravações condicionais por versão. |
| [task-board](examples/task-board/README.pt-br.md) | IDs de tarefas informados pelo chamador, isolamento de quadro, conflitos de revisão, retenção e listagem consistente. |

Os três preservam os bytes correspondentes do Atlas e os IDs lógicos/de cenários do Minerva. O antigo TaskBoard divergente e LegacyReports estão em uma [fixture técnica](tests/fixtures/legacy-ecosystem/README.pt-br.md), para verificar inicialização heterogênea e integração pública. As [fixtures negativas](tests/fixtures/structural-counterexamples/README.pt-br.md) exercitam o avaliador limitado. As variantes de evolução revision-2/revision-3 do Atlas não são exemplos Vulcan executáveis adicionais nesta Alpha.

## Integração e evolução

A [integração Minerva](integrations/minerva/README.pt-br.md) explica derivação manual, decisões, aliases, fixação de fontes, mapeamento de testes e análise de impacto. Entrega somente documentação. Uma revisão local dos vínculos acrescenta observações do código sem alterar a ADPM ou a intenção dos cenários herdados. Mudanças de fonte exigem revisão semântica explícita, novos vínculos e evidências; atualizar um hash, sozinho, não autoriza mudança semântica.

## Conformidade e verificação

Alegações DEVEM nomear edição, referência OAL, perfil selecionado, alvo, regras aplicáveis, evidências e limites. Inspeção estrutural, validação Minerva, execução de cenários e aceite do responsável têm significados distintos. Cenários ausentes são `not_run`; testes ignorados permanecem registrados. [Avaliação](guides/assessment.pt-br.md), [requisitos](verification/REQUIREMENTS.pt-br.md) e o [recibo atual de verificação](verification/RELEASE.pt-br.md) delimitam resultados.

`model.json`, `realization.json` e `test-bindings.json` são escolhas documentais deste repositório, não schemas universais obrigatórios de L3. Os testes observam Python/SQLite local e canais selecionados. Não estabelecem identidade de produção, garantias distribuídas, suporte C/Go ou SLA de produção.

## Versionamento

Manter `Alpha-v0.1.0` e os metadados Python `0.1.0a0`. Futuras edições publicadas devem preservar bytes históricos. Esta revisão melhora o candidato não publicado no lugar; veja [migração](verification/MIGRATION.pt-br.md). A edição executa suas verificações L3 sem os scripts da raiz; integração ainda exige o validador Minerva externo explicitamente selecionado.

<a id="release-notes"></a>
## Notas da versão

Exemplos canônicos substituem o exemplo de negócio divergente; integrações são explicativas; há manuais EN/PT na raiz e na edição; avaliação de dependências no Windows e evidência por cenário foram corrigidas. Não há motor de tradução, nova edição, publicação remota ou aceite automático.
