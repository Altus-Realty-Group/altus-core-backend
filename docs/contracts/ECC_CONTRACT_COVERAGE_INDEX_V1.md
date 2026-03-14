# ECC Contract Coverage Index V1

## Purpose

Record the current proof-bearing contract coverage for the discovered ECC routes on `main`.

## Coverage Index

| Route | Contract Doc | Fixtures | Contract Test | Route-Scoped CI Workflow | Current Proof Status |
| --- | --- | --- | --- | --- | --- |
| `GET /api/ecc/system/health` | `docs/contracts/ECC_SYSTEM_HEALTH_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_system_health/` | `tests/contracts/test_ecc_system_health_contract.py` | `.github/workflows/ecc_system_health_contract_proof.yml` | Proof-bearing package present |
| `GET /api/ecc/portfolio/summary` | `docs/contracts/ECC_PORTFOLIO_SUMMARY_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_portfolio_summary/` | `tests/contracts/test_ecc_portfolio_summary_contract.py` | `.github/workflows/ecc_portfolio_summary_contract_proof.yml` | Proof-bearing package present |
| `GET /api/ecc/portfolio/assets` | `docs/contracts/ECC_PORTFOLIO_ASSETS_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_portfolio_assets/` | `tests/contracts/test_ecc_portfolio_assets_contract.py` | `.github/workflows/ecc_portfolio_assets_contract_proof.yml` | Proof-bearing package present |
| `GET /api/ecc/assets/search` | `docs/contracts/ECC_ASSET_SEARCH_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_asset_search/` | `tests/contracts/test_ecc_asset_search_contract.py` | `.github/workflows/ecc_asset_search_contract_proof.yml` | Proof-bearing package present |
| `GET /api/ecc/assets/metrics` | `docs/contracts/ECC_ASSET_METRICS_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_asset_metrics/` | `tests/contracts/test_ecc_asset_metrics_contract.py` | `.github/workflows/ecc_asset_metrics_contract_proof.yml` | Proof-bearing package present |

## Audit Notes

- This index is grounded in route declarations under `azure/functions/asset_ingest/function_app.py`.
- Coverage status here means the route currently has all four required proof surfaces in repo truth:
  - contract doc
  - fixtures
  - contract test
  - route-scoped contract proof workflow
- This index does not assert that all proofs ran in the current PR; it records that the proof-bearing package exists on `main`.
