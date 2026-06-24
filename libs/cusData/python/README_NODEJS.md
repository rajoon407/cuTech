# TestData DLL - Node.js 사용 가이드

이 문서는 TestData DLL을 Node.js에서 사용하는 방법을 설명합니다.

## 목차

1. [설치](#설치)
2. [빠른 시작](#빠른-시작)
3. [API 레퍼런스](#api-레퍼런스)
4. [예제](#예제)
5. [문제 해결](#문제-해결)

## 설치

### 1. Node.js 설치

Node.js 12.0.0 이상이 필요합니다.

- Windows: https://nodejs.org/ 에서 다운로드
- Linux: `sudo apt-get install nodejs npm`
- Mac: `brew install node`

### 2. 의존성 설치

```bash
cd testData
npm install
```

또는

```bash
npm run install-deps
```

설치되는 패키지:
- `ffi-napi`: Node.js에서 C/C++ 라이브러리 호출
- `ref-napi`: C 타입과 JavaScript 간 변환
- `ref-struct-napi`: C 구조체 지원

### 3. DLL 빌드

Node.js 코드를 실행하기 전에 DLL을 먼저 빌드해야 합니다.

```bash
# Windows
build.bat

# Linux/Mac
./build.sh
```

## 빠른 시작

### 기본 사용법

```javascript
const { TestData } = require('./testdata');

// 객체 생성
const data = new TestData(
    '홍길동',
    '조선시대 의적',
    30,
    95.5
);

// 속성 접근
console.log(`이름: ${data.name}`);
console.log(`점수: ${data.score}`);

// 속성 수정
data.value = 35;
data.score = 98.0;

// 출력
console.log(data.toString());

// 메모리 해제 (중요!)
data.destroy();
```

### 테스트 실행

```bash
# 전체 테스트 실행
npm test
# 또는
node test_testdata.js

# 간단한 예제 실행
npm run example
# 또는
node example_node.js
```

## API 레퍼런스

### TestData 클래스

#### 생성자

```javascript
new TestData([name, description, value, score])
```

**매개변수:**
- `name` (string, optional): 이름
- `description` (string, optional): 설명
- `value` (number, optional): 정수 값
- `score` (number, optional): 실수 값

**예제:**
```javascript
// 기본 생성
const td1 = new TestData();

// 전체 데이터로 생성
const td2 = new TestData('이름', '설명', 100, 95.5);

// 일부 데이터만 생성 후 설정
const td3 = new TestData();
td3.name = '이름';
td3.value = 42;
```

#### 속성 (Properties)

##### name
```javascript
data.name  // getter
data.name = '새 이름'  // setter
```
문자열 타입. 데이터의 이름.

##### description
```javascript
data.description  // getter
data.description = '새 설명'  // setter
```
문자열 타입. 데이터의 설명.

##### value
```javascript
data.value  // getter
data.value = 42  // setter
```
정수 타입. 데이터의 정수 값.

##### score
```javascript
data.score  // getter
data.score = 95.5  // setter
```
실수 타입. 데이터의 실수 값.

#### 메서드

##### isEmpty()
```javascript
data.isEmpty()  // => boolean
```
데이터가 비어있는지 확인합니다.

**반환값:** `true` (비어있음) 또는 `false` (데이터 있음)

##### print()
```javascript
data.print()
```
C++ 측에서 데이터를 콘솔에 출력합니다.

##### clear()
```javascript
data.clear()
```
데이터를 초기화합니다.

##### isEqual(other)
```javascript
data.isEqual(otherData)  // => boolean
```
다른 TestData 객체와 비교합니다.

**매개변수:**
- `other` (TestData): 비교할 객체

**반환값:** `true` (같음) 또는 `false` (다름)

##### copy()
```javascript
const newData = data.copy()  // => TestData
```
객체를 복사하여 새로운 객체를 반환합니다.

**반환값:** 복사된 TestData 객체

##### toString()
```javascript
data.toString()  // => string
```
객체의 문자열 표현을 반환합니다.

**반환값:** `"TestData(name='...', description='...', value=..., score=...)"`

##### toJSON()
```javascript
data.toJSON()  // => object
```
객체를 JSON 객체로 변환합니다.

**반환값:**
```javascript
{
    name: '...',
    description: '...',
    value: ...,
    score: ...
}
```

##### destroy()
```javascript
data.destroy()
```
**중요:** 객체를 메모리에서 해제합니다. 사용이 끝난 객체는 반드시 이 메서드를 호출해야 합니다.

### 유틸리티 함수

#### initialize(dllPath)
```javascript
const { initialize } = require('./testdata');
initialize('/custom/path/to/TestDataDLL.dll');
```
커스텀 DLL 경로를 지정합니다. TestData 객체 생성 전에 호출해야 합니다.

## 예제

### 예제 1: 객체 생성 및 속성 접근

```javascript
const { TestData } = require('./testdata');

const person = new TestData('홍길동', '의적', 30, 95.5);

console.log(person.name);        // '홍길동'
console.log(person.description); // '의적'
console.log(person.value);       // 30
console.log(person.score);       // 95.5

person.destroy();
```

### 예제 2: 객체 복사 및 비교

```javascript
const { TestData } = require('./testdata');

const original = new TestData('원본', '설명', 100, 90.0);
const copy = original.copy();

console.log(original.isEqual(copy));  // true

copy.name = '복사본';
console.log(original.isEqual(copy));  // false

original.destroy();
copy.destroy();
```

### 예제 3: 배열 처리

```javascript
const { TestData } = require('./testdata');

const students = [
    new TestData('김철수', '컴공', 20, 92.5),
    new TestData('이영희', '전공', 21, 88.3),
    new TestData('박민수', '기공', 22, 95.7),
];

// 최고 점수 찾기
const best = students.reduce((max, s) => 
    s.score > max.score ? s : max
);
console.log(`최고 점수: ${best.name} (${best.score}점)`);

// 평균 계산
const avg = students.reduce((sum, s) => sum + s.score, 0) / students.length;
console.log(`평균: ${avg.toFixed(2)}점`);

// 메모리 해제
students.forEach(s => s.destroy());
```

### 예제 4: JSON 변환

```javascript
const { TestData } = require('./testdata');

const data = new TestData('테스트', '설명', 42, 95.5);

// JSON으로 변환
const json = data.toJSON();
console.log(JSON.stringify(json, null, 2));

// JSON 파일로 저장
const fs = require('fs');
fs.writeFileSync('data.json', JSON.stringify(json, null, 2));

data.destroy();
```

### 예제 5: 함수형 프로그래밍

```javascript
const { TestData } = require('./testdata');

const data = [
    new TestData('A', 'desc1', 10, 90.0),
    new TestData('B', 'desc2', 20, 85.0),
    new TestData('C', 'desc3', 30, 95.0),
];

// 점수 90점 이상 필터링
const excellent = data.filter(d => d.score >= 90);

// 점수순 정렬
const sorted = [...data].sort((a, b) => b.score - a.score);

// 이름 추출
const names = data.map(d => d.name);

// 메모리 해제
data.forEach(d => d.destroy());
```

### 예제 6: Promise와 비동기 처리

```javascript
const { TestData } = require('./testdata');

async function processData() {
    const data = new TestData('비동기', '테스트', 100, 90.0);
    
    try {
        // 비동기 작업 시뮬레이션
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        console.log(data.toString());
        return data.toJSON();
    } finally {
        // 에러가 발생해도 메모리 해제
        data.destroy();
    }
}

processData().then(json => {
    console.log('완료:', json);
});
```

### 예제 7: 클래스 확장

```javascript
const { TestData } = require('./testdata');

class Student extends TestData {
    constructor(name, major, age, gpa) {
        super(name, major, age, gpa);
    }
    
    get studentName() { return this.name; }
    get major() { return this.description; }
    get age() { return this.value; }
    get gpa() { return this.score; }
    
    isPassing() {
        return this.gpa >= 2.0;
    }
    
    getGrade() {
        const gpa = this.gpa;
        if (gpa >= 4.0) return 'A';
        if (gpa >= 3.0) return 'B';
        if (gpa >= 2.0) return 'C';
        return 'F';
    }
}

const student = new Student('김철수', '컴공', 20, 3.8);
console.log(`${student.studentName}: ${student.getGrade()}학점`);
student.destroy();
```

## 문제 해결

### DLL을 찾을 수 없음

**증상:**
```
Error: TestDataDLL을 찾을 수 없습니다
```

**해결:**
1. DLL이 빌드되었는지 확인
2. DLL 경로를 명시적으로 지정:
   ```javascript
   const { initialize } = require('./testdata');
   initialize('C:/path/to/TestDataDLL.dll');
   ```

### ffi-napi 설치 오류

**증상:**
```
npm ERR! Failed at the ffi-napi install script
```

**해결:**
1. Windows: Visual Studio Build Tools 설치
   - https://visualstudio.microsoft.com/downloads/
   - "C++를 사용한 데스크톱 개발" 워크로드 선택
2. Python 2.7 또는 3.x 설치 (node-gyp용)
3. 재시도: `npm install`

### 메모리 누수

**증상:** 프로그램이 오래 실행되면 메모리 사용량이 계속 증가

**해결:**
반드시 `destroy()` 메서드를 호출하세요:

```javascript
// 좋은 예
function processData() {
    const data = new TestData();
    try {
        // ... 작업 ...
    } finally {
        data.destroy();  // 항상 호출됨
    }
}

// 나쁜 예
function processData() {
    const data = new TestData();
    // ... 작업 ...
    // destroy() 호출 안 함 - 메모리 누수!
}
```

### 32bit/64bit 불일치

**증상:**
```
Error: Dynamic Linking Error: Win32 error 193
```

**해결:**
- Node.js와 DLL의 아키텍처가 일치해야 함
- Node.js 아키텍처 확인: `node -p "process.arch"`
- 64bit Node.js에는 64bit DLL 필요

### Linux에서 libcuo.so를 찾을 수 없음

**증상:**
```
Error: libcuo.so: cannot open shared object file
```

**해결:**
```bash
export LD_LIBRARY_PATH=/path/to/libcuo:$LD_LIBRARY_PATH
# 또는
sudo ldconfig /path/to/libcuo
```

## 모범 사례

### 1. 항상 메모리 해제

```javascript
const data = new TestData();
try {
    // 작업 수행
} finally {
    data.destroy();  // 항상 호출
}
```

### 2. 배열 처리 시 일괄 해제

```javascript
const dataArray = [
    new TestData('A', 'desc1', 1, 1.0),
    new TestData('B', 'desc2', 2, 2.0),
];

try {
    // 배열 처리
} finally {
    dataArray.forEach(d => d.destroy());
}
```

### 3. 에러 처리

```javascript
let data = null;
try {
    data = new TestData();
    // 작업 수행
} catch (error) {
    console.error('오류:', error);
} finally {
    if (data) data.destroy();
}
```

### 4. 타입 체크

```javascript
function processData(data) {
    if (!(data instanceof TestData)) {
        throw new TypeError('TestData 객체가 필요합니다');
    }
    // 처리
}
```

## 추가 리소스

- [Python 예제](test_testdata.py)
- [빌드 가이드](BUILD.md)
- [프로젝트 README](README.md)

## 라이선스

이 프로젝트는 libcuo 프로젝트의 일부로, 해당 라이선스를 따릅니다.

