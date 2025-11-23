from account.application.port.account_repository_port import AccountRepositoryPort
from account.domain.account import Account
from social_oauth.infrastructure.service.google_oauth2_service import GoogleOAuth2Service, GetAccessTokenRequest, \
    AccessToken


class GoogleOAuth2UseCase:
    def __init__(self, service: GoogleOAuth2Service):
        self.service = service

    def get_authorization_url(self) -> str:
        return self.service.get_authorization_url()

    def login_and_fetch_user(self, state: str, code: str) -> AccessToken:
        # 코드 -> 액세스 토큰
        token_request = GetAccessTokenRequest(state=state, code=code)
        access_token = self.service.refresh_access_token(token_request)

        # 액세스 토큰으로 사용자 프로필 가져오기
        user_profile = self.service.fetch_user_profile(access_token)
        email = user_profile.get("email")
        nickname = user_profile.get("nickname")

        # Account 자동 생성/조회
        account = self.account_repository.find_by_email(email)
        if not account:
            if not nickname:
                # nickname 없으면 anonymous{n} 형태
                nickname = f"anonymous{self.account_repository.count() + 1}"
            account = Account(email=email, nickname=nickname)
            self.account_repository.save(account)

        # AccessToken 반환 (DB 처리 완료 후)
        return access_token

    def fetch_user_profile(self, code: str, state: str) -> dict:
        token_request = GetAccessTokenRequest(state=state, code=code)
        access_token = self.service.refresh_access_token(token_request)

        profile = self.service.fetch_user_profile(access_token)
        return {"profile": profile, "access_token": access_token}
