# Contratos de execução

[English](execution.md) · [Edição](../README.pt-br.md)

Os três exemplos canônicos são ecossistemas independentes de um aplicativo. `launch.py` na raiz contém `REGISTRY` explícito; `list` o apresenta, `start --all` seleciona modos padrão e `start --apps APP` seleciona o aplicativo registrado. Aplicativos desconhecidos são recusados antes da inicialização. O runner da edição exige `--example NOME` para iniciar um ecossistema. Ele não combina exemplos independentes em um aplicativo.

HTTP é o modo padrão, em `127.0.0.1`. Prontidão só é impressa após associar/escutar a porta, incluindo ID único também retornado por `/health`. `--port 0` pede porta efêmera. Ctrl+C ou `--duration` positivo e finito encerra o serviço e fecha o socket. Falha inicial retorna saída não zero; porta ocupada é recusada sem encerrar serviço alheio. O servidor HTTP sequencial didático não é um serviço concorrente de produção.

CLI executa uma operação, imprime um resultado JSON e encerra. Sucesso retorna zero; recusa/falha de domínio retorna não zero. Erros de configuração/uso são separados. SQLite padrão fica em `work/demo.sqlite3` relativo ao ecossistema; `--db CAMINHO` substitui. `--board` usa `board-A` no TaskBoard por padrão. `VULCAN_DEMO_TOKEN` configura a identidade didática (padrão `demo-editor`); `VULCAN_CALLER_TOKEN` fornece a credencial CLI. HTTP usa `Authorization: Bearer ...`. Um objeto de ator não é credencial.

PowerShell, a partir da edição:

```powershell
$env:VULCAN_CALLER_TOKEN = 'demo-editor'
python examples/task-board/launch.py start --mode cli --operation create --payload '{"task_id":"TASK001","title":"Review Atlas"}'
python examples/task-board/launch.py start --mode cli --operation complete --payload '{"task_id":"TASK001"}'
python examples/task-board/launch.py start --mode cli --operation list
python run_examples.py start --example composition --apps BookingDesk --port 8766 --duration 10
```

Em shell POSIX, use `export VULCAN_CALLER_TOKEN=demo-editor`. Chamadas diretas constroem `AppComposition(db_path)` e invocam o caso preparado com `Entity_ActorContext` confiável; o chamador integra a aplicação confiável. O resolvedor de tokens didático não é um provedor de identidade de produção.

A [fixture legada](../tests/fixtures/legacy-ecosystem/README.pt-br.md) demonstra vários aplicativos, inclusão de pré-requisitos, prontidão por instância, falha de filhos e limpeza apenas de processos próprios. É evidência técnica, sem representar o contrato canônico TaskBoard.
