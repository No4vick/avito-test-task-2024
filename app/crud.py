from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from . import schemas, models

def get_or_create_tag(db: Session, tag_id):
    try:
        tag = db.query(models.Tag).filter(models.Tag.id == tag_id).one()
        return tag, False
    except NoResultFound:
        new_tag = models.Tag(id=tag_id)
        db.add(new_tag)
        db.commit()
        return new_tag, True

def get_or_create_banner_tags(db: Session, banner_id, tag_ids: list[int]):
    new_pairs = []
    for tag_id in tag_ids:
        try:
            pair = db.query(models.banner_tags).filter(models.banner_tags.tag_id == tag_id,
                                                       models.banner_tags.banner_id == banner_id).one()
        except NoResultFound:
            pair = models.banner_tags(banner_id=banner_id, tag_id=tag_id)
            new_pairs.append(pair)
            
    if new_pairs:
        db.bulk_save_objects(new_pairs)
        db.commit()
        
    return new_pairs

def get_banner_by_id(db: Session, banner_id: int):
    return db.query(models.Banner).filter(models.Banner.id == banner_id).first()

def get_banners(db: Session, banner_feature_id: int = None, banner_tag_id: int = None, limit: int = None, offset: int = None):
    if banner_feature_id and banner_tag_id:
        return db.query(models.Banner).filter(
                models.Banner.feature_id == banner_feature_id,
                models.Banner.tags.any(models.Tag.id == banner_tag_id)
                ).offset(offset).limit(limit).all()
    elif not banner_feature_id and banner_tag_id:
        return db.query(models.Banner).filter(
                models.Banner.tags.any(models.Tag.id == banner_tag_id)
                ).offset(offset).limit(limit).all()
    elif banner_feature_id and not banner_tag_id:
        return db.query(models.Banner).filter(
                models.Banner.feature_id == banner_feature_id
                ).offset(offset).limit(limit).all()
    else:
        return db.query(models.Banner).offset(offset).limit(limit).all()

def create_banner(db: Session, banner: schemas.BannerCreate):
    tags = [get_or_create_tag(db, tag_id)[0] for tag_id in banner.tag_ids]
    db_banner = models.Banner(feature_id=banner.feature_id, 
                              tags=tags,
                              content=banner.content, 
                              is_active=banner.is_active)
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return db_banner

def update_banner(db: Session, banner_id: int, banner: schemas.BannerUpdate):
    # initial_count = db.query(models.banner_tags).filter_by(banner_id=banner_id).count()
    banner_dict = banner.model_dump(exclude_unset=True)
    updated = False
    if banner_dict.get('tag_ids'):
        tags = [get_or_create_tag(db, tag_id)[0] for tag_id in banner.tag_ids]
        db_banner = db.query(models.Banner).filter_by(id=banner_id).first()
        if not db_banner:
            return False
        updated = True
        db_banner.tags = tags
        del banner_dict['tag_ids']
    banner_dict['updated_at'] = datetime.now()
    updated = db.query(models.Banner).filter_by(id=banner_id).update(banner_dict) > 0 or updated
    db.commit()
    return updated
def delete_banner(db: Session, banner_id: int):
    db.query(models.banner_tags).filter(models.Banner.id == banner_id).delete()
    count = db.query(models.Banner).filter(models.Banner.id == banner_id).delete()
    db.commit()
    return count

def is_user_admin(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first().is_admin

def get_user_banner(db: Session, feature_id: int, tag_id: int):
    banner = (
        db.query(models.Banner.content, models.Banner.feature_id, models.banner_tags.c.tag_id)
            .join(models.banner_tags, models.Banner.id == models.banner_tags.c.banner_id)
            .filter(models.Banner.feature_id == feature_id, models.banner_tags.c.tag_id == tag_id)
            .first()
        ) 
    return banner
def create_user(db: Session, is_admin: bool):
    db_user = models.User(is_admin=is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def commit_db(db: Session):
    print("COM!")
    db.commit()