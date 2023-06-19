import pytest
from app import schemas
import json


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    print(posts_list)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    print(res.json())
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/989")
    print(res.json())
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[1].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    print(post)
    assert post.Posts.id == test_posts[1].id
    assert post.Posts.content == test_posts[1].content
    assert post.Posts.title == test_posts[1].title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])

def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.PostResponse(**res.json()[0])
    print(created_post)
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})

    created_post = schemas.PostResponse(**res.json()[0])
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "aasdfjasdf"
    assert created_post.published == True
    assert created_post.user_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    print(res.json())
    assert res.status_code == 401


def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    print(res.json())
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/738")
    print(res.json())
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    print(res.json())
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json()[0])
    print(updated_post)
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    print(res.json())
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/123", json=data)
    print(res.json())
    assert res.status_code == 404