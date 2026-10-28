# Fixture técnica: ecossistema heterogêneo

[English](README.md) · [Exemplos canônicos](../../../examples/README.pt-br.md)

TaskBoard e LegacyReports históricos servem somente às regressões de ciclo de vida/HTTP público. Esta não é a realização canônica TaskBoard do Atlas/Minerva. IDs gerados, títulos normalizados e conclusão idempotente antigos são comportamento da fixture, sem equivalência ADVS alegada.

`launch.py list` mostra registro explícito. `launch.py start --all --duration 1` inicia os dois serviços HTTP padrão. Selecionar `--apps LegacyReports` inclui o TaskBoard como pré-requisito. A inicialização verifica identidade de instância e limpa filhos próprios diante de falha; nunca apaga dados persistentes nem encerra serviços alheios. LegacyReports mantém organização procedural e usa somente HTTP público.

O runner executa esta fixture em processo separado para isolar nomes de módulos dos exemplos canônicos. Os bytes originais estão no baseline Git anterior à revisão; a fixture atual inclui correções de propriedade de porta no Windows. A documentação do antigo exemplo de negócio não é contrato ativo.
