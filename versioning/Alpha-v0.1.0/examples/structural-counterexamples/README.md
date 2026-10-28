# Structural counterexamples

This fixture is deliberately invalid and is not an executable/conforming ecosystem. Its `launch.py` exists solely to isolate structural diagnostics; file existence never proves startup behavior.

Run from the edition root:

```bash
python scripts/evaluate_structure.py --ecosystem examples/structural-counterexamples/invalid-ecosystem --profile-app BrokenApp --json
```

Expected exit: **1**. The required diagnostic families are published in [expected-diagnostics.json](expected-diagnostics.json): multiple independent structures, filename mismatch, wrong role name, method/attribute casing, missing use-case domain, tool-to-case import, direct tool-to-value-object consumption, entity infrastructure import and a static tool dependency cycle. Line numbers and paths are returned by the actual assessor.

`tests/Test_Structure.py` checks this fixture and complementary temporary fixtures for missing directories/entry, invalid syntax, relative imports and the positive case where documentation lives elsewhere. It also verifies the real TaskBoard scope; legacy internals are explicitly excluded.
