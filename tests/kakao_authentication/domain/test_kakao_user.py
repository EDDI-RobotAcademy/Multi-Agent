import pytest
from kakao_authentication.domain.value_objects.kakao_email import KakaoEmail
from kakao_authentication.domain.value_objects.kakao_nickname import KakaoNickname
from kakao_authentication.domain.value_objects.kakao_user_id import KakaoUserId
from kakao_authentication.domain.kakao_user import KakaoUser

# TDD (Test Driven Development/Design)
# 먼저 실패하는 테스트 케이스를 작성합니다.
# 우리가 만들고자하는 백로그(제목) -> DDD (Domain Driven Design)
# TDD -> DDD -> 도메인 정리가 굉장히 깔끔하게 떨어집니다.
# boardUsecase <- 이런 것을 만들 것이다라는 명시
# createdBoard = boardUsecase.create(title, content, writer);
# createdBoard에 title, content, writer가 우리가 입력한 값이 잘 들어갔는지 확인
# assert(title, content, writer) 일치 여부 확인
# 자연스럽게 Usecase(유스케이스) 레벨에서 백로그가 작성되게 되어 있음
# 그러므로 도메인 정합성이 깨지거나 요상한 내용이 다른 도메인으로 통합되는 상황을 피할 수 있음

# 예로 Order를 만든다 가정
# orderUsecase
# accountUsecase
# cartUsecase
# bookUsecase
# 실패하는 테스트 케이스를 작성함으로서 자연스럽게 도메인 분리를 달성하게 됨.
# 결국 TDD를 자연스럽게 DDD가 가능해진다.
# 결론적으로 TDD 없는 DDD는 불가능하다 <- 핵심 메시지

# 정상 생성
def test_kakao_user_creation():
    user_id = KakaoUserId(1)
    email = KakaoEmail("test@example.com")
    nickname = KakaoNickname("nickname")

    user = KakaoUser(user_id=user_id, email=email, nickname=nickname)

    assert user.user_id.value == 1
    assert user.email.value == "test@example.com"
    assert user.nickname.value == "nickname"


# 잘못된 이메일 입력 시 ValueError 발생
def test_kakao_user_invalid_email():
    user_id = KakaoUserId(1)
    with pytest.raises(ValueError):
        email = KakaoEmail("invalid-email")
        nickname = KakaoNickname("nickname")
        KakaoUser(user_id=user_id, email=email, nickname=nickname)


# 잘못된 닉네임 입력 시 ValueError 발생
def test_kakao_user_invalid_nickname():
    user_id = KakaoUserId(1)
    email = KakaoEmail("test@example.com")
    with pytest.raises(ValueError):
        nickname = KakaoNickname("")  # 빈 문자열
        KakaoUser(user_id=user_id, email=email, nickname=nickname)


# 잘못된 사용자 ID 입력 시 ValueError 발생
def test_kakao_user_invalid_user_id():
    email = KakaoEmail("test@example.com")
    nickname = KakaoNickname("nickname")
    with pytest.raises(ValueError):
        user_id = KakaoUserId(0)
        KakaoUser(user_id=user_id, email=email, nickname=nickname)
