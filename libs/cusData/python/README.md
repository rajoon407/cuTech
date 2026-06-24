# testouter - cuDataEx 클래스 (XML/JSON 직렬화)

이 프로젝트는 `cuo` 클래스를 상속받은 `cuDataEx` 클래스를 구현하여, 객체를 XML과 JSON 형식으로 직렬화/역직렬화할 수 있는 동적 DLL입니다.

## 주요 기능

1. **cuo 상속**: libcuo의 `cuo` 클래스를 상속받아 구현
2. **데이터 관리**: 키-값 쌍으로 데이터 저장 (string, int, double, bool)
3. **계층 구조**: 자식 노드를 통한 트리 구조 지원
4. **XML 직렬화/역직렬화**: 객체를 XML로 변환하고 XML에서 객체 생성
5. **JSON 직렬화/역직렬화**: 객체를 JSON으로 변환하고 JSON에서 객체 생성
6. **파일 I/O**: XML/JSON 파일 읽기/쓰기 지원

## 프로젝트 구조

```
testouter/
├── cuDataEx.h                    # cuDataEx 클래스 헤더
├── cuDataEx.cpp                  # cuDataEx 클래스 구현
├── cuDataExExport.h              # DLL export 함수 선언
├── cuDataExExport.cpp            # DLL export 함수 구현
├── CMakeLists.txt             # CMake 빌드 설정
├── build.bat                  # Windows 빌드 스크립트
├── build.sh                   # Linux 빌드 스크립트
├── cuDataEx_wrapper.py           # Python 래퍼 모듈
├── test_cuDataEx.py              # Python 테스트 스크립트
└── README.md                  # 이 파일
```

## cuDataEx 클래스 특징

### 데이터 타입
- **String**: 문자열 데이터
- **Int**: 정수 데이터
- **Double**: 실수 데이터
- **Bool**: 불리언 데이터

### 주요 메서드

#### 데이터 설정
- `setString(key, value)`: 문자열 설정
- `setInt(key, value)`: 정수 설정
- `setDouble(key, value)`: 실수 설정
- `setBool(key, value)`: 불리언 설정

#### 데이터 조회
- `getString(key, default)`: 문자열 조회
- `getInt(key, default)`: 정수 조회
- `getDouble(key, default)`: 실수 조회
- `getBool(key, default)`: 불리언 조회

#### 자식 노드 관리
- `addChild(name)`: 자식 노드 추가
- `getChild(index)`: 인덱스로 자식 조회
- `getChildByName(name)`: 이름으로 자식 조회
- `getChildCount()`: 자식 노드 개수
- `removeChild(index)`: 자식 노드 삭제
- `removeAllChildren()`: 모든 자식 노드 삭제

#### XML 직렬화
- `toXml(xmlString)`: XML 문자열로 변환
- `fromXml(xmlString)`: XML 문자열에서 로드
- `fromXmlFile(filePath)`: XML 파일에서 로드
- `saveXmlFile(filePath)`: XML 파일로 저장

#### JSON 직렬화
- `toJson(jsonString)`: JSON 문자열로 변환
- `fromJson(jsonString)`: JSON 문자열에서 로드
- `fromJsonFile(filePath)`: JSON 파일에서 로드
- `saveJsonFile(filePath)`: JSON 파일로 저장

## 빠른 시작

### 1. DLL 빌드

#### Windows
```batch
cd testouter
build.bat
```

#### Linux/Mac
```bash
cd testouter
./build.sh
```

### 2. Python 테스트 실행

```bash
# 전체 테스트 실행
python test_cuDataEx.py
```

## 사용 예제

### Python 기본 사용법

```python
from cuDataEx_wrapper import Cuddd

# 객체 생성
root = Cuddd("person")

# 데이터 설정
root.set_string("name", "홍길동")
root.set_int("age", 30)
root.set_string("job", "의적")
root.set_bool("active", True)

# 데이터 조회
print(f"이름: {root.get_string('name')}")
print(f"나이: {root.get_int('age')}")
print(f"직업: {root.get_string('job')}")
print(f"활성: {root.get_bool('active')}")
```

### 계층 구조 생성

```python
from cuDataEx_wrapper import Cuddd

# 루트 노드
document = Cuddd("document")
document.set_string("title", "나의 문서")

# 자식 노드 추가
chapter1 = document.add_child("chapter")
chapter1.set_string("title", "서론")
chapter1.set_int("page", 1)

chapter2 = document.add_child("chapter")
chapter2.set_string("title", "본론")
chapter2.set_int("page", 10)

# 자식 노드 조회
for i in range(document.get_child_count()):
    child = document.get_child(i)
    print(f"Chapter: {child.get_string('title')}")
```

### XML 직렬화

```python
from cuDataEx_wrapper import Cuddd

# 객체 생성
root = Cuddd("book")
root.set_string("title", "Python 프로그래밍")
root.set_string("author", "김철수")
root.set_int("year", 2024)

# XML로 변환
xml = root.to_xml()
print(xml)

# 파일로 저장
root.save_xml_file("book.xml")

# XML에서 로드
new_root = Cuddd()
new_root.from_xml_file("book.xml")
print(f"제목: {new_root.get_string('title')}")
```

**생성되는 XML 예시:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<book title="Python 프로그래밍" author="김철수" year="2024" />
```

### JSON 직렬화

```python
from cuDataEx_wrapper import Cuddd

# 객체 생성
product = Cuddd("product")
product.set_string("name", "노트북")
product.set_double("price", 1299.99)
product.set_int("stock", 50)

# JSON으로 변환
json = product.to_json()
print(json)

# 파일로 저장
product.save_json_file("product.json")

