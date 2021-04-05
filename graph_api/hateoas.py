

def get_links(router):
    """
        Return list of links from given router

        Args:
            router (Router): Router to get links from

        Returns:
            List of links
        """
    links_json = []
    links = [[route.name, route.path, route.methods] for route in router.routes]

    for link in links:
        for method in link[2]:
            links_json.append({'rel': link[0], '$ref': link[1], 'action': method})

    return links_json
