# Perfil Vulcan Architecture

[English](README.md) · [Edição](../../README.pt-br.md) · [Regras](../../specification/README.pt-br.md)

Arquitetura interna opcional para um aplicativo participante do Vulcan Ecosystem. Selecionar explicitamente aplicativo, edição, adaptação de linguagem e arquivos avaliados. Estar em uma pasta não transfere o perfil para aplicativos legados vizinhos.

| Área | Responsabilidade e exemplo |
| --- | --- |
| `usecases/<Domain>/` | Caso invocável, autorização e algoritmo: `UseCase_CreateTask.py`. |
| `tools/` | Capacidade concreta e garantias de infraestrutura: `Tool_SqliteTaskStore.py`. |
| `entities/` | Validade intrínseca canônica e transições: `Entity_Task.py`. |
| `value_objects/` | Valores imutáveis opcionais consumidos em produção por entidades: `ValueObject_TaskIdentity.py`. |

As quatro áreas irmãs existem; uma área pode ficar vazia. Minimal não inventa um value object. As áreas de apoio `composition/`, `boundaries/`, `support/` e `tests/` são identificadas. Uma classe/estrutura principal por arquivo do perfil; nome-base igual ao da estrutura. Prefixos dos papéis seguidos de PascalCase, métodos camelCase e atributos snake_case. Hooks dunder Python e overrides HTTP obrigatórios mantêm a grafia do framework.

Entidades/value objects não dependem de infraestrutura, casos ou ferramentas. Ferramentas não revalidam intrinsecamente entidades prontas. Hidratação de armazenamento bruto é construção canônica. Condições contextuais de persistência, transações, isolamento e incerteza pertencem aos contratos das ferramentas. Cada caso autoriza contexto confiável antes de validação/efeitos. Dados operacionais são primitivos/entidades/coleções tipadas; colaboradores injetados são dependências técnicas.

Dependências são explícitas e acíclicas. Ferramentas não consomem casos. Casos podem compor casos preservando contexto e autorização de cada chamado. O cancelamento de reserva compõe a consulta. `AppComposition` seleciona implementações e injeta colaboradores; nenhuma classe-base, container ou biblioteca arquitetural é obrigatória.

Ferramentas vivem com a aplicação; conexões vivem por operação e fecham em `finally`. Transações SQLite explícitas e `BEGIN IMMEDIATE` protegem as garantias selecionadas. O operador é dono dos dados persistentes. Canais projetam entradas/resultados e obtêm contexto pelo caminho confiável; não definem validade ou política de permissão do domínio.

O [avaliador](../../scripts/evaluate_structure.py) confere sintaxe/importações Python delimitadas. Seu grafo é estático e não prova dependências dinâmicas ou preservação do domínio. [Fixtures negativas](../../tests/fixtures/structural-counterexamples/README.pt-br.md) exercitam diagnósticos.

## Adaptações descritivas de linguagem

C pode associar uma struct/typedef principal a funções com receptor e um par declarado de header/implementação. Cada arquivo físico continua com seu espelho L2. Documentar propriedade, alocação, ligação, erros e limpeza.

Go pode associar métodos com receptor a uma struct principal. Nomes exportados exigem inicial maiúscula; registrar a adaptação em vez de alegar camelCase literal. Declarar pacotes, valores zero, construtores e imutabilidade. C e Go são apenas descrições; não se entrega evidência de compilação/execução ou avaliação dessas linguagens.
