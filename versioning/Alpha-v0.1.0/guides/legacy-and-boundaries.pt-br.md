# Outras arquiteturas e fronteiras

[English](legacy-and-boundaries.md)

Um aplicativo pode manter handlers procedurais, framework ou outra arquitetura interna. Declarar operações públicas reais, contratos dos canais, configuração e partes avaliadas/não avaliadas. Participar do Vulcan Ecosystem não concede conformidade Vulcan Architecture.

A [fixture legada](../tests/fixtures/legacy-ecosystem/README.pt-br.md) mantém LegacyReports consumindo o TaskBoard da fixture por HTTP público, sem importar classes privadas nem abrir seu banco. Verifica compatibilidade pública, inclusão de dependências de inicialização e limpeza. IDs gerados/títulos normalizados/conclusão idempotente antigos pertencem somente à fixture; os exemplos canônicos seguem o Atlas.

Casos do perfil são invocáveis independentemente de HTTP/CLI. Fronteiras resolvem contexto confiável e projetam resultados; casos autorizam e definem seus algoritmos. Interação é identificada como L4. Aplicativos se integram por contratos públicos documentados; atalhos de transporte/banco não os substituem.
