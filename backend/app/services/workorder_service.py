import json
from datetime import datetime, timezone
from uuid import uuid4

from app.db.session import get_connection
from app.schemas.chat_schema import SourceItem
from app.schemas.workorder_schema import WorkOrderCreateRequest, WorkOrderItem


class WorkOrderNotFoundError(Exception):
    """Raised when a work order id does not exist."""


class WorkOrderService:
    def list_workorders(self) -> list[WorkOrderItem]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT work_order_id, equipment_type, fault_symptom, fault_understanding,
                       possible_causes_json, repair_steps_json, safety_notes_json,
                       safety_actions_json, sources_json, operator_note, status, created_at
                FROM workorders
                ORDER BY created_at DESC
                """
            ).fetchall()

        return [self._row_to_item(row) for row in rows]

    def get_workorder(self, work_order_id: str) -> WorkOrderItem:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT work_order_id, equipment_type, fault_symptom, fault_understanding,
                       possible_causes_json, repair_steps_json, safety_notes_json,
                       safety_actions_json, sources_json, operator_note, status, created_at
                FROM workorders
                WHERE work_order_id = ?
                """,
                (work_order_id,),
            ).fetchone()

        if row is None:
            raise WorkOrderNotFoundError("未找到对应检修记录。")
        return self._row_to_item(row)

    def create_workorder(self, payload: WorkOrderCreateRequest) -> WorkOrderItem:
        work_order_id = f"wo-{uuid4().hex[:10]}"
        created_at = datetime.now(timezone.utc).isoformat()
        status_value = "created"

        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO workorders (
                    work_order_id, equipment_type, fault_symptom, fault_understanding,
                    possible_causes_json, repair_steps_json, safety_notes_json,
                    safety_actions_json, sources_json, operator_note, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    work_order_id,
                    payload.equipment_type,
                    payload.fault_symptom,
                    payload.fault_understanding,
                    json.dumps(payload.possible_causes, ensure_ascii=False),
                    json.dumps(payload.repair_steps, ensure_ascii=False),
                    json.dumps(payload.safety_notes, ensure_ascii=False),
                    json.dumps(payload.safety_actions, ensure_ascii=False),
                    json.dumps(
                        [source.model_dump() for source in payload.sources],
                        ensure_ascii=False,
                    ),
                    payload.operator_note,
                    status_value,
                    created_at,
                ),
            )

        return WorkOrderItem(
            work_order_id=work_order_id,
            equipment_type=payload.equipment_type,
            fault_symptom=payload.fault_symptom,
            fault_understanding=payload.fault_understanding,
            possible_causes=payload.possible_causes,
            repair_steps=payload.repair_steps,
            safety_notes=payload.safety_notes,
            safety_actions=payload.safety_actions,
            sources=payload.sources,
            operator_note=payload.operator_note,
            status=status_value,
            created_at=created_at,
        )

    def _row_to_item(self, row) -> WorkOrderItem:
        sources = [
            SourceItem(**source)
            for source in self._loads_json(row["sources_json"], default=[])
            if isinstance(source, dict)
        ]
        return WorkOrderItem(
            work_order_id=row["work_order_id"],
            equipment_type=row["equipment_type"],
            fault_symptom=row["fault_symptom"],
            fault_understanding=row["fault_understanding"],
            possible_causes=self._loads_json(row["possible_causes_json"], default=[]),
            repair_steps=self._loads_json(row["repair_steps_json"], default=[]),
            safety_notes=self._loads_json(row["safety_notes_json"], default=[]),
            safety_actions=self._loads_json(row["safety_actions_json"], default=[]),
            sources=sources,
            operator_note=row["operator_note"],
            status=row["status"],
            created_at=row["created_at"],
        )

    def _loads_json(self, value: str, default):
        try:
            payload = json.loads(value)
        except json.JSONDecodeError:
            return default
        return payload if isinstance(payload, type(default)) else default
