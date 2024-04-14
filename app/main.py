from typing import List, Optional, Union
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, Response, status, BackgroundTasks

from . import crud, models, schemas
from .database import SessionLocal, engine

from app.schemas import (
    BannerGetResponse,
    BannerIdPatchRequest,
    BannerPostRequest,
    BannerPostResponse,
    UserBannerGetResponse,
    BadRequestErrorResponse,
    InternalErrorResponse,
    UnauthorizedErrorResponse,
    ForbiddenErrorResponse,
    NotFoundErrorResponse,
    ValidationErrorResponse,
)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Сервис баннеров',
    version='1.0.0',
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def commit_db(db: Session):
    crud.commit_db(db)

@app.get(
    '/banner',
    response_model=List[BannerGetResponse],
    responses={
        '500': {'model': InternalErrorResponse},
        '401': {'description': 'Пользователь не авторизован'},
        '403': {'description': 'Пользователь не имеет доступа'},
    },
)
async def get_banner(
    token: int,
    feature_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    db: Session = Depends(get_db)
) -> Union[List[BannerGetResponse], InternalErrorResponse]:
    """
    Получение всех баннеров c фильтрацией по фиче и/или тегу
    """
    if crud.is_user_admin(db, token):
        banners = crud.get_banners(
            db=db,
            banner_feature_id=feature_id,
            banner_tag_id=tag_id,
            limit=limit,
            offset=offset,
        )
        return [BannerGetResponse(
            banner_id=banner.id,
            feature_id=banner.feature_id,
            tag_ids=[tag.id for tag in banner.tags],
            content=banner.content,
            is_active=banner.is_active,
            created_at=banner.created_at,
            updated_at=banner.updated_at
        ) for banner in banners]
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app.post(
    '/banner',
    response_model=None,
    responses={
        '201': {'model': BannerPostResponse},
        '400': {'model': NotFoundErrorResponse,
                'description': 'Некорректные данные'},
        '401': {'description': 'Пользователь не авторизован'},
        '403': {'description': 'Пользователь не имеет доступа'},
        '500': {'model': InternalErrorResponse,
                'description': 'Внутренняя ошибка сервера'},
    },
)
async def post_banner(
    token: int, 
    body: BannerPostRequest,
    db: Session = Depends(get_db),
    
) -> Union[None, BannerPostResponse, NotFoundErrorResponse, InternalErrorResponse,
           UnauthorizedErrorResponse]:
    """
    Создание нового баннера
    """
    if crud.is_user_admin(db, token):
        banner = crud.create_banner(db=db, banner=body)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=BannerPostResponse(banner_id=banner.id).model_dump())
    else:
        return UnauthorizedErrorResponse(error='Пользователь не авторизован')


@app.patch(
    '/banner/{id}',
    response_model=None,
    responses={
        '400': {'model': BadRequestErrorResponse},
        '401': {'description': 'Пользователь не авторизован'},
        '403': {'description': 'Пользователь не имеет доступа'},
        '404': {'description': 'Баннер не найден'},
        '500': {'model': InternalErrorResponse,
                'description': 'Внутренняя ошибка сервера'},
    },
)
async def patch_banner_id(
    background_tasks: BackgroundTasks,
    id: int,
    token: int, 
    body: BannerIdPatchRequest,
    db: Session = Depends(get_db)
) -> Union[None, BadRequestErrorResponse, InternalErrorResponse]:
    """
    Обновление содержимого баннера
    """
    if crud.is_user_admin(db, token):
        count = crud.update_banner(db, id, body)
        background_tasks.add_task(crud.commit_db, db)
        if count > 0:
            return Response(status_code=status.HTTP_200_OK)
        else:
            return NotFoundErrorResponse(error='Баннер не найден')


@app.delete(
    '/banner/{id}',
    response_model=None,
    responses={
        '401': {'description': 'Пользователь не авторизован'},
        '403': {'description': 'Пользователь не имеет доступа'},
        '404': {'description': 'Баннер для тэга не найден'},
        '400': {'model': BadRequestErrorResponse},
        '500': {'model': InternalErrorResponse,
                'description': 'Внутренняя ошибка сервера'},
        '204': {'description': 'Баннер успешно удален'},
    },
)
async def delete_banner_id(
    id: int, 
    token: int,
    db: Session = Depends(get_db)
) -> Union[ForbiddenErrorResponse, InternalErrorResponse]:
    """
    Удаление баннера по идентификатору
    """
    try:
        if crud.is_user_admin(db, token):
            count = crud.delete_banner(db, id)
            if count > 0:
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return ForbiddenErrorResponse(error='Пользователь не имеет доступа')
    except:
        return InternalErrorResponse(error='Произошла ошибка при удалении баннера')



@app.get(
    '/user_banner',
    response_model=UserBannerGetResponse,
    responses={
        '400': {'model': ForbiddenErrorResponse},
        '500': {'model': InternalErrorResponse},
    },
)
async def get_user_banner(
    tag_id: int,
    feature_id: int,
    token: int,
    use_last_revision: Optional[bool] = False,
    db: Session = Depends(get_db)
) -> Union[BannerGetResponse, ForbiddenErrorResponse, InternalErrorResponse]:
    """
    Получение баннера для пользователя
    """
    if use_last_revision:
        crud.commit_db(db)
    banner = crud.get_user_banner(
        db=db,
        feature_id=feature_id,
        tag_id=tag_id,
    )
    if not banner:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return UserBannerGetResponse(
        title=banner.content['title'],
        text=banner.content['text'],
        url=banner.content['url']
    )

@app.post('/add_user')
async def add_user(
    is_admin: bool,
    db: Session = Depends(get_db)):
    return crud.create_user(db=db, is_admin=is_admin)