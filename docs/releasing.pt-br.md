# Preparação de uma entrega do Vulcan Ecosystem

[English](releasing.md) · [Início](../README.pt-br.md) · [Guia de agentes](../AGENTS.md)

Este procedimento valida a distribuição do repositório para a edição indicada por `VERSION`, atualmente Stable-v1.0.0. Ele atualiza essa edição estável no próprio lugar conforme autorizado; não cria outra edição nem autoriza publicação remota.

## 1. Finalizar e verificar

Preserve as árvores completas de origem Minerva e suas identidades Atlas. Confirme que cada módulo Minerva executável ou testável tem um destino de realização, que projetos de ferramentas concretas são realizados por adaptadores, que Boundary continua sendo um adaptador de interação e que a evidência de runtime declara seu escopo e limites.

```bash
python -m pip install -r scripts/requirements-dev.txt
python scripts/check_repository.py
python -m pytest scripts/tests
python -m pip install -e "versioning/Stable-v1.0.0"
python versioning/Stable-v1.0.0/run_examples.py
python versioning/Stable-v1.0.0/scripts/validate_ecosystem.py
python -m pytest versioning/Stable-v1.0.0/tests
```

Se fontes de arte mudarem, instale `assets/requirements-artwork.txt`, regenere com `assets/sources/render_images.py` e inspecione as imagens derivadas.

## 2. Gerar por último o inventário de bytes exatos

`CONTENT-SHA256.json` cobre todos os arquivos de entrega presentes e não ignorados reportados pelo Git, exceto ele próprio. Inclui arquivos não rastreados preparados intencionalmente e registra caminhos POSIX relativos, tamanhos exatos e valores SHA-256.

```bash
python scripts/content_inventory.py --write
python scripts/content_inventory.py --check
git status --short
```

Revise todas as mudanças e garanta que caches, bancos de dados, saídas temporárias e ambientes locais continuem ignorados. O histórico de release pertence à edição e aos registros de lançamento; não há changelog separado.

## 3. Construir uma distribuição commitada somente com autorização

Depois de um commit local autorizado separadamente deixar a árvore limpa:

```bash
python scripts/build_distribution.py --output /absolute/path/OlympusProject_VulcanEcosystem_Stable-v1.0.0.zip
python scripts/check_archive.py /absolute/path/OlympusProject_VulcanEcosystem_Stable-v1.0.0.zip
```

Mantenha externos o recibo e o hash do ZIP. Uma verificação, arquivo ou commit local bem-sucedido não autoriza push, tag, release nem alegações de execução hospedada.
