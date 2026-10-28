# Bundled Minerva validator

This copy makes the Vulcan Alpha-v0.1.0 edition self-contained. Its runtime, schema, command-line wrapper, dependency declaration and license are byte-for-byte copies from Minerva Blueprints Alpha-v0.1.0. [SOURCE.json](SOURCE.json) records their provenance and hashes. The full Minerva model, authoring guides, negative fixtures and validator tests are provided in the companion repository distribution.

Install the Vulcan edition's `requirements.txt`, then use the edition runner's `verify` command. The copied CLI uses its own adjacent package; it does not silently fall back to another installation or edition. It reads YAML and source bytes without importing or executing project code. Code execution belongs to Vulcan's explicit test command.

Copy updates deliberately from the selected Minerva edition, update the source record, rerun verification and regenerate the repository's single content inventory last. Do not fix the copy while leaving its declared source unchanged.
