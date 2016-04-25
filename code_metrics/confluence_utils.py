import os
import requests


class ConfluenceSpace(object):

    def __init__(self, url, username, password, space_key):
        self.url = url
        self.space_key = space_key
        self.session = requests.Session()
        self.session.auth = (username, password)

    @classmethod
    def from_environment(cls):
        server = os.environ.get("CONFLUENCE_URL")
        user = os.environ.get("CONFLUENCE_USER")
        passwd = os.environ.get("CONFLUENCE_PASSWORD")
        space_name = os.environ.get("CONFLUENCE_SPACE")
        if not server:
            raise RuntimeError("CONFLUENCE server URL required. Set env var CONFLUENCE_URL")
        if not user:
            raise RuntimeError("CONFLUENCE username required. Set env var CONFLUENCE_USER")
        if not passwd:
            raise RuntimeError("CONFLUENCE password required. Set env var CONFLUENCE_PASSWORD")
        if not space_name:
            raise RuntimeError("CONFLUENCE space name required. Set env var CONFLUENCE_SPACE")

        return cls(server, user, passwd, space_name)

    def __str__(self):
        return "{} - {}".format(self.url, self.space_key)

    def get_page_id(self, title):
        response = self.session.get(self.url, params={
            'spaceKey': self.space_key, 'title': title
        })
        results = response.json().get('results', None)
        if not results:
            return None
        assert len(results) == 1, "multiple pages found for title {}".format(title)
        return results[0]['id']

    def create_page(self, title, parent_id=None):
        data = {
            'title': title,
            'type': 'page',
            'space': {'key': self.space_key}
        }
        if parent_id:
            data['ancestors'] = [{"id": parent_id}]
        response = self.session.post(self.url, json=data)
        return response.json()['id']

    def get_page_content(self, page_id):
        page_url = "{}/{}".format(self.url, page_id)
        response = self.session.get(page_url, params={'expand': 'body.storage'})
        return response.json()['body']['storage']['value']

    def set_page_content(self, page_id, content):
        page_url = "{}/{}".format(self.url, page_id)
        response = self.session.get(page_url, params={'expand': 'version'})
        page_data = response.json()
        page_version = page_data['version']['number']
        title = page_data['title']
        response = self.session.put(page_url, json={
            'type': 'page',
            'title': title,
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage',
                }
            },
            'version': {
                'number': page_version + 1,
            }
        })
        assert response.status_code == requests.codes.OK, ( # pylint: disable=no-member
            "Cannot update page content: {}".format(response.reason)
        )
        return response.json()
