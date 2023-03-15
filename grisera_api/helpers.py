def create_stub_from_response(response, id_key = 'id'):
    stub = {id_key: response['id'], 'additional_properties': []}

    for prop in response["properties"]:
        stub['additional_properties'].append({'key': prop['key'], 'value': prop['value']})

    return stub