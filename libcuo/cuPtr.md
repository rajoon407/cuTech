### cuPtr(libcuo/cuPtr.h) 
- CUBL 에서의 스마트 포인트 기능 
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
- cuPtr 를 사용할 경우 그리고 사용해야 하는 이유는 
  참조를 위해서이며 참조가 갖고 있는 여러가지 장점를 활용하기 위한 기법이다.  
  cuPtr 를 사용하지 않으면 nRefCount_ 카운트는 증가하지 않는다.  

  A와 B의 라이프 사이클이 서로 다르고 종속적이지 않을 경우   
  마지막 살아 있는 객체에 스마트 포인트를 쓸 것을 추천 한다.  
  아니면 별도로 마지막 객체 소멸자에서 강제 삭제를 실행 해야 한다. 
    