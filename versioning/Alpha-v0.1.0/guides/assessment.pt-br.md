# Avaliação, evidência e limites

[Verificação da edição](../README.pt-br.md#verification) · [English](assessment.md)

## Três perguntas separadas

A avaliação estrutural verifica formas de código suportadas na organização escolhida. A validação Minerva verifica a representação L2 selecionada e seus vínculos. Testes de execução verificam resultados observados dos cenários implementados. Nenhum resultado substitui os demais; mesmo sua combinação conserva os limites de ambiente e cenários registrados.

`python run_examples.py verify` executa gates separados e retorna erro se algum falhar ou não puder executar. Relatórios são resultados de comandos reais. Referenciar um símbolo de teste estabelece rastreabilidade, não comprova sua execução. Validade de schema não comprova preservação de contrato pelo código.

## Avaliador Python

```bash
python scripts/evaluate_structure.py --ecosystem examples/task-board-ecosystem --profile-app TaskBoard --legacy-app LegacyReports --technical-file apps/TaskBoard/main.py --json
```

Repita `--profile-app` e `--legacy-app` para declarar o escopo. `--entry` seleciona o arquivo de entrada. `--technical-file` identifica arquivos técnicos para revisão; a exceção não aceita classes escondidas. `--json REPORT` grava relatório; `--json` sozinho escreve JSON na saída padrão. Cada diagnóstico contém regra, caminho, linha quando disponível, gravidade e mensagem. Saída 1 indica erro estrutural; argumentos inválidos usam saída 2 do argparse.

| Família de regras | Inspeção implementada |
| --- | --- |
| `ECO_APPS`, `ECO_ENTRY` | Presença de apps e entrada local na raiz; existência não demonstra execução |
| `ECO_CLASSIFICATION` | Caminhos declarados, classificações conflitantes e aviso de app não classificado |
| `VA_AREAS`, `VA_DOMAIN` | Quatro áreas centrais e casos dentro de subpasta de domínio |
| `VA_SINGLE_STRUCTURE`, `VA_FILE_NAME`, `VA_ROLE_NAME` | Contagem de classes, incluindo aninhadas, funções independentes sem adaptação, nome de arquivo e prefixo de papel |
| `VA_METHOD_CASE`, `VA_ATTRIBUTE_CASE` | Grafia de métodos definidos e atributos da classe/self, com adaptações Python/HTTP conhecidas |
| `VA_DEPENDENCY_DIRECTION` | Imports estáticos reconhecidos que violam direção do núcleo e avisos para imports entre apps |
| `VA_VALUE_OBJECT_CONSUMER`, `VA_PURE_DATA` | Consumo direto de value object por papel indevido e lista delimitada de imports de infraestrutura nas estruturas de dados |
| `VA_STATIC_CYCLE` | Ciclos nas arestas locais de imports reconhecidas, incluindo relações entre casos/ferramentas |
| `PYTHON_SYNTAX` | Parsing Python, leitura das fontes e recusa explícita de perfil selecionado sem fontes Python |

O avaliador suporta as formas demonstradas pelo TaskBoard. Não comprova chamadas de execução, inspeciona reflexão, descobre imports dinâmicos, prova pureza para qualquer biblioteca, infere API pública de um import ou avalia equivalência de tipos/comportamento. Overrides HTTP são reconhecidos para herança direta de `BaseHTTPRequestHandler`; outros frameworks exigem adaptação declarada e, quando necessário, extensão da ferramenta.

A presença ou ausência de `docs/` isoladamente não decide conformidade. YAML não é inspecionado. Conteúdo documental, confiança no ator, significado de I/O, preservação das fontes, identidade de produção e garantias de recursos fora dos caminhos testados exigem verificações próprias. C e Go não são linguagens implementadas no avaliador.

## Evidências positivas e negativas

O [contraexemplo](../examples/structural-counterexamples/README.pt-br.md) viola deliberadamente dez famílias de diagnóstico. Os testes verificam essas recusas, o exemplo positivo TaskBoard, áreas/entrada ausentes, sintaxe inválida, imports relativos e aceitação de outra localização documental. A fixture não é produto executável nem segundo exemplo conforme.

Os testes de execução verificam garantias selecionadas: recusa antes de acessar ferramenta injetada, construção/normalização, valores imutáveis, persistência entre composições, falha de conexão simulada, projeção HTTP/CLI, integração real em loopback, inicialização completa/seletiva, preservação de serviço alheio e limpeza dos filhos próprios. Alguns caminhos usam substitutos controlados; seus nomes e documentação distinguem esses testes dos processos reais. Não se conclui cobertura de todas as concorrências, recuperações de falha ou combinações possíveis.

## Decisão de release e impacto de mudanças

A release deve preservar fontes selecionadas, comandos locais e evidência de cobertura dos requisitos. Compare contratos autoritativos antes de atualizar hashes observados. Uma mudança no limite do título exige revisão do critério Atlas, dados/algoritmo/ADVS Minerva, value object canônico, restrições dos canais e testes. Uma simples movimentação de arquivo atualiza vínculo físico/espelho sem recriar a identidade lógica do caso. Nenhuma delas se resume a recalcular hashes sem análise.

O [registro L3 de impacto](../examples/task-board-ecosystem/docs/L3_Vulcan/change-impact.pt-br.md) é um exercício fundamentado, sem afirmar que a mudança hipotética foi implementada. Relatórios históricos e atuais permanecem distinguíveis.
