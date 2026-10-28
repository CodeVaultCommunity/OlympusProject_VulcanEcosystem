# Regras adotadas pelo Vulcan — Alpha-v0.1.0

[English](README.md) · [Manual da edição](../README.pt-br.md) · [Alinhamento ao OAL](OAL-ALIGNMENT.pt-br.md)

MUST indica obrigação no escopo nomeado, SHOULD recomendação, MAY opção. São regras adotadas pelo Vulcan. Prefixos, pastas, convenções de nomes e políticas do inicializador são decisões do modelo/perfil; não são exigências universais do OAL. O [catálogo](../verification/requirements/catalog.json) preserva a discussão e os IDs originais. A [cobertura de entrega](../verification/REQUIREMENTS.pt-br.md) registra escopo e evidência, sem afirmar aceite do responsável.

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

A descoberta pode usar um registro explícito. Os ecossistemas canônicos de um aplicativo usam `REGISTRY` no inicializador da raiz; adicionar uma pasta não registra um aplicativo. A fixture técnica de vários aplicativos declara dependências e inclui pré-requisitos. Bibliotecas, classes-base e value objects são opcionais; uma área exigida pelo perfil pode ficar vazia.
