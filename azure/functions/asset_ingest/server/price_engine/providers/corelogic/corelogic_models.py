from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class CoreLogicPropertyIntelligence:
    avm: int
    flood_zone: str
    parcel_id: str
    beds: int
    baths: float
    sqft: int
    year_built: int

    def to_dict(self) -> dict[str, object]:
        return {
            "AVM": self.avm,
            "FloodZone": self.flood_zone,
            "ParcelId": self.parcel_id,
            "Beds": self.beds,
            "Baths": self.baths,
            "SqFt": self.sqft,
            "YearBuilt": self.year_built,
        }


def mock_property_intelligence() -> CoreLogicPropertyIntelligence:
    return CoreLogicPropertyIntelligence(
        avm=245000,
        flood_zone="X",
        parcel_id="MO-JACKSON-000123456",
        beds=3,
        baths=2.0,
        sqft=1680,
        year_built=1998,
    )
