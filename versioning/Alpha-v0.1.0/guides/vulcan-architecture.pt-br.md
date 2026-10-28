# Perfil Vulcan Architecture

[Regras da edição](../README.pt-br.md#reference-rules) · [English](vulcan-architecture.md)

## Aplicabilidade

Vulcan Ecosystem organiza aplicativos que cooperam. Cada app escolhe explicitamente o perfil Vulcan Architecture; outros podem conservar arquitetura procedural, funcional, de framework ou existente. A declaração identifica app, adaptação de linguagem, edição, arquivos avaliados e limites. Estar na mesma pasta não transfere o perfil aos demais apps.

Os quatro papéis centrais são `UseCase_`, `Tool_`, `Entity_` e `ValueObject_`. São responsabilidades de organização de código, não classes obrigatórias de uma biblioteca. O exemplo instancia classes Python concretas comuns, recebe colaboradores nos construtores e os seleciona em `AppComposition`.

## Unidades e nomes

| Papel | Caminho ilustrado | Estrutura principal |
| --- | --- | --- |
| Caso em um domínio declarado | `usecases/TaskManagement/UseCase_CreateTask.py` | `UseCase_CreateTask` |
| Capacidade concreta | `tools/Tool_SqliteTaskStore.py` | `Tool_SqliteTaskStore` |
| Dados e comportamento intrínseco | `entities/Entity_Task.py` | `Entity_Task` |
| Valor encapsulado | `value_objects/ValueObject_TaskTitle.py` | `ValueObject_TaskTitle` |
| Suporte de composição | `composition/AppComposition.py` | `AppComposition` |
| Adaptador de canal, identificado como L4 | `boundaries/Boundary_Http.py` | `Boundary_Http` |

O nome-base do arquivo corresponde à classe/struct. Métodos usam camelCase, como `createTask`; atributos usam snake_case, como `task_store`. Arquivos de suporte também mantêm uma estrutura principal. Uma entrada técnica de processo pode conter funções de inicialização ou exigidas pela linguagem; isso não autoriza esconder operações de aplicação em um script sem papel identificado.

O exemplo usa namespace packages Python e dispensa `__init__.py` vazios. `main.py` é uma exceção técnica explícita. Hooks Python como `__init__` e `__post_init__`, além de `do_GET`, `do_POST` e `log_message` exigidos pelo framework HTTP, conservam as grafias necessárias. As adaptações constam da evidência estrutural. LegacyReports fica fora do perfil interno, sem dispensas artificiais para cada função procedural.

Contraexemplos incluem duas classes independentes no mesmo arquivo, `Entity_Task.py` contendo `Tool_Task`, método `create_task`, atributo `taskStore` ou caso diretamente em `usecases/` sem domínio. O [contraexemplo publicado](../examples/structural-counterexamples/README.pt-br.md) exercita esses problemas e violações de dependências.

## Responsabilidades e dependências

Entidades concentram validade canônica e transições intrínsecas. Não abrem conexões, leem requisições ou resolvem identidades. Value objects representam valores imutáveis, igualdade e invariantes; seu consumo direto de produção fica nas entidades. Testes podem examiná-los diretamente para verificar essa garantia.

Ferramentas implementam capacidades como persistência e acesso externo. Uma ferramenta pode receber primitivos e construir ou hidratar uma entidade pelo construtor canônico. Isso difere de repetir independentemente a validação intrínseca da entidade. Condições contextuais como existência de registro, falha de transporte e escopo transacional pertencem ao contrato da capacidade. A autorização do caso permanece no caso.

Casos preservam identidade lógica, domínio declarado e comportamento selecionado. Parâmetros e resultados operacionais são primitivos, entidades e coleções tipadas; os colaboradores do construtor são dependências técnicas. Um caso preparado pode ser invocado diretamente e por diferentes canais. Recebe contexto de ator confiável e recusa acesso insuficiente antes de chamar colaborador com efeito de domínio. Ao compor casos, cada caso mantém sua autorização e o contexto é propagado sem ampliar permissões silenciosamente.

Dependências concretas são explícitas e acíclicas. Casos podem colaborar com casos e ferramentas com ferramentas quando o modelo lógico exigir; ferramentas não dependem de casos. Laço de algoritmo não é ciclo entre componentes. O exemplo não tem arestas entre casos nem entre ferramentas: os três casos compartilham um store, enquanto entidades dependem apenas de value object e suporte da linguagem. O grafo estático observado consta de [structure.json](../verification/structure.json); o grafo abstrato pertence ao blueprint L2.

## Composição e recursos

`AppComposition` cria a ferramenta SQLite concreta e a entrega aos três casos concretos. Também resolve tokens didáticos em contexto de entidade na fronteira confiável. O container inteiro e localizadores globais não são entradas operacionais dos casos.

O store vive por instância da aplicação. Cada operação abre e fecha sua conexão SQLite com `contextlib.closing`; o contexto da conexão confirma escritas bem-sucedidas e reverte em exceções. O arquivo do banco continua sob propriedade do operador, e a limpeza dos processos não remove os dados. A criação de schema na inicialização é ação de infraestrutura anterior às requisições; a autorização se refere às operações de domínio, não à ausência de toda inicialização de infraestrutura.

## Adaptações de linguagem: descritas, não executadas

### C

Uma adaptação C associa uma `struct`/`typedef` principal às funções cujo parâmetro receptor e nomes identificam essa estrutura. `Entity_Task.h` e `Entity_Task.c` podem formar um par explícito de declaração e implementação da mesma unidade. Cada arquivo físico recebe sua ficha no espelho Minerva; ambos podem referenciar o mesmo elemento lógico. Funções de outra estrutura exigem outra unidade. Linkagem, handles opacos, alocação, propriedade, códigos de erro e liberação precisam ser declarados; macros e headers não criam novos papéis arquiteturais.

### Go

Uma adaptação Go associa métodos com receiver a uma struct principal e preserva a correspondência escolhida entre arquivo e tipo. Métodos privados podem usar camelCase e campos internos snake_case. Métodos exportados precisam começar com maiúscula pelas regras de Go; o perfil deve registrar essa exceção, como `GetId` em lugar de `getId`, sem afirmar cumprimento literal de camelCase. Organização de pacotes, superfície exportada, construtores, comportamento do valor zero e convenções de imutabilidade devem ser especificados na implementação concreta. A existência de uma struct, isoladamente, não comprova essas garantias.

Esta edição não compila nem testa C ou Go. O avaliador Python produz evidência apenas das formas Python suportadas, sem ser um validador universal. Uma nova linguagem precisa de sua avaliação e de evidência própria de execução.
