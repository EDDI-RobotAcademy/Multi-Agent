import json
from fastapi import HTTPException, Cookie
from social_oauth.adapter.input.web.google_oauth2_router import redis_client  # 이미 redis_client 존재한다고 가정

def get_current_user(session_id: str = Cookie(None)) -> int:
    if not session_id:
        raise HTTPException(status_code=401, detail="세션이 존재하지 않습니다.")

    redis_key = f"session:{session_id}"
    user_data_bytes = redis_client.get(redis_key)
    if not user_data_bytes:
        raise HTTPException(status_code=401, detail="세션이 유효하지 않습니다.")

    # bytes -> str -> dict
    if isinstance(user_data_bytes, bytes):
        user_data_str = user_data_bytes.decode("utf-8")
    else:
        user_data_str = str(user_data_bytes)

    try:
        user_data = json.loads(user_data_str)
        user_id = int(user_data["user_id"])
    except (KeyError, ValueError, json.JSONDecodeError):
        raise HTTPException(status_code=401, detail="세션 데이터가 올바르지 않습니다.")

    return user_id
