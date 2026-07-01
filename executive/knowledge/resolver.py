def unresolved_links(entities):
    titles = {e.title for e in entities}
    unresolved = []

    for entity in entities:
        for link in entity.links:
            if link not in titles:
                unresolved.append({
                    "source": entity.title,
                    "source_path": entity.path,
                    "missing": link,
                })

    return unresolved
