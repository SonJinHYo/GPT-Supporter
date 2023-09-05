# GPT Supoorter Backend  

GPT Supporter 프로젝트의 백엔드 디렉터리입니다.
각 필드별로 CRUD 구현을 중점으로 RestfulAPI를 구현했습니다.
<br><br><br>
## ERD

![ERD Diagram](https://github.com/SonJinHYo/image_repo/blob/main/image_server/Untitled.png?raw=true)

[ERD 다이어그램 상세보기](https://dbdiagram.io/d/64f40e4c02bd1c4a5edd927d)

### 주요 모델

- **User**: 유저 객체로, Django에서 기본으로 제공하는 필드 외에도 커스텀 필드로 작성되었습니다.
- **RefBook, RefData**: 유저가 가진 서적 및 참고자료를 저장하는 필드입니다. 특히 `Content` 필드는 RefData의 본문 내용을 저장하며 페이지네이션 등의 요구사항을 고려하여 별도 필드로 구성했습니다.
- **SystemInfo**: 사용자가 저장한 정보를 관리하며, ChatGPT에게 사용자의 정보를 최적의 방식으로 전달하는 스크립트를 제공합니다.
- **PublicScript**: 관리자 유저가 다루는 공용 스크립트 객체로, `Script` 필드에서 스크립트 순서를 `number`로 저장합니다.

<br>

**참고**: `Chatrooms.models` 및 `Dialogues.models` 코드는 현재 사용되지 않지만, 향후 스크립트 내용이 많아질 경우 사용할 예정입니다.

<br><br><br>

## 개발환경
- 운영체제 : ubuntu 22.04
- **프로그래밍 언어 및 버전**: Python 3.9
- **통합 개발 환경 (IDE)**: Visual Studio Code
- **의존성 관리 도구**: Poetry, Pip
- **데이터베이스 관리 시스템**:
  - SQLite (개발 환경)
  - MySQL (배포 환경)
- **웹 프레임워크**: Django 4.2.0
- **기타 필수 소프트웨어 및 도구**:
  - Postman (API 테스트)
  - AWS ECS, ELB, CloudWatch, Docker-compose (컨테이너 관리)
  - Docker (컨테이너화)
  - AWS RDS (관계형 데이터베이스 서비스)

<br><br><br>
## API명세서

자세한 API 명세서는 [이 링크](https://documenter.getpostman.com/view/23787123/2s9YBxXaie)에서 확인할 수 있습니다. 아래는 일부 API 엔드포인트 예시입니다:

| URL                                    | Method      | 기능                              |
| -------------------------------------- | ----------- | --------------------------------- |
| users/signup                           | POST        | 회원가입                          |
| users/signin                           | POST        | 로그인                            |
| users/me                               | GET         | 개인정보 조회 및 로그인 상태 갱신 |
| gpt-sys-infos?page=                    | GET         | ChatGPT 설정 리스트 요청          |
| gpt-sys-infos/create                   | POST        | ChatGPT 설정 생성                 |
| gpt-sys-infos/\<int:pk\>               | PUT, DELETE | 특정 ChatGPT 설정 수정 및 삭제    |
| gpt-sys-infos/refbook?page=            | GET         | 참고서적 리스트 요청              |
| gpt-sys-infos/refbook/create           | POST        | 참고서적 설정 생성                |
| gpt-sys-infos/gpt-sys-infos/\<int:pk\> | PUT, DELETE | 특정 참고서적 설정 수정 및 삭제   |
| gpt-sys-infos/refdata?page=            | GET         | 참조자료 설정 리스트 요청         |
| gpt-sys-infos/refdata                  | POST        | 참조자료 설정 생성                |
| gpt-sys-infos/refdata/\<int:pk\>       | PUT, DELETE | 특정 참조자료 설정 수정 및 삭제   |
| gpt-sys-infos/\<int:pk\>/dialogues     | GET         | 특정 ChatGPT 설정 스크립트 요청   |
| public-script/                         | GET         | 공용 스크립트 생성                |
| public-script/create                   | POST        | ChatGPT 설정 생성                 |



<br><br><br>
## 기술스택
- **프로그래밍 언어** : &nbsp; &nbsp;Python 3.9 <br><br>
- **웹 프레임워크** :&nbsp; &nbsp;Django (gunicorn) 
  - Django 웹 프레임워크와 gunicorn 웹 서버를 활용하여 API의 핵심 로직과 웹 요청을 처리합니다. Django의 강력한 기능을 통해 안정적인 웹 애플리케이션을 개발할 수 있습니다.
  - DRF를 통한 RESTfulAPI 개발 및 ORM 사용 <br><br>
- **데이터베이스** :&nbsp; &nbsp;  MySQL (AWS RDS)
  - MySQL 데이터베이스는 AWS RDS(Relational Database Service)를 통해 호스팅이 됩니다.
  - ECS cluster와 같은 VPC내에서 django와 직접 소통합니다.<br><br>
- **보안 및 인증** :&nbsp; &nbsp; ACM (AWS Certificate Manager), AFM (AWS Firewall Manager), AWS Shield
  - AWS Certificate Manager를 사용하여 SSL/TLS 인증서를 관리합니다.
  - AWS Firewall Manager 및 AWS Shield를 통해 sql문 주입, DDoS 공격 등의 API 보안을 합니다.<br><br>
- **클라우드 플랫폼** :&nbsp; &nbsp;  AWS ECS (Elastic Container Service)
  - AWS ECS를 통해 API 컨테이너화 및 관리를 수행합니다. <br><br>
- **버전 관리** :&nbsp; &nbsp;  Git
  - Git 버전 관리 시스템을 사용하여 API 코드의 버전 관리를 합니다.<br><br>
- **도구 및 서비스** :&nbsp; &nbsp;  Docker, Postman, Nginx
  - Docker 컨테이너 기술을 사용하여 개발 환경을 구축 및 배포를 위한 컨테이너를 제공합니다.
  - Postman은 API 테스트 및 문서화를 위해 활용했습니다.
  - Nginx 웹 서버는 API 리버스 프록시 및 부하 분산을 위해 사용됩니다. React 앱의 build파일을 가지고 모든 정적파일을 제공합니다.
<br><br><br>
## 향후 업데이트 사항.

1. Redis 캐시 서버 적용 (컨테이너 or AWS Redis)
2. 텍스트 데이터 분석 API 개발 - 여러 사용 예제 거들기
3. public-script 유닛테스트 코드 추가
