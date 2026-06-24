# TestData DLL 빌드 가이드

이 문서는 TestData DLL을 빌드하는 상세한 방법을 설명합니다.

## 목차

1. [사전 준비](#사전-준비)
2. [Windows 빌드](#windows-빌드)
3. [Linux 빌드](#linux-빌드)
4. [빌드 옵션](#빌드-옵션)
5. [문제 해결](#문제-해결)

## 사전 준비

### 1. libcuo 라이브러리 빌드

TestData는 libcuo 라이브러리에 의존합니다. 먼저 libcuo를 빌드해야 합니다.

```bash
# 상위 디렉토리의 libcuo로 이동
cd ../libcuo

# Visual Studio를 사용하는 경우
# libcuo.sln을 열고 빌드

# 또는 CMake를 사용하는 경우
mkdir build
cd build
cmake .. -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release
```

### 2. 필요한 도구 설치

#### Windows

- **Visual Studio 2017 이상** (Community Edition 가능)
  - C++ 데스크톱 개발 워크로드 설치
  - Windows SDK 포함
- **CMake 3.10 이상**
  - https://cmake.org/download/
- **Python 3.6 이상** (테스트용)
  - https://www.python.org/downloads/

#### Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential cmake python3

# CentOS/RHEL
sudo yum install gcc gcc-c++ make cmake python3

# Arch Linux
sudo pacman -S base-devel cmake python
```

## Windows 빌드

### 방법 1: CMake + Visual Studio (권장)

```powershell
# testData 디렉토리로 이동
cd testData

# 빌드 디렉토리 생성
mkdir build
cd build

# CMake 구성 (Visual Studio 2022)
cmake .. -G "Visual Studio 17 2022" -A x64

# 또는 Visual Studio 2019
cmake .. -G "Visual Studio 16 2019" -A x64

# Release 빌드
cmake --build . --config Release

# Debug 빌드
cmake --build . --config Debug

# 빌드 결과 확인
dir Release\TestDataDLL.dll
# 또는
dir Debug\TestDataDLL.dll
```

### 방법 2: CMake + NMake

```powershell
# Visual Studio 개발자 명령 프롬프트 실행
# 또는 vcvarsall.bat 실행

# 빌드 디렉토리 생성
mkdir build
cd build

# CMake 구성
cmake .. -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release

# 빌드
nmake

# 결과 확인
dir TestDataDLL.dll
```

### 방법 3: Visual Studio 프로젝트 직접 생성

CMakeLists.txt를 사용하지 않고 수동으로 프로젝트를 생성하려면:

1. Visual Studio에서 새 DLL 프로젝트 생성
2. 소스 파일 추가:
   - `TestData.h`, `TestData.cpp`
   - `TestDataExport.h`, `TestDataExport.cpp`
3. 프로젝트 속성 설정:
   - **구성 속성 > 일반**
     - 구성 형식: 동적 라이브러리(.dll)
   - **C/C++ > 일반 > 추가 포함 디렉터리**
     - `$(SolutionDir)..`
     - `$(SolutionDir)../libcuo`
   - **C/C++ > 전처리기 > 전처리기 정의**
     - `TESTDATA_EXPORTS`
   - **링커 > 일반 > 추가 라이브러리 디렉터리**
     - libcuo.lib가 있는 디렉토리
   - **링커 > 입력 > 추가 종속성**
     - `libcuo.lib`
4. 빌드 (Ctrl+Shift+B)

## Linux 빌드

### GCC 사용

```bash
# testData 디렉토리로 이동
cd testData

# 빌드 디렉토리 생성
mkdir build
cd build

# CMake 구성
cmake .. -DCMAKE_BUILD_TYPE=Release

# 빌드 (멀티스레드)
make -j$(nproc)

# 결과 확인
ls -lh libTestDataDLL.so
```

### Clang 사용

```bash
# CMake 구성 시 Clang 지정
cmake .. -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Release

# 빌드
make -j$(nproc)
```

## 빌드 옵션

### CMake 옵션

```bash
# Debug 빌드
cmake .. -DCMAKE_BUILD_TYPE=Debug

# Release 빌드 (최적화)
cmake .. -DCMAKE_BUILD_TYPE=Release

# 설치 경로 지정
cmake .. -DCMAKE_INSTALL_PREFIX=/custom/path

# libcuo 경로 수동 지정
cmake .. -DLIBCUO_DIR=/path/to/libcuo

# 출력 디렉토리 지정
cmake .. -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=/output/path
```

### 고급 설정

CMakeLists.txt를 수정하여 고급 옵션 설정:

```cmake
# C++ 표준 변경 (C++14, C++17, C++20 등)
set(CMAKE_CXX_STANDARD 20)

# 경고 레벨 증가
if(MSVC)
    target_compile_options(TestDataDLL PRIVATE /W4)
else()
    target_compile_options(TestDataDLL PRIVATE -Wall -Wextra)
endif()

# 정적 링크 (libcuo가 정적 라이브러리인 경우)
set(BUILD_SHARED_LIBS OFF)
```

## 설치

```bash
# 빌드 후 시스템에 설치
cd build
cmake --install . --prefix /usr/local

# 또는 make install
sudo make install
```

설치되는 파일:
- `bin/TestDataDLL.dll` (또는 `.so`)
- `include/TestData.h`
- `include/TestDataExport.h`
- `lib/TestDataDLL.lib` (Windows의 경우)

## Python 테스트

빌드가 완료되면 Python 테스트 실행:

```bash
# testData 디렉토리로 돌아가기
cd ..

# Python 테스트 실행
python test_testdata.py

# DLL 경로 명시
python test_testdata.py build/Release/TestDataDLL.dll

# Linux의 경우
python3 test_testdata.py build/libTestDataDLL.so
```

## 문제 해결

### 1. libcuo를 찾을 수 없음

**증상**: CMake 구성 시 libcuo 관련 오류

**해결**:
```bash
# CMakeLists.txt 수정하여 libcuo 경로 지정
# 또는 환경 변수 설정
export LIBCUO_DIR=/path/to/libcuo  # Linux
set LIBCUO_DIR=C:\path\to\libcuo   # Windows
```

### 2. 링크 오류 (unresolved external symbol)

**증상**: 빌드 중 링크 오류 발생

**해결**:
1. libcuo.lib 파일이 존재하는지 확인
2. Release/Debug 구성 일치 확인
3. 32bit/64bit 아키텍처 일치 확인
4. CMakeLists.txt의 링크 경로 수정

```cmake
# Windows
target_link_libraries(TestDataDLL 
    ${LIBCUO_DIR}/x64/Release/libcuo.lib
)

# 또는 환경에 맞게 수정
target_link_libraries(TestDataDLL 
    ${LIBCUO_DIR}/build/libcuo.lib
)
```

### 3. DLL 실행 시 오류 (모듈을 찾을 수 없음)

**증상**: Python 실행 시 DLL 로드 실패

**해결**:
1. libcuo.dll이 시스템 PATH에 있는지 확인
2. DLL을 같은 디렉토리에 복사
3. 환경 변수 PATH에 추가

```powershell
# Windows
$env:PATH += ";C:\path\to\libcuo\x64\Release"

# Linux
export LD_LIBRARY_PATH=/path/to/libcuo/build:$LD_LIBRARY_PATH
```

### 4. Python ctypes 오류

**증상**: `OSError: [WinError 193] %1은(는) 올바른 Win32 응용 프로그램이 아닙니다`

**해결**:
- Python 아키텍처(32bit/64bit)와 DLL 아키텍처가 일치하는지 확인
- 64bit Python에는 64bit DLL 필요

```bash
# Python 아키텍처 확인
python -c "import platform; print(platform.architecture())"
```

### 5. 컴파일 오류 (C2065, C2039 등)

**증상**: 헤더 파일을 찾을 수 없거나 타입 정의 오류

**해결**:
1. 포함 디렉토리가 올바른지 확인
2. pch.h가 있는 경우 미리 컴파일된 헤더 설정
3. CMakeLists.txt 수정

```cmake
target_include_directories(TestDataDLL PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/..
    ${LIBCUO_DIR}
)
```

## 배포

### Windows 배포 패키지

```powershell
# Release 빌드 후
cd build/Release
mkdir deploy

# DLL 복사
copy TestDataDLL.dll deploy\
copy ..\..\..libcuo\x64\Release\libcuo.dll deploy\

# 헤더 파일 복사
mkdir deploy\include
copy ..\..\TestData.h deploy\include\
copy ..\..\TestDataExport.h deploy\include\

# Python 스크립트 복사
copy ..\..\test_testdata.py deploy\

# README 복사
copy ..\..\README.md deploy\
```

### Linux 배포 패키지

```bash
# Release 빌드 후
cd build
mkdir deploy

# 라이브러리 복사
cp libTestDataDLL.so deploy/
cp ../../libcuo/build/liblibcuo.so deploy/

# 헤더 파일 복사
mkdir -p deploy/include
cp ../TestData.h deploy/include/
cp ../TestDataExport.h deploy/include/

# Python 스크립트 복사
cp ../test_testdata.py deploy/

# README 복사
cp ../README.md deploy/
```

## 추가 정보

### 성능 최적화

Release 빌드 시 추가 최적화:

```cmake
# CMakeLists.txt에 추가
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    if(MSVC)
        target_compile_options(TestDataDLL PRIVATE /O2 /Ob2)
    else()
        target_compile_options(TestDataDLL PRIVATE -O3 -march=native)
    endif()
endif()
```

### 디버깅

Debug 빌드로 디버깅:

```bash
# Visual Studio에서 F5로 디버깅
# 또는 Python 디버거 사용
python -m pdb test_testdata.py
```

### 자동 빌드 스크립트

간편한 빌드를 위한 스크립트 생성 가능:

**build.bat** (Windows):
```batch
@echo off
if not exist build mkdir build
cd build
cmake .. -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release
cd ..
echo Build complete!
pause
```

**build.sh** (Linux):
```bash
#!/bin/bash
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
cd ..
echo "Build complete!"
```

## 지원

문제가 지속되면 프로젝트 이슈 트래커에 문의하세요.

