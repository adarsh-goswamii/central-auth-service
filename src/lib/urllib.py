from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class URL:
    @staticmethod
    def strip_query_params(url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    @staticmethod
    def build_redirect_url(redirect_uri: str, params: dict) -> str:
        parsed = urlparse(redirect_uri)
        query = parse_qs(parsed.query)
        query.update(params)
        new_query = urlencode(query, doseq=True)

        return urlunparse(parsed._replace(query=new_query))


url = URL()