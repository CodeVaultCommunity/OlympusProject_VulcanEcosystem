# Alinhamento com o L3 do OAL

[English](OAL-ALIGNMENT.md) · [Fonte fixada](../verification/sources/oal/README.md.txt)

Referência: OAL Stable-v1.0.0, commit `0cc54a19df324ac54857b92b068931cc1b090a10`. A seção ADI define cinco obrigações para uma organização reutilizável de código. O Vulcan as trata assim.

| Obrigação ADI do OAL | Realização e ponto de revisão no Vulcan |
| --- | --- |
| Materializar papéis, dependências, algoritmos e falhas de L2 | Perfil interno opcional; casos invocáveis, entidades canônicas e ferramentas concretas; contratos exatos do Atlas e intenção fixada do Minerva em cada exemplo. |
| Caminho explícito do contexto do ator e autorização em cada caso | Composição resolve a identidade didática; chamadas diretas recebem contexto confiável; cada caso recusa contexto insuficiente antes da validação/persistência, inclusive na consulta composta. |
| Executar ADVS e verificações dos canais com vínculos | Sete testes comportamentais lógicos, 76 cenários e 12 verificações de apoio mapeados em `test-bindings.json`; o runner registra subtestes executados e observações ausentes. HTTP/CLI têm verificações separadas. |
| Selecionar e fornecer colaboradores; cumprir garantias concretas | `AppComposition`, transações SQLite por operação, atualizações condicionais, leituras consistentes, liberação de recursos e certeza das falhas. |
| Evolução, rastreabilidade e evidência | Bytes das fontes fixados, revisão própria dos vínculos, observações L2 por arquivo e relatórios isolados com hashes das fontes e ambiente. |

O mapeamento das fontes/catálogos exige revisão semântica. Aprovação estática e exemplos executados são evidências delimitadas, sem certificar projetos futuros arbitrários. Autenticação de produção, garantias distribuídas e outras linguagens permanecem não verificadas. Nomes, quatro pastas irmãs do núcleo e registro explícito são decisões do Vulcan, não exigências impostas pelo OAL a todo modelo L3.

L1 define comportamento externo requerido; L2 define o programa e a verificação pretendidos; L3 trata a realização concreta; rotas HTTP, formas CLI e projeções de resultados são escolhas L4 mesmo quando seu código compõe um artefato L3. A pasta, sozinha, não determina a camada.
