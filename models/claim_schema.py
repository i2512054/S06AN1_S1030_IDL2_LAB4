from typing import List

from pydantic import BaseModel, Field, field_validator


class ItemReclamado(BaseModel):
    item_id: str
    descripcion: str
    monto_estimado: float = Field(gt=0, description="El monto debe ser mayor a cero")
    categoria: str


class ReclamacionInsurance(BaseModel):
    id_reclamacion: str
    numero_poliza: str
    id_cliente: str
    fecha_incidente: str
    tipo_siniestro: str
    monto_total_reclamado: float = Field(ge=0)
    descripcion_hechos: str
    items: List[ItemReclamado]

    @field_validator("numero_poliza")
    @classmethod
    def validar_poliza(cls, v: str) -> str:
        if not v.startswith("POL-"):
            raise ValueError("El número de póliza debe iniciar con el prefijo 'POL-'")
        return v

    def to_ai_embedding_payload(self) -> dict:
        text_context = (
            f"Siniestro: {self.tipo_siniestro}. "
            f"Descripción: {self.descripcion_hechos}. "
            f"Póliza: {self.numero_poliza}. "
            f"Monto Total: S/. {self.monto_total_reclamado:.2f}. "
            f"Items involucrados: {', '.join(i.descripcion for i in self.items)}."
        )
        return {
            "metadata": {
                "id_reclamacion": self.id_reclamacion,
                "id_cliente": self.id_cliente,
                "fecha_incidente": self.fecha_incidente,
                "monto_total": self.monto_total_reclamado,
            },
            "canonical_text_for_embedding": text_context,
        }