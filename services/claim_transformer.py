from models.claim_schema import ReclamacionInsurance
from services.xml_parser import XMLClaimParser
class ClaimTransformerService:
    @staticmethod
    def process_xml_to_ai_json(xml_content: str) -> dict:
        raw_dict = XMLClaimParser.parse_xml_content(xml_content)
        claim_model = ReclamacionInsurance(**raw_dict)
        return claim_model.to_ai_embedding_payload()