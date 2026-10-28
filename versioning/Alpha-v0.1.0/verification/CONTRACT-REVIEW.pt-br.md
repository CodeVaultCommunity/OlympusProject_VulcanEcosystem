# Revisão de preservação dos contratos

[English](CONTRACT-REVIEW.md) · [Método de integração](../integrations/minerva/README.pt-br.md)

Os bytes JSON canônicos do Atlas são copiados sem alteração. Blueprints originais do Minerva ficam fixados separadamente; revisões locais preservam ADPM e intenção dos cenários, acrescentando observações das fontes e referências de testes. Os metadados mantêm revisão pendente pelo responsável. O Minerva local mudou durante o trabalho; seus vínculos esclarecidos de qualidade e listas de invariantes canônicas foram incorporados antes da verificação final.

Minimal preserva códigos exatos sensíveis a maiúsculas e quantidades inteiras positivas; duplicata não substitui dados. Booking preserva códigos em maiúsculas, autorização independente da consulta, composição com o mesmo contexto e gravações por versão esperada. TaskBoard preserva identificadores/títulos exatos informados, contexto por quadro, revisão zero na criação, recusa de conclusão repetida, incremento condicional e listagem ordenada consistente.

Falhas SQLite distinguem recusa confirmada/not_applied de confirmação de gravação incerta; não há repetição automática. Testes aplicam uma gravação e perdem a confirmação para verificar que unknown não vira falso sucesso/ausência de mudança. A qualidade compartilhada de Booking permanece o procedimento de criação da fonte; latência específica do cancelamento é questão aberta. Observação inferida do código ou teste aprovado não constitui aceite do responsável.

Resultados rastreáveis, hashes e limites operacionais estão no [recibo atual](RELEASE.pt-br.md), não nesta narrativa de revisão semântica.
