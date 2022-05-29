from typing import List, Optional

from fastapi import Depends, exceptions, status

from .. import models
from LightServer.database.database import get_session
from ..database import orm


class TagsService:

    def __init__(self, session=Depends(get_session)):
        self._session = session

    def create_tag(self, tag: models.TagCreate) -> orm.Tag:
        new_tag = orm.Tag(title=tag.name)

        self._session.query.add(new_tag)
        self._session.commit()
        return new_tag

    def _get_relations_by_post_query(self, post: orm.Post):
        return (
            self._session
                .query(orm.PostTag)
                .filter(orm.PostTag.post_id == post.id)
        )

    def _get_relations_by_tag_query(self, tag: orm.Tag):
        return (
            self._session
                .query(orm.PostTag)
                .filter(orm.PostTag.tag_id == tag.id)
        )

    def _get_relation(self,  tag: orm.Tag, post: orm.Post) -> orm.PostTag:
        relation = (
            self._get_relations_by_post_query(post)
                .filter(orm.PostTag.tag_id == tag.id)
                .first()
        )

        return relation

    def add_tag_to_post(self, tag: orm.Tag, post: orm.Post) -> orm.PostTag:
        relation = self._get_relation(tag, post)
        if not relation:
            relation = orm.PostTag(tag_id=tag.id, post_id=post.id)

        self._session.add(relation)
        self._session.commit()

        return relation

    def remove_tag_from_post(self, tag: orm.Tag, post: orm.Post):
        relation = self._get_relation(tag, post)
        if not relation:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this post have no this tag")

        self._session.delete(relation)
        self._session.commit()

    def get_post_tags_list(self, post: orm.Post) -> List[orm.Tag]:
        relations: List[orm.PostTag] = self._get_relations_by_post_query(post).all()

        return [item.tag for item in relations]

    def get_tag(self, item: models.TagCreate) -> orm.Tag:
        tag = (
            self._session
                .query(orm.Tag)
                .filter(orm.Tag.name == item.name)
                .first()
        )
        if not tag:
            tag = orm.Tag(name=item.name)
            self._session.add(tag)
            self._session.commit()

        return tag

    def add_tags_to_post(self, post: orm.Post, tags: List[models.TagCreate]) -> List[orm.PostTag]:
        tags = [self.get_tag(tag) for tag in tags]
        relations = list(map(self.add_tag_to_post, tags, [post] * len(tags)))

        return relations

