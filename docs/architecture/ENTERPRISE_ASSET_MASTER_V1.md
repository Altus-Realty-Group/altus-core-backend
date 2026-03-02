# ENTERPRISE ASSET MASTER V1
Status: ACTIVE (Drift-Proof Reference)
Owner: CD v5.1
Last Updated: 2026-03-01

## Purpose
Central SSOT for property asset data across all Altus apps.

## Tables
- assets (root)
- asset_data_raw (immutable payloads)
- asset_specs_reconciled (underwritten truth)

## Rule
Frontends NEVER call CoreLogic/MLS directly. Azure Functions only.
