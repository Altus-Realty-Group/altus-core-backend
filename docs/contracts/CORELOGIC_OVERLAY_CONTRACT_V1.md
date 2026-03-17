# CORELOGIC_OVERLAY_CONTRACT_V1

Status: draft, mock-safe only  
Scope: Price Engine property intelligence and map overlay docking surface  
Live paid provider calls: not authorized in this contract slice

## Purpose

This contract defines the backend-ready payload shape the Price Engine frontend can use to dock:

- subject property map coordinates
- parcel boundary geometry
- flood zone overlay geometry
- normalized property intelligence values
- provider/source metadata

This contract is mock-safe and additive. It does not change the existing Price Engine calculate contract.

## Response Shape

```json
{
  "subject": {
    "address": "string",
    "lat": 0,
    "lng": 0
  },
  "overlays": {
    "parcelBoundary": {
      "type": "Polygon",
      "coordinates": [
        [
          [0, 0],
          [0, 0],
          [0, 0],
          [0, 0],
          [0, 0]
        ]
      ]
    },
    "floodZone": {
      "zone": "string",
      "panel": "string",
      "effectiveDate": "YYYY-MM-DD",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
          ]
        ]
      }
    },
    "corelogicLayerStatus": "string"
  },
  "propertyIntelligence": {
    "avm": null,
    "beds": null,
    "baths": null,
    "sqFt": null,
    "yearBuilt": null
  },
  "meta": {
    "provider": "string",
    "mock": true,
    "approvalRequired": true
  }
}
```

## Field Notes

- `subject.address`: normalized display address for the mapped subject property.
- `subject.lat` / `subject.lng`: frontend-ready coordinates for map centering and pin placement.
- `overlays.parcelBoundary`: mock-safe GeoJSON-compatible polygon using `[lng, lat]` coordinate pairs.
- `overlays.floodZone`: zone metadata plus a mock-safe `geometry` object using the same GeoJSON-compatible polygon shape.
- `overlays.corelogicLayerStatus`: quick provider state signal for UI overlay controls.
- `propertyIntelligence`: normalized property facts the frontend can display without vendor-specific field names.
- `meta.provider`: current provider identity, expected to be `corelogic` for this surface.
- `meta.mock`: explicit indicator that this payload is deterministic mock data.
- `meta.approvalRequired`: explicit guardrail indicator that live paid provider activation still requires operator approval.

## Geometry Shape

The canonical mock-safe geometry shape for map layers is:

```json
{
  "type": "Polygon",
  "coordinates": [
    [
      [lng, lat],
      [lng, lat],
      [lng, lat],
      [lng, lat],
      [lng, lat]
    ]
  ]
}
```

- Coordinates are GeoJSON-compatible and ordered as `[longitude, latitude]`.
- The first and last coordinate pair should match so the polygon ring is closed.
- Frontend consumers may transform these values into the map library coordinate order they require.

## Mock Notes

- This contract is currently satisfied by deterministic mock payload generation only.
- No live CoreLogic request is permitted through this surface.
- Parcel boundary and flood geometry are deterministic mock polygons until provider approval and implementation are authorized.
