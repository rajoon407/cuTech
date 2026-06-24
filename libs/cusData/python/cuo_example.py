#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cuddd 계층 구조 예제 - 도서관 시스템
"""

from cuoWrapper import cuo

def main():
    print("=" * 60)
    print("Cuddd 계층 구조 예제 - 도서관 시스템")
    print("=" * 60)
    
    # 도서관 생성
    library = cuo("library")
    library.set_string("name", "중앙 도서관")
    library.set_string("location", "서울특별시 종로구")
    library.set_int("founded", 1945)
    library.set_bool("open", True)
    
    # 책 추가
    books = [
        {"title": "파이썬 프로그래밍", "author": "김철수", "year": 2023, "rating": 4.5},
        {"title": "C++ 완벽 가이드", "author": "이영희", "year": 2022, "rating": 4.8},
        {"title": "데이터 구조와 알고리즘", "author": "박민수", "year": 2024, "rating": 4.3},
        {"title": "웹 개발 입문", "author": "정수진", "year": 2023, "rating": 4.6},
        {"title": "인공지능 기초", "author": "최현우", "year": 2024, "rating": 4.7},
    ]
    
    print(f"\n도서관 정보:")
    print(f"  이름: {library.get_string('name')}")
    print(f"  위치: {library.get_string('location')}")
    print(f"  설립연도: {library.get_int('founded')}")
    print(f"  영업중: {library.get_bool('open')}")
    
    print(f"\n책 추가 중...")
    for book_data in books:
        book = library.add_child("book")
        book.set_string("title", book_data["title"])
        book.set_string("author", book_data["author"])
        book.set_int("year", book_data["year"])
        book.set_double("rating", book_data["rating"])
        print(f"  ✓ {book_data['title']} - {book_data['author']}")
    
    print(f"\n총 {library.get_child_count()}권의 책이 등록되었습니다.")
    
    # XML 저장
    print("\nXML 파일 저장 중...")
    library.save_xml_file("library.xml")
    print("  ✓ library.xml 저장 완료")
    
    # JSON 저장
    print("\nJSON 파일 저장 중...")
    library.save_json_file("library.json")
    print("  ✓ library.json 저장 완료")
    
    # XML 내용 출력
    print("\n" + "=" * 60)
    print("XML 내용:")
    print("=" * 60)
    xml = library.to_xml()
    print(xml)
    
    # JSON 내용 출력
    print("=" * 60)
    print("JSON 내용:")
    print("=" * 60)
    json = library.to_json()
    print(json)
    
    # 파일에서 다시 로드
    print("=" * 60)
    print("파일에서 로드 테스트")
    print("=" * 60)
    
    loaded_library = cuo()
    if loaded_library.from_xml_file("library.xml"):
        print(f"\n✓ XML 로드 성공")
        print(f"  도서관 이름: {loaded_library.get_string('name')}")
        print(f"  책 수: {loaded_library.get_child_count()}")
        
        print("\n  등록된 책 목록:")
        for i in range(loaded_library.get_child_count()):
            book = loaded_library.get_child(i)
            if book:
                title = book.get_string("title")
                author = book.get_string("author")
                year = book.get_int("year")
                rating = book.get_double("rating")
                print(f"    {i+1}. {title} - {author} ({year}) ★{rating}")
    
    print("\n" + "=" * 60)
    print("예제 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

