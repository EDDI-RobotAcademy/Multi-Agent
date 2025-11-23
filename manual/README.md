## Hexagonal Architecture 

1. domain  
2. application  
3. adapter  
4. infrastructure  

```
기본적으로 Hexagonal Architecture는 위와 같이 최대 4개의 구성을 가짐
Layered와 마찬가지로 필요 없으면 빼버릴 수 있음
가령 Entity가 필요 없는 소셜 인증의 경우
Google 케이스와 동일하게 domain 패키지가 존재하지 않는 것을 볼 수 있음.
``` 

## domain 패키지

```
Layered에서 Entity의 역할을 하던 녀석이 사실상 domain이라고 보면 됩니다.
그런데 여기서는 또 약간의 차이가 있는데 바로 Spring Boot를 사용하면
JPA를 사용하게 됨으로서 의존성 문제가 발생하게 됩니다.

실제로 Entity는 비즈니스 로직만 제어해야 하는데
웃기게도 JPA를 사용함으로서 Repository와 엮였고 세부사항을 그대로 받아들이게 되었음.

그렇기 때문에 Hexagonal 구조에서는 순수한 비즈니스 목적용 entity를 domain에 배치함
그리고 JPA 혹은 R2DBC (Spring Reactive - Webflux) 와 연결하는 녀석은
infrastructure/orm에서 entity_orm 형태로 다루게 됩니다.
```

## application - usecase(유스케이스)

```
일종의 시나리오라고 보면 됩니다.
그런데 도메인 시나리오라고 볼 수 있습니다.
그리고 usecase는 여러 개 만들 수도 있는데
이 경우 특정 도메인에서 어떤 특정 시나리오에 해당하는 목적을 가집니다.
그렇기 때문에 시나리오가 많으면 usecase도 많을 수 있습니다.
(지금 코드에는 다소 퉁쳐놓긴 했는데 사실 저러면 안되긴 합니다)

비즈니스 룰을 사용하기 위해 노출된 계층 (domain)을 위한 계층
```

## adapter

```
외부 요소들을 usecase와 domain을 위한 데이터로 변환하는 계층
그래서 router의 역할을 담당하고 있음
Layered로 생각하면 controller에 해당함.
다만 adapter를 보면 input/web이 있는데
다른 영역에서도 요청이 올 수 있기 때문에 훨씬 더 복잡한 구성을 가지고 있음

반면 실제 output 영역에 대해서도 생각할 수 있어야 함.
이것은 반대로 우리 측에서 API를 요청하는 상황이 되는데
기존 Layered 구성에서는 이 코드를 작성하기가 상당히 난감했음.
어디에 배치하는 것이 가장 좋을까?
응? api?? 만들고 보니 api에 잔뜩 쌓여서 구별이 안되기 시작하네 ㅠ
위와 같은 상황들이 발생할 수 있다는 점이 있었습니다.

특정 도메인에서 외부 api가 필요하다면 그냥 싹 다 output으로 내보내면 됩니다.
그러니 위의 api 패키지에 싹 다 때려 넣고 고통 받을 일이 없다는 뜻입니다.
```

## infrastructure

```
세부 사항에 대한 것을 전부 제어하고 있음
그렇기 때문에 infrastructure 내부에 orm에 있고
실제 JPA와 R2DBC 요소들은 전부 이 orm 패키지에서 관리됨.
그리고 순수 비즈니스 로직에 해당하는 domain은 세부 사항에 연결되지 않기 때문에
순수하게 데이터 관점에서만 코드를 해석할 수 있다는 이점이 생김.
고로 변경에 더 유연해짐.

비즈니스와 무관한 영역 (세부사항 - 기술 영역)
Redis, Mongo DB, MySQL, Kafka, RabbitMQ, Airflow 등등
어찌 보면 외부 프레임워크라고 봐도 괜찮을 것 같습니다.
```

```
벌집처럼 domain을 중간에두고 참조하는 느낌 <- 정.답
Hexagon(육각형) - 벌집 모양도 육각형 도배
그렇기 때문에 도메인은 그냥 비즈니스 규칙을 정할 뿐
더 이상 infra(기술) 영역과 관계가 없는 순수 데이터가 되었습니다.

도메인을 기준으로 데이터를 주고 받는다고 이해하면 됩니다.
```
