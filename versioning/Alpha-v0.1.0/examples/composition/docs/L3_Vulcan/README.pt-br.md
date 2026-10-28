# BookingDesk: realização concreta

[English](README.md) · [Inventário](realization.json) · [Vínculos de testes](test-bindings.json) · [Procedimento de integração](../../../../integrations/minerva/README.pt-br.md)

`AppComposition` escolhe SQLite e injeta colaboradores concretos. O caso autoriza primeiro; entidades canônicas mantêm validade intrínseca. `Boundary_Json` projeta resultados para HTTP e CLI; essas escolhas são L4. Os casos são invocáveis sem esses canais.

A ferramenta vive durante a aplicação; conexões vivem por operação e fecham em `finally`. Transações explícitas cobrem leituras/gravações. Gravações condicionais usam `BEGIN IMMEDIATE`; confirmação perdida preserva `unknown` e nunca inicia repetição automática. Hidratação de registros brutos usa o construtor canônico. O operador é dono do banco; encerrar não o apaga.

`Main` é a pasta concreta de domínio dos casos. A fonte selecionada não nomeia um domínio. `task_id` nativo corresponde a `task_identifier` de L2; o quadro é fixado na ferramenta pela composição e conferido no contexto do chamador. Esse vínculo físico preserva escopo sem repetir o parâmetro em cada método concreto.

O snapshot do blueprint projetado fica nas fontes de verificação da edição. A revisão local acrescenta observações e referências de testes de apoio. Mapeamentos planejados ficam separados de resultados. Ao mudar, rastrear critério-fonte → caso/entidade/ferramenta → composição/canal → cenário/apoio → espelho → nova evidência. Revisar intenção antes de atualizar hashes.

Limites: SQLite local e identidade didática; doubles exercitam tratamento da incerteza, sem demonstrar durabilidade física diante de falta de energia. O relatório delimita cada teste e medição.
