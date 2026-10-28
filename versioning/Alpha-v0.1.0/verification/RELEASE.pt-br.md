# Recibo de verificação — Alpha-v0.1.0

[English](RELEASE.md) · [JSON](current.json) · [Summary / resumo](runs/20261028-windows-final/summary.json)

Mesma Alpha não publicada, revisada no lugar. A execução atual passou no Windows com Python 3.12.14. Não se afirma publicação remota, execução hospedada de CI ou aceite do responsável.

| Scope / escopo | Result / resultado |
| --- | --- |
| [minimal](runs/20261028-windows-final/minimal/execution.json) | 10 métodos; 12 cenários; 2 apoios; todos passaram |
| [composition](runs/20261028-windows-final/composition/execution.json) | 19 métodos; 33 cenários; 3 apoios; todos passaram |
| [task-board](runs/20261028-windows-final/task-board/execution.json) | 21 métodos; 31 cenários; 7 apoios; todos passaram |
| [L3 tooling / ferramentas](runs/20261028-windows-final/tooling.json) | 13 métodos, 1 ignorado (privilégio de symlink de diretório indisponível) |
| [Legacy technical fixture / fixture legada](runs/20261028-windows-final/legacy-fixture.json) | 19 métodos, 1 ignorado (asserção SIGTERM POSIX) |
| [Repository tools / ferramentas da raiz](runs/20261028-windows-final/repository-tests.json) | 33 testes passaram |
| [Source preservation / preservação das fontes](runs/20261028-windows-final/source-preservation.json) | 3 entradas Atlas canônicas exatas; ADPM/cenários Minerva herdados sem alteração; hashes observados correspondem aos bytes atuais. |

A edição executou 82 métodos unittest: 80 passaram e 2 foram ignorados. Cobertura de cenários/apoios é uma contagem distinta: os 76 cenários e 12 apoios passaram. Cada exemplo também passou na avaliação estrutural e no validador Minerva externo explicitamente selecionado, sem diagnósticos. Hashes/versão da ferramenta ficam no respectivo relatório.

[minimal Minerva](runs/20261028-windows-final/minimal/minerva.json) · [composition Minerva](runs/20261028-windows-final/composition/minerva.json) · [task-board Minerva](runs/20261028-windows-final/task-board/minerva.json)

As entradas Minerva foram lidas da árvore local não publicada baseada no commit `5e4da7d`; os hashes identificam o conteúdo selecionado, não os bytes do commit anterior. A conferência confirmou igualdade com essa árvore no momento registrado. Snapshots originais e revisões finais dos vínculos ficam separados.

Limites: SQLite local e identidade didática; doubles não estabelecem durabilidade física diante de desastre. Tempos cobrem 30 chamadas CLI por procedimento aplicável da fonte, não SLA de produção. Cancelamento de reserva reutiliza a verificação temporal da criação; latência do cancelamento permanece questão aberta da fonte. Não houve execução de UI de navegador, C/Go, Docker, implantação distribuída ou CI hospedada. Os dois testes ignorados não são considerados verificados. As imagens não foram alteradas nesta revisão. Relatórios históricos ficam em `reviews/` e execuções anteriores, sem serem reutilizados como evidência atual.

O inventário da raiz é gerado após este recibo e conferido separadamente; o ID do commit final fica em recibo externo para evitar hashes circulares.

## Revisão da organização da raiz

A raiz foi reduzida aos arquivos de entrada/governança combinados, LICENSE e configuração técnica Git/CI. Documentos auxiliares e dependências foram realocados; temporários foram preservados fora do repositório. Os 33 testes das ferramentas e a verificação completa da edição passaram novamente. Veja o [recibo da organização](runs/20261028-root-organization/organization.json) e os [resultados da edição](runs/20261028-root-organization/summary.json).