# JSON에서 로드
new_product = Cuddd()
new_product.from_json_file("product.json")
print(f"상품명: {new_product.get_string('name')}")
```

**생성되는 JSON 예시:**
```json
{
  "_name": "product",
  "_attributes": {
    "name": "노트북",
    "price": "1299.99",
    "stock": "50"
  }
}
```

### 복잡한 구조 예제

```python
from cuDataEx_wrapper import Cuddd

# 도서관 시스템
library = Cuddd("library")
library.set_string("name", "중앙 도서관")
library.set_string("location", "서울")

# 책 1
book1 = library.add_child("book")
book1.set_string("title", "파이썬 프로그래밍")
book1.set_string("author", "김철수")
book1.set_int("year", 2023)
book1.set_double("rating", 4.5)

# 책 2
book2 = library.add_child("book")
book2.set_string("title", "C++ 완벽 가이드")
book2.set_string("author", "이영희")
book2.set_int("year", 2022)
book2.set_double("rating", 4.8)

# XML로 저장
library.save_xml_file("library.xml")

# JSON으로 저장
library.save_json_file("library.json")

print(f"도서관: {library.name}")
print(f"책 수: {library.get_child_count()}")
```

**생성되는 XML:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<library name="중앙 도서관" location="서울">
  <book title="파이썬 프로그래밍" author="김철수" year="2023" rating="4.5" />
  <book title="C++ 완벽 가이드" author="이영희" year="2022" rating="4.8" />
</library>
```

**생성되는 JSON:**
```json
{
  "_name": "library",
  "_attributes": {
    "name": "중앙 도서관",
    "location": "서울"
  },
  "_children": [
    {
      "_name": "book",
      "_attributes": {
        "title": "파이썬 프로그래밍",
        "author": "김철수",
        "year": "2023",
        "rating": "4.5"
      }
    },
    {
      "_name": "book",
      "_attributes": {
        "title": "C++ 완벽 가이드",
        "author": "이영희",
        "year": "2022",
        "rating": "4.8"
      }
    }
  ]
}
```

## DLL Export 함수

다음 C 스타일 함수들이 export되어 Python에서 사용할 수 있습니다:

### 객체 관리
- `cuo_Create()`: 기본 생성자
- `cuo_CreateWithName(name)`: 이름과 함께 생성
- `cuo_Destroy(obj)`: 객체 삭제

### 데이터 설정/조회
- `cuo_SetString(obj, key, value)`
- `cuo_SetInt(obj, key, value)`
- `cuo_SetDouble(obj, key, value)`
- `cuo_SetBool(obj, key, value)`
- `cuo_GetString(obj, key, default)`
- `cuo_GetInt(obj, key, default)`
- `cuo_GetDouble(obj, key, default)`
- `cuo_GetBool(obj, key, default)`

### 자식 노드 관리
- `cuo_AddChild(obj, name)`
- `cuo_GetChild(obj, index)`
- `cuo_GetChildByName(obj, name)`
- `cuo_GetChildCount(obj)`

### XML/JSON
- `cuo_ToXml(obj)`: XML 문자열 생성
- `cuo_ToJson(obj)`: JSON 문자열 생성
- `cuo_FromXml(obj, xmlString)`: XML에서 로드
- `cuo_FromJson(obj, jsonString)`: JSON에서 로드
- `cuo_FromXmlFile(obj, filePath)`: XML 파일에서 로드
- `cuo_FromJsonFile(obj, filePath)`: JSON 파일에서 로드
- `cuo_SaveXmlFile(obj, filePath)`: XML 파일로 저장
- `cuo_SaveJsonFile(obj, filePath)`: JSON 파일로 저장

## 요구 사항

### 빌드 요구사항
- CMake 3.10 이상
- C++17 지원 컴파일러
  - Windows: Visual Studio 2017 이상
  - Linux: GCC 7+ 또는 Clang 5+
- libcuo 라이브러리 (상위 디렉토리에 위치)

### 실행 요구사항
- Python 3.6 이상 (테스트 및 사용)

## 실전 활용 예제

### 설정 파일 관리

```python
from cuDataEx_wrapper import Cuddd

# 설정 생성
config = Cuddd("config")
config.set_string("app_name", "MyApp")
config.set_int("port", 8080)
config.set_bool("debug", True)

# 데이터베이스 설정
db = config.add_child("database")
db.set_string("host", "localhost")
db.set_string("user", "admin")
db.set_int("port", 5432)

# JSON으로 저장
config.save_json_file("config.json")

# 나중에 로드
loaded_config = Cuddd()
loaded_config.from_json_file("config.json")
print(f"Port: {loaded_config.get_int('port')}")
```

### 데이터 교환

```python
# 서버에서 데이터 생성
server_data = Cuddd("response")
server_data.set_int("status", 200)
server_data.set_string("message", "Success")

# JSON으로 직렬화 (네트워크 전송용)
json_str = server_data.to_json()

# 클라이언트에서 수신 후 역직렬화
client_data = Cuddd()
client_data.from_json(json_str)
print(f"Status: {client_data.get_int('status')}")
```

## 문제 해결

### DLL을 찾을 수 없음

**증상:** `FileNotFoundError: cuopy을 찾을 수 없습니다`

**해결:**
1. DLL이 빌드되었는지 확인
2. build.bat 또는 ./build.sh 실행

### 빌드 오류

**증상:** CMake 또는 컴파일 오류

**해결:**
1. libcuo가 먼저 빌드되었는지 확인
2. CMakeLists.txt의 libcuo 경로 확인
3. Visual Studio 버전 확인 (2017 이상)

## 라이선스

이 프로젝트는 libcuo 프로젝트의 일부로, 해당 라이선스를 따릅니다.

