# GPT Supoorter Backend  

GPT Supporter 프로젝트의 백엔드 폴더입니다.
각 필드별로 CRUD 구현을 중점으로 RestfulAPI를 구현했습니다.

## ERD

![](https://github.com/SonJinHYo/image_repo/blob/main/image_server/Untitled.png?raw=true)

ERD 주소 : https://dbdiagram.io/d/64f40e4c02bd1c4a5edd927d

- User : 유저 객체입니다.django에서 기본으로 제공하는 필드 외에 커스텀 필드로 작성했습니다.
- RefBook, RefData : 유저가 가진 서적, 참고자료를 저장하는 필드입니다.
  - Content : RefData의 본문 내용 필드입니다. 객체 전체(페이지네이션)를 불러올 때 Text필드까지 쿼리하지 않기 위해 따로 필드를 두어 Detail 뷰에서만 볼 수 있도록 했습니다.
- SystemInfo : 유저가 저장한 정보 객체입니다. 필드값을 토대로 ChatGPT에게 사용자의 정보를 최적의 방식으로 전달할 수 있는 스크립트를 제공하도록 만든 모델입니다.
- PublicScript: 관리자 유저가 다루는 공용 스크립트 객체입니다.
  - Script: PublicScript에서 스크립트 필드입니다. 스크립트 순서를 number로 저장합니다.

- 코드의 `Chatrooms.models`,` Dialogues.models`는 사용하진 않았고 구현만 되어있는 부분입니다. 향후 스크립트의 내용이 많아질 경우 사용할 예정입니다.

## 개발환경
- **프로그래밍 언어 및 버전:** Python 3.9
- **통합 개발 환경 (IDE):** Visual Studio Code
- **의존성 관리 도구:** Poetry 및 Pip
- **데이터베이스 관리 시스템:**
  - SQLite (개발 환경)
  - MySQL (배포 환경)
- **웹 프레임워크:** Django
- **기타 필수 소프트웨어 및 도구:**
  - Postman (API 테스트)
  - AWS ECS, ELB, CloudWatch, Docker-compose (컨테이너 관리)
  - Docker (컨테이너화)
  - AWS RDS (관계형 데이터베이스 서비스)

## API명세서
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

자세한 API명세서 정보 : https://documenter.getpostman.com/view/23787123/2s9YBxXaie


## 기술스택

- 프로그래밍 언어 : Python 3.9
- 웹 프레임워크: Django (gunicorn):
  - Django 웹 프레임워크와 gunicorn 웹 서버를 활용하여 API의 핵심 로직과 웹 요청을 처리합니다. Django의 강력한 기능을 통해 안정적인 웹 애플리케이션을 개발할 수 있습니다.
- 데이터베이스: MySQL (AWS RDS)
  - MySQL 데이터베이스는 AWS RDS(Relational Database Service)를 통해 호스팅되며, 데이터 저장 및 관리에 사용됩니다. 안정성과 확장성을 위해 AWS의 관리형 데이터베이스 서비스를 선택하였습니다.
- 보안 및 인증: ACM (AWS Certificate Manager), AFM (AWS Firewall Manager), AWS Shield
  - AWS Certificate Manager를 사용하여 SSL/TLS 인증서를 관리하고, AWS Firewall Manager 및 AWS Shield를 통해 API 보안과 DDoS 공격 방어를 강화하였습니다.
- 클라우드 플랫폼: AWS ECS (Elastic Container Service)
  - AWS ECS를 통해 API 컨테이너화 및 관리를 수행합니다. 
- 버전 관리: Git
  - Git 버전 관리 시스템을 사용하여 API 코드의 버전 관리와 협업을 지원합니다.
- 도구 및 서비스: Docker, Postman, Nginx
  - Docker 컨테이너 기술을 사용하여 개발 환경을 구축 및 배포를 위한 컨테이너를 제공합니다.
  - Postman은 API 테스트 및 문서화를 위해 활용했습니다.
  - Nginx 웹 서버는 API 리버스 프록시 및 부하 분산을 위해 사용됩니다. React 앱의 build파일을 가지고 모든 정적파일을 제공합니다.


