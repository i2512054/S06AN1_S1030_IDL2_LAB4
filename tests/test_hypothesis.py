from xml.sax.saxutils import escape

from hypothesis import given, strategies as st

from models.claim_schema import ItemReclamado
from services.claim_transformer import ClaimTransformerService

# Solo caracteres válidos en XML 1.0 (sin controles ni surrogates) y sin espacios en los extremos
safe_text = lambda min_size, max_size: st.text(
    alphabet=st.characters(
        blacklist_categories=("Cs", "Cc"),
        blacklist_characters="\x7f",
    ),
    min_size=min_size,
    max_size=max_size,
).filter(lambda s: s == s.strip() and len(s) >= min_size)

st_item = st.builds(
    ItemReclamado,
    item_id=safe_text(1, 10),
    descripcion=safe_text(3, 30),
    monto_estimado=st.floats(min_value=1.0, max_value=10000.0),
    categoria=st.sampled_from(["vehicular", "hogar", "salud"]),
)


@given(
    claim_id=safe_text(3, 10),
    poliza_num=safe_text(1, 10).map(lambda s: f"POL-{s}"),
    cliente_id=safe_text(3, 10),
    monto=st.floats(min_value=0.0, max_value=100000.0),
    descripcion=safe_text(5, 100),
    items=st.lists(st_item, min_size=1, max_size=5),
)
def test_xml_generation_and_parsing_property(
    claim_id, poliza_num, cliente_id, monto, descripcion, items
):
    items_xml = "".join(
        f"<item><item_id>{escape(i.item_id)}</item_id>"
        f"<descripcion>{escape(i.descripcion)}</descripcion>"
        f"<monto_estimado>{i.monto_estimado}</monto_estimado>"
        f"<categoria>{i.categoria}</categoria></item>"
        for i in items
    )

    xml_str = (
        "<reclamacion>"
        f"<id_reclamacion>{escape(claim_id)}</id_reclamacion>"
        f"<numero_poliza>{escape(poliza_num)}</numero_poliza>"
        f"<id_cliente>{escape(cliente_id)}</id_cliente>"
        "<fecha_incidente>2026-11-09</fecha_incidente>"
        "<tipo_siniestro>Accidente</tipo_siniestro>"
        f"<monto_total_reclamado>{monto}</monto_total_reclamado>"
        f"<descripcion_hechos>{escape(descripcion)}</descripcion_hechos>"
        f"<items>{items_xml}</items>"
        "</reclamacion>"
    )

    result_json = ClaimTransformerService.process_xml_to_ai_json(xml_str)

    assert "metadata" in result_json
    assert "canonical_text_for_embedding" in result_json
    assert result_json["metadata"]["id_reclamacion"] == claim_id
    assert result_json["metadata"]["id_cliente"] == cliente_id