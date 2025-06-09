import requests
class MediaWikiSession(requests.Session):
    def __init__(self, access_token: str, mediawiki_api_url: str):
        super().__init__()
        self.access_token = access_token
        self.mediawiki_api_url = mediawiki_api_url

        # Apply OAuth bearer headers to all requests
        self.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        })

    @property
    def edit_token(self) -> str:
        params = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }
        resp = self.get(self.mediawiki_api_url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data['query']['tokens']['csrftoken']

    @staticmethod
    def from_yaml(config_file: str) -> 'MediaWikiSession':
        import yaml
        with open(config_file) as f:
            cfg = yaml.safe_load(f)
        mw = cfg['mediawiki']
        url = mw['url']
        with open(mw['access token']) as f:
            token = f.read().strip()
        return WikimediaSession(token, url)
