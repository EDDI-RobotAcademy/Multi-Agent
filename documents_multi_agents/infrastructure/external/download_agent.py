import os
import hashlib
import aiohttp

# 캐시 디렉토리 경로 설정
CACHE_DIR = "./cache"
os.makedirs(CACHE_DIR, exist_ok=True)  # 디렉토리 자동 생성

async def download_document(doc_url: str) -> bytes:
    """
    주어진 URL에서 PDF를 다운로드하고 캐시된 파일 경로를 반환
    """
    cache_path = get_cache_filename(doc_url)

    # 이미 캐시에 존재하면 바로 읽어서 반환
    if os.path.exists(cache_path):
        print(f"[DEBUG] 캐시에서 로드: {cache_path}")
        with open(cache_path, "rb") as f:
            return f.read()

    # 없으면 다운로드
    print(f"[DEBUG] 다운로드 시작: {doc_url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(doc_url) as resp:
            if resp.status != 200:
                raise Exception(f"다운로드 실패: {resp.status}")
            content = await resp.read()

    # 다운로드 후 캐시에 저장
    with open(cache_path, "wb") as f:
        f.write(content)
    print(f"[DEBUG] 다운로드 완료 및 캐시 저장: {cache_path} ({len(content)} bytes)")
    return content

def get_cache_filename(doc_url: str) -> str:
    """
    doc_url을 해싱하여 고유 캐시 파일 이름 생성
    """
    file_hash = hashlib.sha256(doc_url.encode()).hexdigest()
    file_path = os.path.join(CACHE_DIR, f"{file_hash}.pdf")

    # 디렉토리 존재 확인
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path
