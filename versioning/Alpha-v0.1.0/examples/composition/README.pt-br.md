# composition — BookingDesk

[English](README.md) · [Fonte Atlas](docs/L1_AtlasSpecifications/example.atlas.json) · [Minerva](docs/L2_MinervaBlueprints/blueprint.yaml) · [Realização](docs/L3_Vulcan/README.pt-br.md)

Realização concreta Python/SQLite do exemplo canônico correspondente do Atlas Stable-v1.0.0 e Minerva Alpha-v0.1.0. Operações JSON públicas: `lookup(booking_code), create(booking_code, title), cancel(booking_code)`. Envie POST para o nome da operação em `/`; use Bearer `demo-editor` na demonstração local. O chamador fornece o identificador de domínio; o texto é preservado.

```sh
python launch.py list
python launch.py start --all --port 8765 --duration 10
python ../../run_examples.py test --example composition
```

O modo padrão é HTTP local. CLI usa `--mode cli --operation NOME --payload JSON`; defina `VULCAN_CALLER_TOKEN=demo-editor` no shell. `--db` seleciona o SQLite e `--board` seleciona o quadro TaskBoard. Veja [execução](../../guides/execution.pt-br.md) para comandos e ciclo de vida. A composição resolve o contexto; um objeto de ator enviado no JSON não é aceito. Chamadores internos diretos são confiáveis para construir contexto autêntico.

ADPM/cenários herdados mantêm seus IDs. Revisão local dos vínculos e hashes estão nos [vínculos de testes](docs/L3_Vulcan/test-bindings.json). YAML por arquivo permanece em L2; resultados ficam nas [execuções de verificação](../../verification/README.pt-br.md) da edição. Não se afirma autenticação de produção ou aceite do responsável.
