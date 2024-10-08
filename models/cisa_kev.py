from datetime import date, datetime, timezone
from typing import Dict, Any, List, Iterator
import json
from pydantic import BaseModel, Field

class KEV(BaseModel):
    cve_id: str = Field(primary_key=True)
    data: str
    first_seen: date
    last_modified: date = Field(default_factory=date.today)
    ingest_ts: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Ingestion timestamp"
    )

class Response(BaseModel):
    data: List[Dict[str, Any]]

    def get_data(self) -> Iterator[Dict[str, Any]]:
        for rows in self.data:
            row = KEV(
                cve_id=rows.get('cveID', ''),
                data=json.dumps(rows),
                first_seen=rows.get('dateAdded', ''),
            )
            yield row

def parse_data(raw_data: Dict[str, Any]) -> Response:
    return Response(**raw_data)
