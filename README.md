
# Connecting_feed

커넥팅 피드 API 구현(Django Rest Framework)

## Stack
- Python 3.9.6
- Django 3.2.6
- DRF 3.12.4
- mysql 8.0.26


## To Do List
#### 1. feeds
- [X] Create Feed
- [X] Detail Feed
- [X] List Feeds 
    - [X] lastest  /latest
    - [X] popular  /popular
    - [X] myfeed   /myfeed
- [X] List RelatedComment /<int:pk>/comments

#### 2. users
- [X] GET my activity status /feed_status

#### 3. comments
- [X] Create Comment 

#### 4. likes
- [X] Create Likes 
    - [X] FeedLike /feed
    - [X] CommentLike /comment

- [X] Delete Likes 
    - [X] FeedLike  /feed
    - [X] CommentLike /comment

## Database 관련

### ERD
* 아래 링크를 통해 확인하실 수 있습니다.
* https://aquerytool.com/aquerymain/index/?rurl=7cdf5193-ef9d-4bda-9c60-01c3a458b134
* password : 3y2w1a

### 데이터베이스 쿼리 최적화
- [X] Eager-Loading
- [X] Indexing
- [X] Cache(Redis)
