# Commercial deployment profile

OBLIVION TextLM is a proprietary query-relative language-model system powered by the OBLIVION
inference-control architecture and a separately licensed pretrained language-model executor.

## Recommended topology

1. Run a commercially permitted OpenAI-compatible executor endpoint. The reference profile is
   Mistral Small 4; its model weights are not bundled with OBLIVION TextLM.
2. Optionally run a smaller control-plane model for `G_theta`, `B_theta`, `P_theta`, and `V_Q`
   when matched benchmarks show a lower total cost without unacceptable quality loss.
3. Run the OBLIVION TextLM FastAPI service as the proprietary control plane.
4. Put the API behind TLS termination, a reverse proxy or API gateway, WAF/rate controls, and
   centralized secret management.
5. Deploy the Streamlit console as a separate frontend. Store its backend API key only in
   server-side environment variables or Streamlit secrets.
6. Export `/metrics` to the organization's observability stack and retain only the data required by
   the deployment's privacy policy.
7. Benchmark the same executor weights under full-context, ordinary retrieval, and OBLIVION
   policies before making efficiency claims.

## Minimum production controls

- private source repository under the proprietary license
- strong per-environment API credentials
- TLS at every public boundary
- secret manager rather than committed `.env` files
- tenant-appropriate authentication and authorization upstream of the demonstration API-key layer
- rate limiting, WAF rules, request-size limits, and abuse monitoring
- encrypted storage/logging where retained
- model, prompt, package, and container version pinning
- dependency/SBOM and vulnerability scanning
- rollbackable image releases
- prompt-injection and evidence-spoofing tests
- quality, latency, and controller-overhead regression gates
- data-retention and deletion policy appropriate to the deployment

## Efficiency claim gate

Do not advertise a reduction in active text as a hardware or monetary saving by itself. A
commercial claim should be supported by matched end-to-end measurements of answer quality,
latency, throughput, GPU/accelerator utilization, memory, model-call count, and controller cost.
The OBLIVION/SHC audit is intended to expose displaced work rather than hide it.

## Physical KV-cache boundary

This release implements task-relative text routing into the executor. It does not claim generic
physical eviction of arbitrary internal KV-cache blocks in third-party serving engines. A custom
runtime may map discharged obligations to cache blocks, but such an integration is a separate
systems optimization and must be benchmarked on the deployed hardware.

## License boundary

The proprietary OBLIVION TextLM source does not include or relicense Mistral weights or other
third-party components. Preserve all third-party notices required by the selected model and serving
stack. The OBLIVION research/reproducibility release remains a separate project under the license
stated by that release.
