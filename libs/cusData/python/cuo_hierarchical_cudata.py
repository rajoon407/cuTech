#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hierarchical CuData - 계층적 구조를 지원하는 CuData 클래스
dict 객체와 CuData 객체 간의 변환을 지원하는 동적 라이브러리
"""

import json
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CuDataType(Enum):
    """데이터 타입 열거형"""
    UNKNOWN = "unknown"
    TEXT = "text"
    JSON = "json"
    BINARY = "binary"
    COMMAND = "command"
    STATUS = "status"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
    HIERARCHICAL = "hierarchical"


class CuDataStatus(Enum):
    """데이터 상태 열거형"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class HierarchicalCuData:
    """계층적 구조를 지원하는 CuData 클래스"""
    id: str = ""
    type: CuDataType = CuDataType.HIERARCHICAL
    name: str = ""
    value: Any = None
    children: List['HierarchicalCuData'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = 0.0
    status: CuDataStatus = CuDataStatus.PENDING
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
    
    def __str__(self):
        return f"HierarchicalCuData(id={self.id}, name={self.name}, type={self.type.value}, children={len(self.children)})"
    
    def __repr__(self):
        return self.__str__()
    
    def add_child(self, child: 'HierarchicalCuData') -> None:
        """자식 노드 추가"""
        self.children.append(child)
    
    def remove_child(self, child_id: str) -> bool:
        """자식 노드 제거"""
        for i, child in enumerate(self.children):
            if child.id == child_id:
                del self.children[i]
                return True
        return False
    
    def find_child(self, child_id: str) -> Optional['HierarchicalCuData']:
        """자식 노드 찾기"""
        for child in self.children:
            if child.id == child_id:
                return child
            # 재귀적으로 하위 노드에서도 검색
            found = child.find_child(child_id)
            if found:
                return found
        return None
    
    def find_by_name(self, name: str) -> Optional['HierarchicalCuData']:
        """이름으로 노드 찾기"""
        if self.name == name:
            return self
        for child in self.children:
            found = child.find_by_name(name)
            if found:
                return found
        return None
    
    def get_all_children(self) -> List['HierarchicalCuData']:
        """모든 하위 노드 가져오기 (재귀적)"""
        result = []
        for child in self.children:
            result.append(child)
            result.extend(child.get_all_children())
        return result
    
    def get_depth(self) -> int:
        """트리 깊이 계산"""
        if not self.children:
            return 0
        return 1 + max(child.get_depth() for child in self.children)
    
    def get_path(self, target_id: str, current_path: List[str] = None) -> Optional[List[str]]:
        """특정 노드까지의 경로 찾기"""
        if current_path is None:
            current_path = []
        
        current_path = current_path + [self.name]
        
        if self.id == target_id:
            return current_path
        
        for child in self.children:
            result = child.get_path(target_id, current_path.copy())
            if result:
                return result
        
        return []
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'type': self.type.value,
            'name': self.name,
            'value': self.value,
            'children': [child.to_dict() for child in self.children],
            'metadata': self.metadata,
            'timestamp': self.timestamp,
            'status': self.status.value,
            'datetime': self.datetime.isoformat()
        }
    
    def to_json(self) -> str:
        """JSON 문자열로 변환"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HierarchicalCuData':
        """딕셔너리에서 생성"""
        children = []
        if 'children' in data and isinstance(data['children'], list):
            children = [cls.from_dict(child_data) for child_data in data['children']]
        
        return cls(
            id=data.get('id', ''),
            type=CuDataType(data.get('type', 'hierarchical')),
            name=data.get('name', ''),
            value=data.get('value'),
            children=children,
            metadata=data.get('metadata', {}),
            timestamp=data.get('timestamp', time.time()),
            status=CuDataStatus(data.get('status', 'pending'))
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'HierarchicalCuData':
        """JSON 문자열에서 생성"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def to_flat_dict(self) -> Dict[str, Any]:
        """평면적 딕셔너리로 변환 (경로를 키로 사용)"""
        result = {}
        
        def _flatten(node, path=""):
            # 루트 노드는 제외하고 자식들만 처리
            for child in node.children:
                current_path = f"{path}.{child.name}" if path else child.name
                
                # 모든 노드를 결과에 추가 (값이 있는 경우)
                if child.value is not None:
                    result[current_path] = child.value
                
                # 자식이 있는 경우 재귀적으로 처리
                if child.children:
                    _flatten(child, current_path)
        
        _flatten(self)
        return result
    
    @classmethod
    def from_flat_dict(cls, flat_dict: Dict[str, Any], root_name: str = "root") -> 'HierarchicalCuData':
        """평면적 딕셔너리에서 계층적 구조로 변환"""
        root = cls(id="root", name=root_name)
        
        for path, value in flat_dict.items():
            parts = path.split('.')
            current = root
            
            # 경로를 따라가면서 노드 생성
            for i, part in enumerate(parts[:-1]):
                child = current.find_by_name(part)
                if not child:
                    child = cls(
                        id=f"{part}_{i}",
                        name=part,
                        type=CuDataType.HIERARCHICAL
                    )
                    current.add_child(child)
                current = child
            
            # 마지막 노드에 데이터 설정
            leaf_name = parts[-1]
            leaf = current.find_by_name(leaf_name)
            if leaf:
                leaf.value = value
            else:
                leaf = cls(
                    id=f"{leaf_name}_{len(current.children)}",
                    name=leaf_name,
                    value=value,
                    type=CuDataType.HIERARCHICAL
                )
                current.add_child(leaf)
        
        return root


