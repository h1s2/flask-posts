# Flask Posts

Flask와 SQLite를 사용한 간단한 게시판 프로젝트입니다.

## 기술 스택
- Python
- Flask
- SQLite

## 구현 내용
- SQLite 데이터베이스 생성
- posts 테이블 생성
- `/posts` GET, POST API 추가
- `/posts/<int:post_id>` PATCH, DELETE API 추가
- 회원가입, 로그인, 로그아웃 기능 추가

## 실행 방법
```bash
python init_db.py
python app.py
```
