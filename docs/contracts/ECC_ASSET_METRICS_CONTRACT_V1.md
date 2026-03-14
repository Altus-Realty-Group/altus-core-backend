# ECC_ASSET_METRICS_CONTRACT_V1

Status: Core-lane contract baseline
Route: `GET /api/ecc/assets/metrics`
Runtime owner: `azure/functions/asset_ingest/ecc_asset_metrics_handler.py`

This document records the currently executable contract for the ECC asset metrics route. It is grounded in the live handler and service code on `main`.

## Current Behavior

- Requires the `assetId` query parameter.
- Accepts optional `windowDays` query parameter.
- Returns a `200` JSON object on success.
- Returns a `400` JSON error envelope when `assetId` is missing or `windowDays` is invalid.
- Returns a `500` JSON error envelope only when an unexpected internal exception occurs.
- Adds response headers for build identity and ECC handler/domain identity.
- Returns a deterministic payload today from in-code service logic derived from `assetId` and `windowDays`.

## Request Contract

Required query parameters:
- `assetId`

Optional query parameters:
- `windowDays`

Current validation rules:
- `windowDays` defaults to `30`
- `windowDays` must be an integer
- `windowDays` must be `1..365`

## Success Contract

Status code:
- `200`

Required headers:
- `x-altus-build-sha`
- `x-ecc-handler`
- `x-ecc-domain-signature`

Response shape:

```json
{
  "data": {
    "assetId": "asset-001",
    "windowDays": 30,
    "occupancyRate": 0.22,
    "maintenanceCostRatio": 0.19,
    "collectionsRate": 0.94,
    "delinquentUnits": 4,
    "openWorkOrders": 6,
    "netOperatingIncome": 24000.0,
    "currency": "USD",
    "lastUpdatedAt": null
  }
}
```

Deterministic behavior grounded in current code:
- top-level payload is wrapped in `data`
- `assetId` echoes the required query parameter
- `windowDays` echoes the validated/defaulted query parameter
- metrics fields are derived deterministically from the `assetId` character seed
- `currency` is currently `USD`
- `lastUpdatedAt` is currently `null`
- `x-ecc-handler` is `ecc-asset-metrics`
- `x-ecc-domain-signature` is `ecc.asset.metrics.v1`

## Error Contract

Status code:
- `400` when required or `windowDays` inputs are invalid
- `500` for unexpected internal failures

Response shape:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "human readable message"
  }
}
```

Named error codes currently observed in code:
- `VALIDATION_FAILED`
- `INTERNAL_ERROR`

Observed validation messages in code include:
- `assetId is required`
- `windowDays must be an integer`
- `windowDays must be 1..365`

## Proof Fixtures

The proof-bearing fixtures for this route live under:

- `docs/contracts/fixtures/ecc_asset_metrics/success_response.json`
- `docs/contracts/fixtures/ecc_asset_metrics/error_missing_asset_id_response.json`
- `docs/contracts/fixtures/ecc_asset_metrics/error_invalid_window_days_response.json`
- `docs/contracts/fixtures/ecc_asset_metrics/error_internal_response.json`

## Proof Rules

- If the response payload, handler headers, or deterministic service logic changes, the fixtures and tests must change in the same PR.
- If the route begins reading additional request inputs later, the request contract and proof fixtures must be expanded in the same PR.
- This contract does not claim persistence behavior because the current implementation returns deterministic in-code metrics data only.
