import pytest

from app.comments.service import CommentService

@pytest.mark.parametrize("comment_id, creator_id, comment_text, task_id",[
    (1, 2, "string1", 1),
    (2, 2, "string2", 1),
    (3, 3, "string1", 2),
])

async def test_find_comments_by_id(comment_id, creator_id, comment_text, task_id):
    comment = await CommentService.find_by_id(comment_id)

    assert comment.id == comment_id
    assert comment.creator_id == creator_id
    assert comment.comment_text == comment_text
    assert comment.task_id == task_id

async def test_find_comment_by_id_not_found():
    comment = await CommentService.find_by_id(99999)  # id, который точно не существует
    assert comment is None

async def test_find_one_or_none():
    comment = await CommentService.find_one_or_none(id=2)
    assert comment is not None

async def test_find_one_or_none_not_found():
    comment = await CommentService.find_one_or_none(comment_text="99999")  # id, который точно не существует
    assert comment is None

async def test_find_all():
    comment = await CommentService.find_all(comment_text="string1")
    assert len(comment) == 2

async def test_find_all_not_found():
    comment = await CommentService.find_all(comment_text="string1111")
    assert comment == []

@pytest.mark.parametrize("creator_id, comment_text, task_id",[
    (2, "string4", 1),
    (2, "string5", 1),
    (3, "string6", 2),
])
async def test_add_comments(creator_id, comment_text, task_id):
    before = await CommentService.find_all()
    count_before = len(before)

    comment = await CommentService.add(creator_id=creator_id, comment_text=comment_text, task_id=task_id)

    after = await CommentService.find_all()
    count_after = len(after)

    assert count_after == count_before + 1
    assert comment.creator_id == creator_id
    assert comment.comment_text == comment_text
    assert comment.task_id == task_id

@pytest.mark.parametrize("initial_text, new_text", [
    ("old_text", "string_after_change"),
])
async def test_update_by_id(initial_text, new_text):
    comment = await CommentService.add(creator_id=2, comment_text=initial_text, task_id=1)
    comment_id = comment.id

    updated_comment = await CommentService.update_by_id(object_id=comment_id, comment_text=new_text)

    assert updated_comment.comment_text == new_text

async def test_delete_by_id():
    updated_comment = await CommentService.delete_by_id(object_id=1)
    assert updated_comment == True

async def test_delete_by_id_not_found():
    updated_comment = await CommentService.delete_by_id(object_id=99999)
    assert updated_comment == False