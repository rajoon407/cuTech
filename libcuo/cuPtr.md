### cuPtr(libcuo/cuPtr.h) 
- CUBL 에서의 스마트 포인트 기능 


#### 유의 사항 
##### cuPtr<T>& operator=(T* ptr)  와 cuPtr<T>& operator=(const bool lp)  오동작   
- C++에서 대입 연산 시 의도치 않게 다른 객체가 bool로 변환되어 operator=(const bool lp) 함수로  
  잘못 흘러 들어가는 현상은 실무에서 빈번히 발생하는 위험한 부작용(Side Effect)  
  <b>받은 스마트 포인터의 T 객체형과 오른쪽 객체의 객체형을 일치 시키면 된다.</b>  

#### 생성과 소멸 라이프 사이클  
- 메모리 릭 발생 
```
{
    cuStr  * pStr = new cuStr(); 
}
```
- 스마트 포인트에 의해 소멸됨 
```
class test
{
    cuPtr<cuStr> m_Str
    setData(cuStr * pStr){m_Str = pStr;}
};

{
    test t; 
    cuStr  * pStr = new cuStr();
    cuPtr<cuStr> str = pStr;
    t.setData(str);   
}
```
- 구역에서 생성하고 스마트 포인트를 통해 외부로 리턴 할 경우 어떡해 될까  
  new 로 생성된 객체가 리턴 받았을 경우 실제 리퍼 카운트가 증가되었다가 감소 되었음을 확인 해야 한다.  
  makeStr() 펑션 블럭이 될때   
  리턴을 통해 리퍼 카운트가 증가된 후   
  리퍼 카운트가 감소된다.    

```
cuPtr<cuStr> cuThread_test::makeStr()
{
	cuPtr<cuStr> str = new cuStr("111");
	return str;  
}

cuThread_test::testPtr()
{
	cuStr<cuStr> v = makeStr(); 
	prientf("%s", v.getCharPtr())
}
```

- 단순하게 cuPtr 은 내부 변수로 구역을 벗어나면 당연히 소멸자를 호출 한다.  
```
	void destroy() noexcept {
		if (pObject_ == nullptr)
			return;

		int decrmentCount = ((cub*)pObject_)->decrement();
		if (decrmentCount <= 0 && pObject_) {
			((cub*)pObject_)->_Release();
		}
		pObject_ = nullptr;
	}

	cuPtr(T* ptr)
	{
		pObject_ = ptr;
		if (pObject_)
			((cub*)pObject_)->increment();
	}

```

- libcuo/cub.h   
```
int decrement() { return --nRefCount_; }
```

- 결과적으로 cuPtr은  cub를 상속 받은 객체만 수용 가능하고  
  결과적으로 (cub.nRefCount_ <= 0) 조건을 만족하면 삭제 된다.  

```
void cub::_Release()
{
	decrement(); 
	if (nRefCount_ <= 0)
		delete this;
}
```

- 스마트 포인트는 리퍼 카운트를 증가 시킨다.  
  사용한 스마트 포인트가 모두 해제 되는 순간 삭제 된다.  


#### 개인적인 견해 유의사항  
- 일반적으로 스마트 포인트를 사용하는 이유는 
   - 메모리 누수 방지: 스마트 포인터가 범위를 벗어나면(Scope Out) 소멸자가  
    자동으로 메모리를 해제합니다.  
	예외 안전성: 코드 실행 중 예외가 발생하더라도 해제되지 않은 메모리가  
	남지 않도록 보장합니다.  
	소유권 명확화: 객체의 소유권(독점/공유)을 코드 레벨에서 명확히 구분할 수 있습니다.

- 개인적으로 위의 내용은 잘 사용할때 그런 거고  
  실제 cuPtr 를 사용하는 이유는 개인적인 스타일, 즉 CUBL에서 객체를 다루는  
  방식, 포인터를 다루는 방식을 편리성으로, 강제 하여, 코딩 규약을 만드는 것이다.  

  현재의 스마트 포인터는 완성형이라 생각하지 않는다.  
  
  - cuPtr 를 사용하지 않으면 nRefCount_ 카운트는 증가하지 않는다.  

