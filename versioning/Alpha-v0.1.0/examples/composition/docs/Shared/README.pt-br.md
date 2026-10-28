# Interação e premissas compartilhadas

[English](README.md) · [Realização](../L3_Vulcan/README.pt-br.md)

Nomes das operações HTTP POST e argumentos JSON da CLI são escolhas L4. Sucesso retorna `result`; recusa/falha retorna `error`; incerteza de armazenamento acrescenta `write_outcome` (`not_applied` ou `unknown`). HTTP usa 403 para recusa de acesso, 400 para entrada inválida, 409 para conflito/ausência de domínio, 503 para armazenamento indisponível e 500 para estado persistido inválido. Esses códigos são projeções, não casos de domínio adicionais.

Somente a composição confiável resolve o token local. Um objeto de ator enviado pelo chamador não concede acesso. Chamadas diretas exigem contexto confiável fornecido pela aplicação que incorpora o núcleo. Token padrão e endereço local são didáticos, sem intenção de implantação. Os exemplos canônicos não incluem interface de navegador.
