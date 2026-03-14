# ECC_CONTRACT_COVERAGE_INDEX_V1

Status: Core-lane ECC contract coverage index
Scope: Discovered ECC HTTP routes in `azure/functions/asset_ingest/function_app.py`

This index records the current proof-bearing contract coverage for the discovered ECC route surface on `main`.

## Coverage Summary

All discovered ECC routes currently have:
- route-scoped contract documentation
- route-scoped proof fixtures
- route-scoped contract tests
- route-scoped CI workflows

## Route Coverage Index

| Route | Contract doc | Fixtures | Contract test | Route-scoped CI workflow | Current proof status |
| --- | --- | --- | --- | --- | --- |
| `GET /api/ecc/system/health` | `docs/contracts/ECC_SYSTEM_HEALTH_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_system_health/` | `tests/contracts/test_ecc_system_health_contract.py` | `.github/workflows/ecc_system_health_contract_proof.yml` | live on `main` |
| `GET /api/ecc/portfolio/summary` | `docs/contracts/ECC_PORTFOLIO_SUMMARY_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_portfolio_summary/` | `tests/contracts/test_ecc_portfolio_summary_contract.py` | `.github/workflows/ecc_portfolio_summary_contract_proof.yml` | live on `main` |
| `GET /api/ecc/portfolio/assets` | `docs/contracts/ECC_PORTFOLIO_ASSETS_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_portfolio_assets/` | `tests/contracts/test_ecc_portfolio_assets_contract.py` | `.github/workflows/ecc_portfolio_assets_contract_proof.yml` | live on `main` |
| `GET /api/ecc/assets/search` | `docs/contracts/ECC_ASSET_SEARCH_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_asset_search/` | `tests/contracts/test_ecc_asset_search_contract.py` | `.github/workflows/ecc_asset_search_contract_proof.yml` | live on `main` |
| `GET /api/ecc/assets/metrics` | `docs/contracts/ECC_ASSET_METRICS_CONTRACT_V1.md` | `docs/contracts/fixtures/ecc_asset_metrics/` | `tests/contracts/test_ecc_asset_metrics_contract.py` | `.github/workflows/ecc_asset_metrics_contract_proof.yml` | live on `main` |

## Audit Basis

The route inventory above is grounded in the current route declarations in `azure/functions/asset_ingest/function_app.py`.

## Maintenance Rule

If a discovered ECC route changes contract shape, its contract doc, fixtures, test module, and route-scoped CI workflow must be updated in the same PR.
