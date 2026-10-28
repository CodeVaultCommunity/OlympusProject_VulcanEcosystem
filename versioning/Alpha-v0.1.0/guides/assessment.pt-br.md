# Escopo da avaliação

[English](assessment.md)

`evaluate` inspeciona estrutura Python declarada, papéis/nomes, direções selecionadas de imports e ciclos estáticos. Caminhos são normalizados para POSIX nas chaves do grafo em Windows e POSIX. Não executa código nem prova preservação semântica.

`test` executa cenários canônicos, verificações concretas de armazenamento, ciclo de vida HTTP/CLI, regressões do avaliador e fixture legada isolada. Subtestes bem-sucedidos mantêm IDs de cenário/apoio; IDs esperados ausentes recebem `not_run`. Quantidades de métodos, cenários e apoios são distintas. Hashes são capturados antes e conferidos depois. Relatórios recusam sobrescrever uma execução anterior.

`verify` acrescenta validação de leitura com edição externa Minerva compatível explicitamente selecionada. Registra hashes da ferramenta e versão declarada. Não há fallback, geração ou tradução. Validador/dependência ausente ou incompatível produz inconclusivo e impede sucesso completo. A configuração GitHub executa somente verificações L3 locais; integração L2 externa é selecionada e registrada separadamente.

Evidência não transforma premissas das fontes em requisitos aprovados. Medições de tempo observam 30 chamadas CLI locais até a captura completa de stdout. A meta de 2 segundos é uma premissa didática da fonte, não SLA de produção. Cancelamento de reserva referencia o procedimento de tempo da criação; isso não comprova latência do cancelamento. A fonte preserva essa questão aberta.

Doubles mostram tratamento de confirmação perdida sem repetição; não demonstram sobrevivência física do disco à falta de energia. Testes SQLite com threads cobrem atualização condicional local e consistência de leitura. Verificações de symlink e sinal POSIX podem ser ignoradas onde indisponíveis; isso permanece visível. Identidade de produção, interface de navegador, sistemas distribuídos, C/Go e execução hospedada de CI ficam fora do escopo observado.
