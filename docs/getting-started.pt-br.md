# Primeiros passos com Vulcan Ecosystem

[English](getting-started.md) · [Início](../README.pt-br.md) · [Edição selecionada](../versioning/Stable-v1.0.0/README.pt-br.md)

Vulcan Stable-v1.0.0 realiza uma árvore Markdown completa do Minerva Stable-v1.0.0 como código executável, testes, metadados de realização e grafo de conhecimento. Cada módulo executável ou testável do Minerva corresponde a um arquivo de código e símbolo de nível superior, preservando as identidades do Atlas e do Minerva.

Use Python 3.11 ou superior. Na raiz do repositório:

```bash
python -m pip install -e "versioning/Stable-v1.0.0"
python versioning/Stable-v1.0.0/run_examples.py
python versioning/Stable-v1.0.0/scripts/validate_ecosystem.py
python -m pytest versioning/Stable-v1.0.0/tests
```

Os exemplos mantidos contêm a origem Minerva completa em `docs/L2_MinervaBlueprints/` e seus registros L3 em `docs/L3_Vulcan/`. Ferramentas abstratas tornam-se protocolos, projetos de ferramentas concretas tornam-se adaptadores e boundaries continuam sendo adaptadores de interação. A validação estabelece apenas evidência estrutural e de runtime dentro do escopo declarado.
