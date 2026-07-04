from executive.knowledge.entity import VaultEntity
from src.knowledge.entity_resolution import (
    build_entity_resolution,
    normalise_name,
    resolve_link_with_index,
)


def test_entity_resolution_canonicalises_company_aliases():
    entities = [
        VaultEntity(id="04 Companies/Microsoft.md", type="company", title="Microsoft", path="04 Companies/Microsoft.md", aliases=[], tags=[], links=[]),
        VaultEntity(id="04 Companies/MSFT.md", type="company", title="MSFT", path="04 Companies/MSFT.md", aliases=["Microsoft Ltd"], tags=[], links=[]),
        VaultEntity(id="04 Companies/Microsoft CSP.md", type="company", title="Microsoft CSP", path="04 Companies/Microsoft CSP.md", aliases=[], tags=[], links=[]),
    ]

    resolution = build_entity_resolution(entities)

    canonical = next(entity for entity in resolution.canonical_entities if entity.canonical_name == "Microsoft")
    assert canonical.entity_type == "company"
    assert "MSFT" in canonical.aliases
    assert "Microsoft Ltd" in canonical.aliases
    assert "Microsoft CSP" in canonical.aliases

    assert resolve_link_with_index("Microsoft Ltd", resolution.index).title == "Microsoft"
    assert resolve_link_with_index("msft", resolution.index).title == "Microsoft"
    assert resolve_link_with_index("microsoft csp", resolution.index).title == "Microsoft"


def test_normalise_name_is_case_and_punctuation_insensitive():
    assert normalise_name("Microsoft Ltd.") == "microsoft"
    assert normalise_name("[[Project-Norman]]") == "project norman"
