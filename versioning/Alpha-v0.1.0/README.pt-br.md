# Vulcan Ecosystem — Alpha-v0.1.0

**Modelo reutilizável L3 do OAL para organizar e realizar um ecossistema em código.** O Vulcan integra o Olympus Project, junto do Atlas Specifications (L1) e do Minerva Blueprints (L2). Vulcan Architecture é um perfil opcional de organização interna de um aplicativo participante.

[English — normativa](README.md) · [Início rápido](#quick-start) · [Regras de referência](#reference-rules) · [Verificação](#verification) · [Conformidade](#conformance) · [Notas da versão](#release-notes)

A edição em inglês é normativa; este manual é sua tradução coordenada. **Alpha** significa que o modelo, as ferramentas e a representação podem sofrer alterações incompatíveis nas próximas edições. O exemplo executável é uma demonstração delimitada, não uma plataforma de produção nem um certificado de todas as obrigações do OAL.

## Modelo e responsabilidades

O referencial selecionado é OAL Stable-v1.0.0. O Atlas fornece os contratos com significado externo; o Minerva especifica o programa abstrato de domínio e sua verificação comportamental; o Vulcan realiza o programa, os testes, a composição concreta e a organização de execução. As decisões de interação continuam sendo L4 mesmo quando seu código está fisicamente em `boundaries/` de um aplicativo.

| Informação ou decisão | Responsabilidade autoritativa nesta edição |
| --- | --- |
| Casos, critérios dos interessados, permissões e resultados externos exigidos | Instância Atlas L1 |
| Contratos de domínio, componentes lógicos, algoritmos, estados, significado das dependências e cenários ADVS | Blueprint Minerva L2 |
| Espelho por arquivo de código, símbolos, fluxos descritivos e vínculos com a realização | Espelho Minerva L2; fatos observados são identificados como observações |
| Inventário de apps, perfil, escolhas de implementação, composição, execução e evidências observadas | Documentação Vulcan L3 |
| Rotas HTTP, interpretação de CLI, controles do navegador e projeções de canal | Material L4 identificado no exemplo |
| Glossário, procedência e apoio transversal | `Shared/`, com referências às definições canônicas |

A localização física não muda a camada de uma responsabilidade. Um contrato semântico não ganha uma segunda definição concorrente em L3. O modelo não exige YAML universal de ecossistema, container, classe abstrata, classe-base `VulcanUseCase`, hierarquia de interfaces ou framework de injeção.

As fontes selecionadas estão congeladas em [baselines](verification/source-baselines.json), [OAL português](verification/sources/oal/README.pt-br.md.txt) e [Atlas português](verification/sources/atlas/README.pt-br.md.txt). A demonstração usa uma instância Atlas própria, `ATLAS-VULCAN-TASKBOARD`, revisão `1`; ela **não** afirma implementar sem mudanças o exemplo Task Board publicado separadamente pelo Atlas.

<a id="quick-start"></a>
## Início rápido

Python 3.11 ou superior é o requisito declarado das fontes. A evidência registra o interpretador e o ambiente efetivamente avaliados. Os aplicativos e o avaliador estrutural usam a biblioteca padrão; a verificação completa também usa o validador Minerva incluído e suas dependências fixadas.

Na pasta desta edição:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_examples.py verify
.venv/bin/python run_examples.py list
.venv/bin/python run_examples.py start --all
```

No Windows, o executável correspondente é `.venv\Scripts\python.exe`. Essa orientação é uma adaptação de instalação, não evidência de execução em Windows. Os serviços HTTP usam `127.0.0.1`: TaskBoard em `http://127.0.0.1:8765/` e LegacyReports em `http://127.0.0.1:8766/report`. Ctrl+C encerra os filhos iniciados pelo launcher. Portas e caminho do banco podem ser configurados.

A execução temporária e a seleção também iniciam aplicativos reais:

```bash
python run_examples.py start --all --duration 2 --task-port 8875 --report-port 8876
python run_examples.py start --apps TaskBoard
python run_examples.py start --apps LegacyReports
```

Selecionar LegacyReports inclui sua dependência TaskBoard. Os modos padrão são serviços HTTP; `--all` não executa comandos de manutenção nem todos os modos disponíveis. As entradas resolvem recursos a partir do próprio arquivo e podem ser chamadas por caminho absoluto a partir de outra pasta de trabalho.

Os mesmos casos são acessíveis pelo terminal:

```bash
python examples/task-board-ecosystem/apps/TaskBoard/main.py --token demo-editor create --title "Revisar o blueprint"
python examples/task-board-ecosystem/apps/TaskBoard/main.py --token demo-reader list
python examples/task-board-ecosystem/apps/TaskBoard/main.py --token demo-editor complete TASK_ID
python examples/task-board-ecosystem/apps/LegacyReports/reports.py report
```

Substitua `TASK_ID` pelo identificador retornado na criação. Os tokens representam identidades didáticas locais. A fronteira de confiança e a configuração estão no [guia de execução](guides/execution.pt-br.md); não constituem um projeto de autenticação de produção.

## Organização

Todo ecossistema instanciado DEVE ter `apps/`, uma pasta identificável por app e uma entrada implementada na raiz. Recomenda-se `docs/`, organizada segundo os modelos adotados:

| Caminho no ecossistema instanciado | Finalidade |
| --- | --- |
| `apps/<App>/` | Código de cada aplicativo, em sua linguagem e arquitetura interna |
| `docs/L1_AtlasSpecifications/` | Instâncias Atlas e referências aos contratos externos |
| `docs/L2_MinervaBlueprints/` | Blueprints e espelho por arquivo de código |
| `docs/L3_Vulcan/` | Organização, composição concreta, execução, integração e referências a evidências |
| `docs/Shared/` | Nome sugerido para material de apoio transversal |
| Uma entrada na raiz, como `launch.py` | Descoberta e inicialização de todos os modos padrão ou de uma seleção |

As informações são exigidas onde indicado; esses nomes de diretórios documentais são recomendados. Outra localização é aceita quando as informações e referências continuam recuperáveis. Camadas não adotadas não exigem pastas vazias. O repositório desta especificação tem organização editorial própria; o ecossistema instanciado está no [exemplo executável](examples/task-board-ecosystem/README.pt-br.md).

<a id="reference-rules"></a>
## Regras de referência

**DEVE** expressa obrigação no escopo indicado; **RECOMENDA-SE** expressa recomendação; **PODE** expressa possibilidade. Obrigações do perfil Vulcan Architecture não são estendidas silenciosamente a aplicativos legados. Os IDs correspondem ao catálogo incluído; esta tabela estabelece as regras adotadas e o relatório de cobertura registra separadamente sua implementação e avaliação.

| ID | Escopo e regra |
| --- | --- |
| VUL-001 | O modelo DEVE identificar-se como L3 do OAL e distinguir ecossistema, perfil arquitetural, fontes L2 e interação L4. |
| VUL-002 | O ecossistema DEVE ter `apps/`, pastas por aplicativo e entrada funcional na raiz. RECOMENDA-SE a organização documental por camadas. |
| VUL-003 | Cada app DEVE declarar identidade, linguagem, perfil interno, modos disponíveis e escopo da declaração de conformidade. |
| VUL-004 | Outras arquiteturas PODEM participar sem refatoração interna. Operações públicas e interiores indisponíveis ou não avaliados DEVEM ser descritos fielmente. |
| VUL-005 | Apps Vulcan Architecture DEVEM apresentar áreas irmãs `usecases/`, `tools/`, `entities/` e `value_objects/`. Áreas podem estar vazias, sem classes artificiais. Áreas de suporte DEVEM ser identificadas. |
| VUL-006 | Casos do perfil DEVEM estar em `usecases/<Domain>/`. A pasta de domínio não concede autorização. |
| VUL-007 | Cada arquivo do perfil DEVE ter uma classe ou estrutura principal equivalente e seus membros associados. Estruturas independentes exigem arquivos próprios; exceções obrigatórias da linguagem DEVEM ser identificadas. |
| VUL-008 | Estruturas centrais DEVEM usar prefixo de papel e PascalCase; métodos usam camelCase, atributos snake_case e o nome-base do arquivo corresponde à estrutura. Grafias impostas por framework exigem adaptação documentada. |
| VUL-009 | Adaptações de linguagem DEVEM preservar responsabilidades e identificar desvios necessários, incluindo pares declaração/implementação em C e identificadores exportados em Go. Descrição e evidência executada DEVEM ser distinguidas. |
| VUL-010 | Value objects DEVEM ser imutáveis, independentes de infraestrutura e conter invariantes. Seu consumo direto de produção fica nas entidades; dados públicos do núcleo não expõem value objects. |
| VUL-011 | Entidades DEVEM preservar validade intrínseca canônica na construção e nas alterações permitidas, sem depender de ferramentas, casos ou infraestrutura. Identidade persistente não é requisito universal de toda entidade. |
| VUL-012 | Ferramentas DEVEM realizar capacidades técnicas sob contratos declarados. NÃO DEVEM assumir autorização dos casos nem duplicar validação intrínseca de entidade já válida. Hidratação usa construção canônica; verificações contextuais ficam explícitas. |
| VUL-013 | Cada caso DEVE realizar a identidade lógica selecionada e continuar invocável sem exigir HTTP, CLI ou outro canal específico. |
| VUL-014 | Entradas e saídas operacionais do núcleo DEVEM ser primitivas, entidades ou coleções tipadas desses valores. Colaboradores e recursos técnicos DEVEM ser separados dos dados operacionais. Ausência, resultados vazios e representações relevantes DEVEM ser explícitos. |
| VUL-015 | Todo caso DEVE receber contexto de ator por caminho confiável explícito e autorizar antes de efeitos de domínio. Contexto ausente, não resolvido, desconhecido ou insuficiente é recusado; anonimato exige admissão explícita. |
| VUL-016 | A composição DEVE identificar e injetar os colaboradores necessários. Biblioteca, classe abstrata, container ou framework de injeção não são obrigatórios. |
| VUL-017 | Grafos concretos de dependência entre casos e entre ferramentas DEVEM ser explícitos, acíclicos e vinculados ao significado L2. Ferramentas NÃO DEVEM consumir casos. Composição de casos preserva contexto e autorização de cada caso. |
| VUL-018 | A implementação DEVE preservar distinções entre sucesso, ausência, falha e, quando previstos, resultados parciais ou incertos. Cancelamento não significa reversão sem garantia do contrato selecionado. |
| VUL-019 | Composição e ferramentas DEVEM identificar proprietário e vida útil de recursos e liberá-los nos caminhos pertinentes de sucesso e falha. |
| VUL-020 | Nos escopos do perfil e OAL avaliados, canais DEVEM adaptar contexto, dados e resultados aos casos preparados, preservando a responsabilidade de domínio. Interação DEVE ser identificada como L4. Handlers legados continuam sendo suas operações reais. |
| VUL-021 | Apps DEVEM integrar-se por operações públicas documentadas, sem imports privados ou acesso direto ao armazenamento de domínio de outro app. Representação, compatibilidade e falhas DEVEM ser explícitas. |
| VUL-022 | A entrada da raiz DEVE descobrir aplicativos, iniciar todos os modos padrão declarados ou uma seleção e informar falhas. |
| VUL-023 | Cada modo DEVE identificar mecanismo, pasta de trabalho, configuração, parâmetros, dependências, prontidão ou conclusão e encerramento. Não se exige Docker ou linguagem universal. |
| VUL-024 | A inicialização DEVE declarar se expande dependências exigidas ou recusa sua ausência; DEVE respeitar ordem de prontidão e rejeitar ciclos. |
| VUL-025 | A inicialização DEVE verificar prontidão da instância pretendida, detectar falha de serviço gerenciado e encerrar somente recursos próprios ou explicitamente entregues à sua gestão. |
| VUL-026 | A realização DEVE definir implementação e execução dos testes comportamentais ADVS e das verificações de apoio, mantendo vínculos com casos e critérios. |
| VUL-027 | Evidências DEVEM identificar versão, ambiente real, comando, resultados e limites, distinguindo verificação concluída, falha, ignorada, apenas configurada e não executada. |
| VUL-028 | A realização DEVE referenciar versões L2 selecionadas e registrar impactos pertinentes no código e nos testes quando contratos, permissões, dados ou dependências mudam. |
| VUL-029 | A documentação L3 DEVE explicar organização, perfis, composição, recursos, execução, integração concreta e evidências, referenciando contratos canônicos e descrições por arquivo em L2. |
| VUL-030 | A avaliação estrutural DEVE publicar regras e formas de linguagem suportadas, contraexemplos e diagnósticos. DEVE distinguir inspeção, revisão semântica, execução e validação Minerva. |

O [guia Vulcan Architecture](guides/vulcan-architecture.pt-br.md) detalha o perfil. [Legados e boundaries](guides/legacy-and-boundaries.pt-br.md) explica a integração sem impor esse perfil ao LegacyReports.

<a id="verification"></a>
## Verificação

```bash
python run_examples.py evaluate
python run_examples.py test
python run_examples.py verify
```

`evaluate` inspeciona a estrutura Python declarada. `test` executa as suítes dos apps e do avaliador. `verify` exige ambas e valida blueprint e espelho L2 usando a CLI Minerva incluída. Relatórios são gravados em `verification/`; `--report-dir PATH` seleciona outra pasta de evidências. Falhas produzem saída não zero; a ausência dos recursos L2 exigidos faz a verificação completa falhar, sem omissão silenciosa.

| Evidência | Significado |
| --- | --- |
| [structure.json](verification/structure.json) | Arquivos Python inspecionados, regras, adaptações, dependências e diagnósticos |
| [execution.json](verification/execution.json) | Contagem, ambiente, comando, duração e resultado real por teste |
| [minerva.json](verification/minerva.json) | Resultado separado da validação L2, com vínculos de código quando solicitados |
| [Cobertura dos requisitos](verification/REQUIREMENTS.pt-br.md) | Escopo de entrega e avaliação por requisito, sem inferir sucesso pela quantidade de arquivos |
| [Contraexemplos](examples/structural-counterexamples/README.pt-br.md) | Violações deliberadas e diagnósticos esperados |

A suíte registrada contém 26 métodos unittest: 19 verificações de aplicações e ciclo de vida e 7 do avaliador. Cobre os três casos diretamente, HTTP/CLI, integração pública com legado, recusas de autorização, validade canônica de títulos, falhas de armazenamento selecionadas, seleção de apps, ciclos, rejeição de instância alheia e limpeza dos processos próprios. Subcasos não são contados como novos métodos. `execution.json` é a referência para os testes realmente executados e seus resultados atuais.

Não há evidência de execução em C/Go, Docker, autenticação de produção, interação completa no navegador, carga, segurança de transações distribuídas ou CI executada no GitHub. C/Go são adaptações descritas. As páginas são servidas e verificadas como respostas HTTP; isso não demonstra automação de navegador. Consulte o [escopo do avaliador](guides/assessment.pt-br.md).

<a id="conformance"></a>
## Conformidade

Uma declaração DEVE identificar modelo e edição, referencial OAL, perfil selecionado, artefato/app avaliado, regras aplicáveis, evidências e limites. Participação no ecossistema difere de adoção do perfil interno. TaskBoard usa Vulcan Architecture para Python; LegacyReports participa por contrato HTTP público e mantém outra arquitetura.

`model.json` contém metadados editoriais, sem impor manifesto universal aos apps. O [registro de realização](examples/task-board-ecosystem/docs/L3_Vulcan/realization.json) é um formato concreto possível de documentação L3, sem criar outro schema universal ao lado do Minerva. O [README L3](examples/task-board-ecosystem/docs/L3_Vulcan/README.pt-br.md) reúne referências a decisões, composição, testes e execução.

Passar no avaliador Python demonstra somente suas verificações sintáticas declaradas. Validar Minerva verifica representação e vínculos selecionados, sem provar comportamento da implementação. Passar nos testes demonstra os cenários observados no ambiente registrado. Avaliações do modelo ou do OAL ainda exigem escopo publicado e revisão semântica; não se presume certificação irrestrita.

<a id="versioning"></a>
## Versionamento

`Alpha-v0.1.0` é o identificador editorial. Os metadados opcionais Python usam `0.1.0a0` pela gramática própria do empacotamento. A edição contém manual, guias, exemplo, testes, ferramentas, snapshots selecionados e dependências. Copiar esta pasta preserva suas entradas; nenhum comando depende de scripts na raiz externa do repositório.

Edições publicadas anteriores devem continuar reproduzíveis. Uma mudança futura registra origem, destino, obrigações alteradas, compatibilidade e migração. Correções que alteram comportamento observado exigem revisão das fontes e do blueprint e novas evidências. Alterar hash, isoladamente, não representa decisão semântica de migração.

O [mapa de migração](verification/MIGRATION.pt-br.md) relaciona a especificação conjunta anterior às responsabilidades separadas. Essa correspondência editorial é distinta da evidência de execução.

<a id="release-notes"></a>
## Notas da versão

Esta edição separa a realização Vulcan L3 da documentação Minerva L2. O espelho por arquivo está em `docs/L2_MinervaBlueprints/`; L3 documenta sua organização e operação concretas. `docs/` é recomendada; `apps/` e inicializador continuam obrigatórios nos ecossistemas instanciados.

O exemplo mantém geração didática de identidade, construção canônica de entidade, título normalizado e conclusão idempotente. Acrescenta vínculos com fontes e critérios, avaliador Python delimitado com contraexemplos, mais testes negativos e de ciclo de vida e uma entrada local de verificação. Nenhuma biblioteca arquitetural abstrata foi introduzida.

As fontes derivam do exemplo Alpha anterior, revisado para a separação atual de responsabilidades. Relatórios históricos não são reutilizados como evidência desta edição. O [registro de fontes](verification/source-baselines.json) preserva a procedência; relatórios atuais registram a execução atual.
