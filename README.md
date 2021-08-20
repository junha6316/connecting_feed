
# Connecting_feed

DRF 사용해서 커넥팅 피드 API 구현

## 진행사항
#### 2021.08.18

- [X] Write ERD   
- [X] Write models

#### 3



### To Do List

#### 1. feeds
- [X] Create Feed
- [X] Detail Feed
- [X] List Feeds 
    - [X] lastest  ?catergory=latest
    - [X] popular  ?catergory=popular
    - [X] myfeed   ?catergory=myfeed

#### 2. users
- [X] GET my activity status /feed_status

#### 3. comments
- [ ] Create Comment 

#### 4. replies
- [ ] Create Reply 

#### 5. likes
- [ ] Create Likes 
    - [ ] feed Likes /feed
    - [ ] comment Likes /comment
    - [ ] reply Likes /reply

- [ ] Delete Likes 
    - [ ] feed Likes /feed
    - [ ] comment Likes /comment
    - [ ] reply Likes /reply



## Database 관련

### ERD
* 아래 링크를 통해 확인하실 수 있습니다.
* https://aquerytool.com/aquerymain/index/?rurl=7cdf5193-ef9d-4bda-9c60-01c3a458b134
* password : 3y2w1a

### 데이터베이스 쿼리 최적화
- Locust로 실험하면서 진행
1. Eager-Loading
2. Connection Pool
3. Cache(Redis)
4. Indexing
5. http Keep alive
