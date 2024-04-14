from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, Field

class Tag(BaseModel):
    id: int

    class Config:
        from_attributes = True

class Banner(BaseModel):
    id: int
    feature_id: str
    tags: List[Tag] = []
    content: Dict[str, Any] = Field(None, description='Содержимое баннера')

    class Config:
        from_attributes = True

class BannerCreate(Banner):
    pass

class BannerUpdate(Banner):
    pass

class User(BaseModel):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class UserBannerGetResponse(BaseModel):
    title: Optional[str] = Field(None, description='Название баннера')
    text: Optional[str] = Field(None, description='Содержание баннера')
    url: Optional[str] = Field(None, description='URL баннера')


class BannerGetResponse(BaseModel):
    banner_id: Optional[int] = Field(None, description='Идентификатор баннера')
    tag_ids: Optional[List[int]] = Field(None, description='Идентификаторы тэгов')
    feature_id: Optional[int] = Field(None, description='Идентификатор фичи')
    content: Optional[Dict[str, Any]] = Field(
        None,
        description='Содержимое баннера',
        example='{"title": "some_title", "text": "some_text", "url": "some_url"}',
    )
    is_active: Optional[bool] = Field(None, description='Флаг активности баннера')
    created_at: Optional[datetime] = Field(None, description='Дата создания баннера')
    updated_at: Optional[datetime] = Field(None, description='Дата обновления баннера')



class BannerPostRequest(BaseModel):
    tag_ids: Optional[List[int]] = Field(None, description='Идентификаторы тэгов')
    feature_id: Optional[int] = Field(None, description='Идентификатор фичи')
    content: Optional[Dict[str, Any]] = Field(
        None,
        description='Содержимое баннера',
        example='{"title": "some_title", "text": "some_text", "url": "some_url"}',
    )
    is_active: Optional[bool] = Field(None, description='Флаг активности баннера')


class BannerPostResponse(BaseModel):
    banner_id: Optional[int] = Field(
        None, description='Идентификатор созданного баннера'
    )

class BannerIdPatchRequest(BaseModel):
    tag_ids: Optional[List[int]] = Field(None, description='Идентификаторы тэгов')
    feature_id: Optional[int] = Field(None, description='Идентификатор фичи')
    content: Optional[Dict[str, Any]] = Field(
        None,
        description='Содержимое баннера',
        example='{"title": "some_title", "text": "some_text", "url": "some_url"}',
    )
    is_active: Optional[bool] = Field(None, description='Флаг активности баннера')


class UserCreate(BaseModel):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class BannerDeleteResponse(BaseModel):
    pass

class BadRequestErrorResponse(BaseModel): # 400
    error: Optional[str] = None


class InternalErrorResponse(BaseModel): # 500
    error: Optional[str] = None

class UnauthorizedErrorResponse(BaseModel): # 401
    error: Optional[str] = None

class ForbiddenErrorResponse(BaseModel): # 403
    error: Optional[str] = None

class NotFoundErrorResponse(BaseModel): # 404
    error: Optional[str] = None

class ValidationErrorResponse(BaseModel): # 422
    error: Optional[str] = None