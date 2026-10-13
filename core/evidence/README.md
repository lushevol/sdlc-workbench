# Evidence responsibility

The existing `src/ai_sdlc_workbench/store.py` implementation retains resource action records and result hashes.
Hashes identify retained bytes; they do not establish business approval or actual execution authenticity.
Keep observations, inferences, and unresolved claims separate.
Complete behavior evidence validation requires further implementation.
