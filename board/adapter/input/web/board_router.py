from fastapi import APIRouter, Depends, Request, Response, Cookie, HTTPException, Query, Body
from fastapi.responses import JSONResponse

from account.adapter.input.web.session_helper import get_current_user
from account.application.usecase.account_usecase import AccountUseCase
from account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl
from board.adapter.input.web.request.create_board_request import CreateBoardRequest
from board.adapter.input.web.request.update_board_request import UpdateBoardRequest
from board.adapter.input.web.response.board_list_response import BoardListResponse
from board.application.usecase.board_usecase import BoardUsecase
from board.infrastructure.repository.board_repository_impl import BoardRepositoryImpl

board_router = APIRouter(tags=["board"])
board_repository_impl = BoardRepositoryImpl()
board_usecase = BoardUsecase(board_repository_impl)

account_repository_impl = AccountRepositoryImpl()
account_usecase = AccountUseCase(account_repository_impl)

# 세션으로 사용자 확인
from fastapi import HTTPException

# 게시글 생성
@board_router.post("/create")
async def create_board(
    request_data: CreateBoardRequest,
    user_id: str = Depends(get_current_user)
):
    # 게시글 생성
    board = board_usecase.create_board(
        title=request_data.title,
        content=request_data.content,
        author_id=user_id
    )

    # 작성자 nickname 가져오기
    account = account_usecase.get_account_by_id(user_id)
    nickname = account.nickname if account else "anonymous"

    return JSONResponse({
        "id": board.id,
        "title": board.title,
        "author": nickname,
        "created_at": board.created_at.isoformat(),
    })

# 게시글 단건 조회
@board_router.get("/read/{board_id}")
async def get_board(board_id: int):
    board = board_usecase.get_board(board_id)
    return JSONResponse({"id": board.id, "title": board.title, "content": board.content, "author_id": board.author_id})

# 게시글 수정
@board_router.put("/update/{board_id}")
async def update_board(
        board_id: int,
        request: UpdateBoardRequest = Body(...),
        user_id: str = Depends(get_current_user)):

    board = board_usecase.get_board(board_id)
    if board.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    updated_board = board_usecase.update_board(board_id, request.title, request.content)
    return JSONResponse({"id": updated_board.id, "title": updated_board.title, "content": updated_board.content})

# 내가 쓴 게시글 전체 조회
@board_router.get("/me")
async def get_my_boards(user_id: str = Depends(get_current_user)):
    boards = board_usecase.get_boards_by_author(user_id)
    return JSONResponse([{"id": b.id, "title": b.title, "content": b.content} for b in boards])

# 게시글 리스트
@board_router.get("/list", response_model=BoardListResponse)
async def list_boards(page: int = Query(1, ge=1), size: int = Query(10, ge=1)):
    boards, total = board_usecase.get_all_boards(page, size)

    author_ids = [b.author_id for b in boards]
    authors = account_usecase.get_accounts_by_ids(author_ids)  # {id: Account}
    nicknames = {a.id: a.nickname for a in authors}

    return BoardListResponse.from_boards(boards, nicknames, page, size, total=total)

# 게시글 삭제
@board_router.delete("/delete/{board_id}")
async def delete_board(board_id: int, user_id: str = Depends(get_current_user)):
    board = board_usecase.get_board(board_id)
    if board.author_id != user_id:
        return JSONResponse({"error": "Not allowed"}, status_code=403)
    board_usecase.delete_board(board_id)
    return JSONResponse({"result": "deleted"})
