#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hierarchical CuData 사용 예제
dict 객체와 CuData 객체 간의 변환을 보여주는 예제들
"""

import json
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from hierarchical_cudata import (
        HierarchicalCuData, CuDataType, CuDataStatus,
        CuDataConverter, dict_to_cudata, cudata_to_dict,
        create_hierarchical_cudata
    )
    print("✓ Python 모듈 로드 성공")
except ImportError as e:
    print(f"✗ Python 모듈 로드 실패: {e}")
    print("C++ 모듈을 먼저 빌드해주세요: ./build.sh")
    sys.exit(1)

try:
    import hierarchical_cudata_cpp
    print("✓ C++ 모듈 로드 성공")
    cpp_available = True
except ImportError as e:
    print(f"⚠ C++ 모듈 로드 실패: {e}")
    cpp_available = False


def print_separator(title):
    """구분선 출력"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def example_basic_usage():
    """기본 사용법 예제"""
    print_separator("기본 사용법 예제")
    
    # 1. 기본 CuData 객체 생성
    root = create_hierarchical_cudata("root", "루트 노드")
    print(f"루트 노드 생성: {root}")
    
    # 2. 자식 노드 추가
    user_node = create_hierarchical_cudata("user", "사용자 정보")
    user_node.add_child(create_hierarchical_cudata("name", "홍길동"))
    user_node.add_child(create_hierarchical_cudata("age", 30))
    user_node.add_child(create_hierarchical_cudata("email", "hong@example.com"))
    
    root.add_child(user_node)
    
    # 3. 설정 노드 추가
    settings_node = create_hierarchical_cudata("settings", "설정 정보")
    settings_node.add_child(create_hierarchical_cudata("theme", "dark"))
    settings_node.add_child(create_hierarchical_cudata("language", "ko"))
    
    root.add_child(settings_node)
    
    print(f"트리 깊이: {root.get_depth()}")
    print(f"모든 자식 노드 수: {len(root.get_all_children())}")
    
    # 4. JSON 변환
    json_data = root.to_json()
    print(f"JSON 출력:\n{json_data}")
    
    return root


def example_dict_conversion():
    """딕셔너리 변환 예제"""
    print_separator("딕셔너리 변환 예제")
    
    # 복잡한 중첩 딕셔너리 예제
    test_dict = {
        "user": {
            "personal": {
                "name": "홍길동",
                "age": 30,
                "birthday": "1993-01-01"
            },
            "contact": {
                "email": "hong@example.com",
                "phone": "010-1234-5678",
                "address": {
                    "city": "서울",
                    "district": "강남구",
                    "street": "테헤란로 123"
                }
            },
            "preferences": {
                "language": "ko",
                "theme": "dark",
                "notifications": True
            }
        },
        "system": {
            "version": "1.0.0",
            "environment": "production",
            "config": {
                "debug": False,
                "log_level": "info",
                "max_connections": 1000
            }
        },
        "data": {
            "items": ["item1", "item2", "item3"],
            "count": 3,
            "active": True
        }
    }
    
    print("원본 딕셔너리:")
    print(json.dumps(test_dict, ensure_ascii=False, indent=2))
    
    # 1. 딕셔너리 -> CuData 변환
    print("\n--- 딕셔너리를 CuData로 변환 ---")
    cudata = dict_to_cudata(test_dict, "test_root")
    print(f"변환된 CuData 구조:")
    print(f"  - 루트 이름: {cudata.name}")
    print(f"  - 트리 깊이: {cudata.get_depth()}")
    print(f"  - 총 노드 수: {len(cudata.get_all_children()) + 1}")
    
    # 2. CuData -> 딕셔너리 변환
    print("\n--- CuData를 딕셔너리로 변환 ---")
    converted_dict = cudata_to_dict(cudata)
    print("변환된 딕셔너리:")
    print(json.dumps(converted_dict, ensure_ascii=False, indent=2))
    
    # 3. 변환 검증
    print("\n--- 변환 검증 ---")
    is_same = json.dumps(test_dict, sort_keys=True) == json.dumps(converted_dict, sort_keys=True)
    print(f"원본과 변환 결과가 동일한가? {is_same}")
    
    return cudata


def example_flat_dict_conversion():
    """평면적 딕셔너리 변환 예제"""
    print_separator("평면적 딕셔너리 변환 예제")
    
    # 평면적 딕셔너리 예제
    flat_dict = {
        "user.name": "홍길동",
        "user.age": 30,
        "user.address.city": "서울",
        "user.address.district": "강남구",
        "settings.theme": "dark",
        "settings.language": "ko",
        "system.version": "1.0.0"
    }
    
    print("평면적 딕셔너리:")
    for key, value in flat_dict.items():
        print(f"  {key}: {value}")
    
    # 평면적 딕셔너리 -> 계층적 CuData 변환
    cudata = HierarchicalCuData.from_flat_dict(flat_dict, "flat_root")
    print(f"\n변환된 CuData 구조:")
    print(f"  - 루트 이름: {cudata.name}")
    print(f"  - 트리 깊이: {cudata.get_depth()}")
    print(f"  - 총 노드 수: {len(cudata.get_all_children()) + 1}")
    
    # CuData -> 평면적 딕셔너리 변환
    converted_flat = cudata.to_flat_dict()
    print(f"\n변환된 평면적 딕셔너리:")
    for key, value in converted_flat.items():
        print(f"  {key}: {value}")


