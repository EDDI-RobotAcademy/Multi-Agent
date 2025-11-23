import os
import requests
from urllib.parse import quote

from social_oauth.adapter.input.web.request.get_access_token_request import GetAccessTokenRequest
from social_oauth.adapter.input.web.response.access_token import AccessToken

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

class GoogleOAuth2Service:

    def get_authorization_url(self) -> str:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = quote(os.getenv("GOOGLE_REDIRECT_URI"), safe='')
        scope = "openid email profile"
        return (
            f"{GOOGLE_AUTH_URL}"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope={quote(scope)}"
        )

    def refresh_access_token(self, request: GetAccessTokenRequest) -> AccessToken:
        data = {
            "code": request.code,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
            "grant_type": "authorization_code"
        }
        resp = requests.post(GOOGLE_TOKEN_URL, data=data)
        resp.raise_for_status()
        token_data = resp.json()
        # Pydantic 모델에 맞춰서 변환
        return AccessToken(
            access_token=token_data.get("access_token"),
            token_type=token_data.get("token_type"),
            expires_in=token_data.get("expires_in"),
            refresh_token=token_data.get("refresh_token")
        )

    def fetch_user_profile(self, access_token: AccessToken) -> dict:
        headers = {"Authorization": f"Bearer {access_token.access_token}"}
        resp = requests.get(GOOGLE_USERINFO_URL, headers=headers)
        resp.raise_for_status()
        return resp.json()
