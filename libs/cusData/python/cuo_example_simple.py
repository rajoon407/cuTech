#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cuddd 간단한 사용 예제
"""

from cuDataEx_wrapper import Cuddd

def main():
    print("=" * 60)
    print("Cuddd 간단한 예제")
    print("=" * 60)
    
    # 1. 객체 생성 및 데이터 설정
    print("\n1. 객체 생성 및 데이터 설정")
    print("-" * 60)
    
    person = Cuddd("person")
    person.set_string("name", "홍길동")
    person.set_int("age", 30)
    person.set_string("job", "의적")
    person.set_bool("active", True)
    
    print(f"이름: {person.get_string('name')}")
    print(f"나이: {person.get_int('age')}")
    print(f"직업: {person.get_string('job')}")
    print(f"활성: {person.get_bool('active')}")
    
    # 2. XML로 변환
    print("\n2. XML로 변환")
    print("-" * 60)
    
    xml = person.to_xml()
    print(xml)
    
    # 3. JSON으로 변환
    print("\n3. JSON으로 변환")
    print("-" * 60)
    
    json = person.to_json()
    print(json)
    
    # 4. 파일로 저장
    print("\n4. 파일로 저장")
    print("-" * 60)
    
    person.save_xml_file("person.xml")
    person.save_json_file("person.json")
    
    print("✓ person.xml 저장 완료")
    print("✓ person.json 저장 완료")
    
    # 5. 파일에서 로드
    print("\n5. 파일에서 로드")
    print("-" * 60)
    
    loaded_person = Cuddd()
    if loaded_person.from_xml_file("person.xml"):
        print(f"XML 로드 성공: {loaded_person.get_string('name')}")
    
    loaded_person2 = Cuddd()
    if loaded_person2.from_json_file("person.json"):
        print(f"JSON 로드 성공: {loaded_person2.get_string('name')}")
    
    print("\n" + "=" * 60)
    print("예제 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

