import xml.etree.ElementTree as ET
from typing import Dict, Any
class XMLClaimParser:
    @staticmethod
    def parse_xml_content(xml_string: str) -> Dict[str, Any]:
        try:
            root = ET.fromstring(xml_string)
            items_list = []
            items_node = root.find("items")
            if items_node is not None:
                for item_elem in items_node.findall("item"):
                    items_list.append({
                        "item_id": item_elem.findtext("item_id", ""),
                        "descripcion": item_elem.findtext("descripcion", ""),
                        "monto_estimado": float(item_elem.findtext("monto_estimado", "0.0")),
                        "categoria": item_elem.findtext("categoria", "general"),
                    })
			
            data = {
                "id_reclamacion": root.findtext("id_reclamacion", ""),
                "numero_poliza": root.findtext("numero_poliza", ""),
                "id_cliente": root.findtext("id_cliente", ""),
                "fecha_incidente": root.findtext("fecha_incidente", ""),
                "tipo_siniestro": root.findtext("tipo_siniestro", ""),
                "monto_total_reclamado": float(root.findtext("monto_total_reclamado", "0.0")),
                "descripcion_hechos": root.findtext("descripcion_hechos", ""),
                "items": items_list
            }
            return data
        except ET.ParseError as e:
            raise ValueError(f"Error de sintaxis XML: {e}")