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






