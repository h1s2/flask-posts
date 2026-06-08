# Flask Posts

Flask와 SQLite를 사용한 간단한 게시판 프로젝트입니다.

## 기술 스택

- Python
- Flask
- SQLite

## 구현 내용

### 게시글 기능

- SQLite 데이터베이스 생성
- posts 테이블 생성
- `/posts` GET, POST API 추가
- `/posts/<int:post_id>` PATCH, DELETE API 추가
- 게시글 목록 조회
- 게시글 생성
- 게시글 수정
- 게시글 삭제

### 회원 기능

- users 테이블 생성
- 회원가입
- 로그인
- 로그아웃
- 세션 기반 인증
- 로그인 상태 확인 (`/me`)

### 권한 기능

- 게시글 작성 시 작성자(user_id) 저장
- 로그인한 사용자만 게시글 작성 가능
- 작성자만 게시글 수정 가능
- 작성자만 게시글 삭제 가능

## 실행 방법

```bash
python init_db.py
python app.py
```