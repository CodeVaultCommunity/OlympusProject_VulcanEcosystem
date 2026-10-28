# Revisão dentro da Alpha não publicada

[English](MIGRATION.md) · [Mapa histórico de responsabilidades](requirements/migration.json)

A edição permanece Alpha-v0.1.0. O baseline Git `78232f2` preserva a distribuição recebida antes da revisão. O mapa da proposta combinada anterior continua como contexto histórico; não prova reexecução do runtime original aqui.

| Local/comportamento anterior | Destino/decisão atual |
| --- | --- |
| Cópia executável `vendor/minerva/` | Removida; `integrations/minerva/` explicativa e validação externa explicitamente selecionada. |
| `examples/task-board-ecosystem/` divergente | `tests/fixtures/legacy-ecosystem/`, somente regressões técnicas. |
| Contraexemplo estrutural em examples | `tests/fixtures/structural-counterexamples/`. |
| Guia arquitetural misturado com guias gerais | `profiles/vulcan-architecture/`, com entradas EN/PT. |
| Exemplo principal diferente do Atlas | `minimal`, `composition`, `task-board` canônicos, fixados às entradas Atlas/Minerva. |
| Nomes de relatório reutilizados | Pastas imutáveis por execução; relatórios anteriores em `reviews/`. |

Bancos da fixture não são migrados automaticamente para exemplos canônicos. Identificadores, validação, estados e semântica da conclusão diferem. Selecione outro `--db` para os programas canônicos. Não há motor de migração ou tradutor. Mudanças de contrato exigem revisão das fontes antes de converter código/dados.