class CuDataConverter:
    """dict와 CuData 간의 변환을 담당하는 클래스"""
    
    @staticmethod
    def dict_to_hierarchical_cudata(data: Dict[str, Any], root_name: str = "root") -> HierarchicalCuData:
        """딕셔너리를 계층적 CuData로 변환"""
        root = HierarchicalCuData(id="root", name=root_name)
        
        def _process_dict(dict_data, parent, parent_key=""):
            for key, value in dict_data.items():
                node_id = f"{parent_key}_{key}" if parent_key else key
                
                if isinstance(value, dict):
                    # 중첩된 딕셔너리의 경우
                    child = HierarchicalCuData(
                        id=node_id,
                        name=key,
                        type=CuDataType.HIERARCHICAL,
                        value=None
                    )
                    parent.add_child(child)
                    _process_dict(value, child, node_id)
                elif isinstance(value, list):
                    # 리스트의 경우
                    child = HierarchicalCuData(
                        id=node_id,
                        name=key,
                        type=CuDataType.JSON,
                        value=value
                    )
                    parent.add_child(child)
                else:
                    # 기본 값의 경우
                    data_type = CuDataConverter._detect_value_type(value)
                    child = HierarchicalCuData(
                        id=node_id,
                        name=key,
                        type=data_type,
                        value=value
                    )
                    parent.add_child(child)
        
        _process_dict(data, root)
        return root
    
    @staticmethod
    def hierarchical_cudata_to_dict(cudata: HierarchicalCuData) -> Dict[str, Any]:
        """계층적 CuData를 딕셔너리로 변환"""
        result = {}
        
        def _process_node(node):
            if node.children:
                # 자식이 있는 경우 재귀적으로 처리
                node_dict = {}
                for child in node.children:
                    node_dict[child.name] = _process_node(child)
                return node_dict
            else:
                # 리프 노드의 경우 값 반환
                return node.value
        
        for child in cudata.children:
            result[child.name] = _process_node(child)
        
        return result
    
    @staticmethod
    def _detect_value_type(value: Any) -> CuDataType:
        """값의 타입을 감지"""
        if isinstance(value, str):
            return CuDataType.TEXT
        elif isinstance(value, (int, float)):
            return CuDataType.JSON
        elif isinstance(value, bool):
            return CuDataType.JSON
        elif isinstance(value, (list, tuple)):
            return CuDataType.JSON
        elif isinstance(value, dict):
            return CuDataType.JSON
        else:
            return CuDataType.UNKNOWN


# 편의 함수들
def dict_to_cudata(data: Dict[str, Any], root_name: str = "root") -> HierarchicalCuData:
    """딕셔너리를 CuData로 변환"""
    return CuDataConverter.dict_to_hierarchical_cudata(data, root_name)


def cudata_to_dict(cudata: HierarchicalCuData) -> Dict[str, Any]:
    """CuData를 딕셔너리로 변환"""
    return CuDataConverter.hierarchical_cudata_to_dict(cudata)


def create_hierarchical_cudata(name: str = "root", value: Any = None, **kwargs) -> HierarchicalCuData:
    """계층적 CuData 객체 생성"""
    return HierarchicalCuData(
        id=kwargs.get('id', name),
        name=name,
        value=value,
        type=kwargs.get('type', CuDataType.HIERARCHICAL),
        metadata=kwargs.get('metadata', {}),
        timestamp=kwargs.get('timestamp', time.time()),
        status=kwargs.get('status', CuDataStatus.PENDING)
    )


if __name__ == "__main__":
    print("Hierarchical CuData 모듈이 로드되었습니다.")
    
    # 테스트 예제
    test_dict = {
        "user": {
            "name": "홍길동",
            "age": 30,
            "address": {
                "city": "서울",
                "district": "강남구"
            },
            "hobbies": ["독서", "영화감상", "운동"]
        },
        "settings": {
            "theme": "dark",
            "language": "ko"
        }
    }
    
    print("\n=== 딕셔너리 -> CuData 변환 ===")
    cudata = dict_to_cudata(test_dict)
    print(f"CuData 구조: {cudata}")
    print(f"깊이: {cudata.get_depth()}")
    print(f"모든 자식: {len(cudata.get_all_children())}")
    
    print("\n=== CuData -> 딕셔너리 변환 ===")
    converted_dict = cudata_to_dict(cudata)
    print(json.dumps(converted_dict, ensure_ascii=False, indent=2))
