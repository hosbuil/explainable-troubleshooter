# Explainable Troubleshooter

A small Python CLI that turns user-reported device and network observations into transparent next-step recommendations. Python 3.10+; no external dependencies.

## Origin and status

Created on 23 October 2026 with OpenAI Codex. The initial implementation, tests and documentation were AI-generated at the repository owner's request. This is a learning scaffold, not evidence of independent implementation or earlier work. Personal contributions should be recorded in future commits as they happen.

## Run

```sh
python3 troubleshoot.py --input examples/dns.json
python3 troubleshoot.py
python3 -m unittest -v
```

The example recommends a **DNS check**, showing the exact observations that matched. The interactive mode accepts `y`, `n` and `?` (unknown). JSON input accepts booleans or null and rejects unrecognized keys or other value types.

## How it works

Six explicit rules cover power, Wi-Fi connectivity, upstream connectivity, name resolution, a site-specific failure and storage. A rule matches only when every required observation is known and agrees. Missing evidence leaves the rule pending; a contradiction rules it out. Several recommendations may match together. Output includes matched evidence, pending rules and unanswered questions.

These are fixed rules, not machine learning or an LLM. Recommendations are hypotheses and next checks, not confirmed diagnoses. In the site-specific rule, the user is assumed to be investigating a target site that already fails.

## Limits

- No automatic device inspection, networking, telemetry, account access or system modification.
- Observations can be inconsistent or mistaken. No causal diagnosis is guaranteed.
- Six handcrafted rules do not represent comprehensive technical support.
- Tests check rule behavior, unknown inputs and validation. They do not measure real-world diagnostic accuracy.

## Your first contribution

1. Run the DNS example and explain why Wi-Fi and upstream rules did not match.
2. Change `dns` to null and predict the output before running it.
3. Add a browser-cache observation and a narrowly defined recommendation; add a test for unknown evidence and one for contradictory evidence.
4. Commit your change with a short explanation of the design choice.

Do not put passwords, private logs or real personal data in examples. Record measured results only after actually running an evaluation.
