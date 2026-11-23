# FraudPulse

Real-time fraud detection on AWS: Kafka, PySpark, a rule engine plus ML scoring, and an LLM layer for alert explanations.

**Status: Week 1 of 12 (foundations).** Nothing is measured yet. Every number in this project will go into [RESULTS.md](RESULTS.md) with the load, the method and the commit that produced it. Empty rows mean not measured yet.

## What exists today

- A validated transaction event schema (pydantic v2): UTC-only timestamps, positive integer amounts, strict field checks, no unknown fields.
- Tests and linting that run on every push (GitHub Actions: `ruff` and `pytest`).

## What I am building (planned, not built yet)

| Part | Plan |
|---|---|
| Event stream | Kafka (local Docker first), versioned event schema, synthetic transaction producer |
| Rules | Pure-Python rule engine: velocity, impossible travel, amount anomaly |
| Real-time scoring | PySpark Structured Streaming, state keyed by account, event-time rules with late-data handling |
| Alerts | DynamoDB table, one row per flagged transaction |
| Batch and ML | Databricks Free Edition: lakehouse tables, feature engineering, model training |
| LLM layer | Bedrock-generated alert explanations, with an evaluation set |
| Infrastructure | Terraform for the AWS resources |

Design rule: the pipeline never sees the fraud label. The ground truth lives in a held-back file used only for evaluation.

## Repository layout

```
src/fraudpulse/
  schema.py      transaction event contract
  rules/         pure functions only (no Kafka, Spark or AWS imports)
  producer/      synthetic transaction generator
tests/           pytest
.github/workflows/ci.yml
RESULTS.md       measured results (empty until measured)
```

## Development setup

Requires Python 3.12 (pinned to match Databricks serverless).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
ruff check .
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

## Roadmap

12 weeks, from foundations through streaming, batch and ML, the LLM layer, and a measured RESULTS.md. Each week ends with something that runs.