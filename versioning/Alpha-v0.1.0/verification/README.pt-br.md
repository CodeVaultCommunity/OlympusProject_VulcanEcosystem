# Evidências de verificação

[English](README.md) · [Edição](../README.pt-br.md#verification)

Execute `python run_examples.py verify` nesta edição ou invoque o script por caminho absoluto. Ele grava relatórios reais e retorna erro se estrutura, testes ou gate Minerva exigido falharem. Use `--report-dir PATH` para registrar uma nova execução separada.

| Relatório | Escopo |
| --- | --- |
| [structure.json](structure.json) | Inspeção AST delimitada de 14 fontes TaskBoard; LegacyReports fica explicitamente fora desse perfil interno |
| [execution.json](execution.json) | Métodos unittest de aplicativos e avaliador, com ambiente, comando, duração, resultados e limites reais |
| [minerva.json](minerva.json) | Validação L2 e vínculo de código independentes, pela versão Minerva incluída e declarada |
| [Baselines](source-baselines.json) | Revisões de fontes, localizações imutáveis e hashes |
| [Cobertura dos requisitos](REQUIREMENTS.pt-br.md) | Situação rastreável de entrega e avaliação do catálogo |

A suíte dos apps contém 19 métodos; a do avaliador, 7. Os casos diretos preservam três identidades ADVS; verificações adicionais cobrem canais, integração, negativos estruturais e ciclo de vida. Sucesso da suíte não significa prova independente de todo cenário ou afirmação de aceite possível. Alguns caminhos usam mocks; verificações HTTP e de subprocessos reais também estão presentes e delimitadas nos guias.

Os relatórios atuais são evidência desta edição, sem reutilizar resultados da Alpha anterior. Não implicam execução C/Go, Docker, implantação remota, identidade de produção, carga, interação em navegador ou CI hospedada. Testes de sinal POSIX são explicitamente ignorados em outros sistemas; a contagem de ignorados deve continuar visível.

Não inclua bancos temporários, credenciais, caches de bytecode ou diretórios temporários de teste. Hash observado detecta alteração de arquivo, sem decidir correção comportamental; reconcilie com L1/L2 antes de atualizá-lo.
