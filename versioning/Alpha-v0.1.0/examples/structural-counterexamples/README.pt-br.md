# Contraexemplos estruturais

A fixture é deliberadamente inválida e não representa ecossistema executável ou conforme. Seu `launch.py` existe apenas para isolar os diagnósticos; presença de arquivo não prova inicialização.

Na raiz da edição:

```bash
python scripts/evaluate_structure.py --ecosystem examples/structural-counterexamples/invalid-ecosystem --profile-app BrokenApp --json
```

Saída esperada: **1**. [expected-diagnostics.json](expected-diagnostics.json) publica as famílias exigidas: estruturas independentes no mesmo arquivo, nome de arquivo divergente, papel incorreto, grafia de método/atributo, caso sem domínio, ferramenta importando caso, ferramenta consumindo value object diretamente, entidade importando infraestrutura e ciclo entre ferramentas. A ferramenta informa caminhos e linhas observados.

`tests/Test_Structure.py` verifica essa fixture e exemplos temporários de áreas/entrada ausentes, sintaxe inválida, imports relativos e localização documental alternativa aceita. Também verifica o TaskBoard real, com exclusão explícita do interior do legado.