def example_node_operations():
    """노드 조작 예제"""
    print_separator("노드 조작 예제")
    
    # CuData 트리 생성
    root = dict_to_cudata({
        "company": {
            "name": "테크컴퍼니",
            "employees": {
                "john": {"name": "John Doe", "position": "Developer"},
                "jane": {"name": "Jane Smith", "position": "Designer"}
            }
        }
    })
    
    print("원본 구조:")
    print(json.dumps(root.to_dict(), ensure_ascii=False, indent=2))
    
    # 1. 노드 찾기
    print("\n--- 노드 찾기 ---")
    john_node = root.find_by_name("john")
    if john_node:
        print(f"john 노드 찾음: {john_node}")
        print(f"john의 이름: {john_node.find_child('name').value if john_node.find_child('name') else 'Not found'}")
    
    # 2. 경로 찾기
    print("\n--- 경로 찾기 ---")
    if john_node:
        path = root.get_path(john_node.id)
        print(f"john까지의 경로: {' -> '.join(path)}")
    
    # 3. 노드 추가
    print("\n--- 노드 추가 ---")
    new_employee = create_hierarchical_cudata("bob", "Bob Wilson")
    new_employee.add_child(create_hierarchical_cudata("name", "Bob Wilson"))
    new_employee.add_child(create_hierarchical_cudata("position", "Manager"))
    
    employees_node = root.find_by_name("employees")
    if employees_node:
        employees_node.add_child(new_employee)
        print("새 직원 Bob 추가됨")
    
    # 4. 노드 제거
    print("\n--- 노드 제거 ---")
    if john_node and employees_node:
        removed = employees_node.remove_child(john_node.id)
        print(f"john 노드 제거: {removed}")
    
    print("\n수정된 구조:")
    print(json.dumps(root.to_dict(), ensure_ascii=False, indent=2))


def example_cpp_module_usage():
    """C++ 모듈 사용 예제"""
    if not cpp_available:
        print_separator("C++ 모듈 사용 예제 (건너뜀)")
        print("C++ 모듈이 사용할 수 없습니다.")
        return
    
    print_separator("C++ 모듈 사용 예제")
    
    # C++ 모듈을 사용한 변환
    test_dict = {
        "cpp_test": {
            "message": "C++ 모듈 테스트",
            "number": 42,
            "flag": True
        }
    }
    
    print("C++ 모듈을 사용한 딕셔너리 변환:")
    
    # Python dict -> C++ dict 변환
    cpp_dict = hierarchical_cudata_cpp.py_dict_to_cpp_dict(test_dict)
    
    # C++ 모듈을 사용한 CuData 생성
    cpp_cudata = hierarchical_cudata_cpp.dict_to_cudata(cpp_dict, "cpp_root")
    print(f"C++ CuData 생성: {cpp_cudata}")
    
    # C++ CuData -> C++ dict 변환
    cpp_result_dict = hierarchical_cudata_cpp.cudata_to_dict(cpp_cudata)
    
    # C++ dict -> Python dict 변환
    python_result_dict = hierarchical_cudata_cpp.cpp_dict_to_py_dict(cpp_result_dict)
    
    print("변환 결과:")
    print(json.dumps(python_result_dict, ensure_ascii=False, indent=2))


def example_performance_test():
    """성능 테스트 예제"""
    print_separator("성능 테스트 예제")
    
    import time
    
    # 큰 데이터셋 생성
    large_dict = {}
    for i in range(1000):
        large_dict[f"item_{i}"] = {
            "id": i,
            "name": f"Item {i}",
            "value": i * 2.5,
            "active": i % 2 == 0,
            "metadata": {
                "created": f"2023-01-{i%28+1:02d}",
                "category": f"cat_{i%10}"
            }
        }
    
    print(f"테스트 데이터 크기: {len(large_dict)} 개의 아이템")
    
    # Python 모듈 성능 테스트
    print("\n--- Python 모듈 성능 ---")
    start_time = time.time()
    
    for _ in range(10):
        cudata = dict_to_cudata(large_dict, "performance_test")
        converted = cudata_to_dict(cudata)
    
    python_time = time.time() - start_time
    print(f"Python 모듈 (10회 반복): {python_time:.4f}초")
    
    # C++ 모듈 성능 테스트 (사용 가능한 경우)
    if cpp_available:
        print("\n--- C++ 모듈 성능 ---")
        start_time = time.time()
        
        for _ in range(10):
            cpp_dict = hierarchical_cudata_cpp.py_dict_to_cpp_dict(large_dict)
            cpp_cudata = hierarchical_cudata_cpp.dict_to_cudata(cpp_dict, "performance_test")
            cpp_result = hierarchical_cudata_cpp.cudata_to_dict(cpp_cudata)
            python_result = hierarchical_cudata_cpp.cpp_dict_to_py_dict(cpp_result)
        
        cpp_time = time.time() - start_time
        print(f"C++ 모듈 (10회 반복): {cpp_time:.4f}초")
        
        if python_time > 0:
            speedup = python_time / cpp_time
            print(f"성능 향상: {speedup:.2f}x")


def main():
    """메인 함수"""
    print("Hierarchical CuData 라이브러리 사용 예제")
    print("=" * 60)
    
    try:
        # 각 예제 실행
        example_basic_usage()
        example_dict_conversion()
        example_flat_dict_conversion()
        example_node_operations()
        example_cpp_module_usage()
        example_performance_test()
        
        print_separator("모든 예제 완료")
        print("✓ 모든 예제가 성공적으로 실행되었습니다!")
        
    except Exception as e:
        print(f"\n✗ 예제 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
