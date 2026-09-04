# Security

The API requires bearer authentication on inference and metrics routes. The bundled in-memory
rate limiter is suitable for a single-process deployment; distributed production deployments
should enforce limits at the gateway or a shared rate-limit service.

Do not commit `.env`, model credentials, private datasets, customer prompts, model weights, or
production traces. Disable trace return where evidence or internal task state is sensitive.

Treat model-generated certificates as untrusted structured data. The implementation validates
referenced evidence IDs against the active evidence set and applies confidence thresholds, but a
generic LLM verifier is not a formal proof checker. High-assurance domains should replace it
with a domain-specific sound verifier.

Report security issues through the private commercial support channel associated with the
software license agreement.
