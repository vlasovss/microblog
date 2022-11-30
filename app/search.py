from flask import current_app


def add_to_index(index, model):
    if not current_app.es:
        return
    
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    
    current_app.es.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not current_app.es:
        return
    
    current_app.es.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.es:
        return [], 0
    
    resp = current_app.es.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 
                                        'fields': ['*']}},
              'from': (page - 1) * per_page,
              'size': per_page}
    )
    
    ids = [int(hit['_id']) for hit in resp['hits']['hits']]
    
    return ids, resp['hits']['total']['value']