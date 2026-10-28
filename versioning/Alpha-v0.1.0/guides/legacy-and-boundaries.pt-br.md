# Participação de legados e responsabilidade das boundaries

[Edição](../README.pt-br.md) · [English](legacy-and-boundaries.md)

Um app participa do ecossistema publicando superfície de integração fiel, ciclo de vida e documentação pertinente. Não precisa refatorar seu interior para Vulcan Architecture. LegacyReports mantém funções de módulo e `ReportsHandler` no mesmo `reports.py`, sem reivindicar uma classe por arquivo.

As operações reais são `fetch_tasks`, `summarize_tasks`, `create_report`, o handler HTTP e `main`. O espelho L2 descreve essas unidades sem inventar classe de caso de uso. Seu contrato observável é recuperável; o blueprint TaskBoard não presume análise L1→L2 equivalente de todo o interior legado. Interior indisponível continua identificado como indisponível ou não avaliado.

LegacyReports chama a operação HTTP pública TaskBoard com identidade leitora configurada, verifica o formato primitivo e calcula contagens. Não importa o interior do TaskBoard nem lê seu banco. A ordem de inicialização TaskBoard → LegacyReports é uma decisão concreta L3, com significado e contratos públicos recuperáveis nas referências do modelo e da interação.

No TaskBoard, `Boundary_Http` e `Boundary_Cli` adaptam os canais aos mesmos casos preparados. A composição fornece colaboradores e resolvedor confiável de contexto. Escolhas L4 estão nos [mapeamentos de interação](../examples/task-board-ecosystem/docs/Shared/interaction.pt-br.md); a localização `apps/TaskBoard/boundaries/` não transforma essas escolhas em regras de domínio.

A integração pública também pode usar biblioteca deliberadamente publicada, evento ou outro mecanismo declarado. Vulcan não exige rede em toda relação. Imports privados e acesso ao armazenamento de domínio de outro app não substituem contrato público. A publicação identifica representações, versões, compatibilidade e falhas; nomes de campos iguais não comprovam equivalência semântica.

A integração é exercitada por consistência HTTP/CLI, subprocesso LegacyReports, inicialização completa e ciclo de vida do serviço de relatórios. O escopo é local e síncrono, sem garantia de confiabilidade distribuída, autenticação ou implantação.
