from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

_NLP_CONFIG = {"nlp_engine_name": "spacy", "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]}
_analyzer = AnalyzerEngine(nlp_engine=NlpEngineProvider(nlp_configuration=_NLP_CONFIG).create_engine())
_anonymizer = AnonymizerEngine()


def redact(text: str) -> str:
    results = _analyzer.analyze(text=text, language="en")
    return _anonymizer.anonymize(text=text, analyzer_results=results).text


NON_PII_KEYS = {
    "thread_id",
    "image_b64",
    "route",
    "severity",
    "injection_flagged",
    "moderation_violation",
    "case_confirmation",
    "lead_confirmation",
    "escalation_confirmation",
    "case_kb_attempted",
}


def redact_nested(value):
    if isinstance(value, str):
        return redact(value)
    if isinstance(value, dict):
        return {k: (v if k in NON_PII_KEYS else redact_nested(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_nested(v) for v in value]
    return value