# Registros de verificação

[English](README.md) · [Recibo atual](RELEASE.pt-br.md) · [Requisitos](REQUIREMENTS.pt-br.md) · [Revisão dos contratos](CONTRACT-REVIEW.pt-br.md)

`source-baselines.json` fixa snapshots exatos das entradas OAL/Atlas/Minerva. `sources/` contém documentos de entrada, sem código copiado do validador. `requirements/` preserva IDs do catálogo e mapeamento delimitado da entrega. `runs/<id>/` contém execuções observadas imutáveis; cada chamada cria uma pasta. `reviews/baseline-78232f2/` preserva relatórios recebidos antes desta revisão apenas como evidência histórica.

`test-bindings.json` em cada exemplo identifica cenários/apoios esperados e testes nativos. O relatório registra separadamente subtestes reais, estados, hashes de entradas/fontes, plataforma, tempos e testes ignorados. Estrutura e Minerva têm relatórios próprios. O resultado geral não pode passar com cenário esperado ausente ou integração exigida indisponível.
