#### cuNet 을 이용한 Tcp/Ip 네트워크 셈플 활용 

##### Cubl Net 에서 RAS 규약 
- 통신은 connected 방식으로 처리 된다. 
- 통신은 무조건 RAS 를 강제 한다.  (보안적 이유)
  * 다만 서버나 클라이언트의 사용 방법에 따라 무시 될 수 있다.  
  * 기본적으로 RAS 를 통과 하지 못한 클라이언트는 바로 연결 해지 된다.  
- 클라이언트가 접속 시도 전에 RAS 정보를 강제로 넣는다. 
```
long cuNet_C::startNet(const char* ip, int port). (베이스에 로직 적용되어 있음)
{
	cuo* pRas = getRasInfo();
	if (!pRas)
	{
		cuo* pRas = new cuo();
		pRas->set(CUID_USERID, "test");
		pRas->set(CUID_PASSWD, "test");
		_setRasInfo(pRas);
	}
	return _startNet(ip, port);
}
```  
- 접속 클라이언트 소스 전체  
```
#include "pch.h"
#include "cuNet_C.h"

cuNet_C::cuNet_C() : cuNetCC()
{
	setFNM("cuNetCC"); 
	setNet(nullptr, CUID_FATYPE_CUNETC);
}
long cuNet_C::onStatus(const char* key, long nStatus)
{
	return log(nStatus, "cuNet_C::onStatus[%s][%d]", key, nStatus);
}

long cuNet_C::onRecv(cuo* pChild, cuo* pData)
{
	log(0, "cuNet_C::onRecv"); 
	return CUFAIL; 
}
void cuNet_C::onClose(cuo* pChild)
{
	log(0, "cuNet_C::onClose");
}
void cuNet_C::setRas(const char* id, const char* pW)
{
	cuo* pRas = getRasInfo();
	if (!pRas)
	{
		cuo* pRas = new cuo();
		pRas->set(CUID_USERID, id);
		pRas->set(CUID_PASSWD, pW);
		_setRasInfo(pRas);
	}
	else
	{
		pRas->set(CUID_USERID, id);
		pRas->set(CUID_PASSWD, pW);
	}

}
long cuNet_C::startNet(const char* ip, int port)
{
	cuo* pRas = getRasInfo();
	if (!pRas)
	{
		cuo* pRas = new cuo();
		pRas->set(CUID_USERID, "test");
		pRas->set(CUID_PASSWD, "test");
		_setRasInfo(pRas);
	}
	return _startNet(ip, port);
}
``` 
- 서버는 강제로 Ras 에 대한 응답을 처리 해야 한다. (베이스에 로직 적용되어 있음)    
```
long      cuNet_Svr::isLoginWork(cuNetD* pData)
{
	log(0, "cumSC::isLoginWork[%s] - ", pData->getNetID());
	if (pData->is(CUID_USERID, "test") && 
	pData->is(CUID_PASSWD, "test"))
		return CUOK; 	
	return CUERR_NET_CUNETS_RAS;
}
```  
- 보내 준대로 데이터를 확인 한다. 


- 서버 전체 소스 
```

cuNet_Svr::cuNet_Svr(cuNetS* pNetS, cuo* pNetInfo)
	: cuNetSC(pNetS, pNetInfo)
{
	setFNM("cuNetSC"); 
}
cuNetSRC* cuNet_Svr::onAccept(cuNetSR* pSR)
{
	log(0, "cuNet_Svr::onAccept");
	return new cuNet_SRC(pSR);
}
long      cuNet_Svr::isLoginWork(cuNetD* pData)
{
	log(0, "cumSC::isLoginWork[%s] - ", pData->getNetID());
	if (pData->is(CUID_USERID, "test") && pData->is(CUID_PASSWD, "test"))
		return CUOK; 	
	return CUERR_NET_CUNETS_RAS;
}
long      cuNet_Svr::onRecvWork(cuo* pSRC, cuo* pData)
{
	log(0, "cumSC::onRecvWork[%s] - ", ((cuNetSRC*)pSRC)->getID());
	return CUFAIL;
}
void      cuNet_Svr::onCloseWork(cuo* pSRC)
{
	log(0, "cuNet_Svr::onRecvWork[%s]", ((cuNetSRC*)pSRC)->getID());
}
long      cuNet_Svr::startServer(const char* ip, int port, const char* AType)
{
	return _startNet(ip, port, nullptr, AType);
}
```

##### 서버 생성 및 실행 
- libcuo/cuNet.h 의 cuNetSC 클래스를 상속 시킨다.

```
class cuNet_Svr : public cuNetSC
{
protected:
	cuNet_Svr(cuNetS* pNetS = nullptr, cuo* pNetInfo = nullptr);
	void      onClose(cuo* pChild = nullptr);
public:
	cuNetSRC* onAccept(cuNetSR* pSR);
    long startServer(int port, const char* AType = CUID_FATYPE_CUNETS)
};
```
- startServer 구현 부분 
```
cuNet_Svr::cuNet_Svr(cuNetS* pNetS, cuo* pNetInfo)
	: cuNetSC(pNetS, pNetInfo)
{
}
cuNetSRC* cuNet_Svr::onAccept(cuNetSR* pSR)
{
	log(0, "cuNet_Svr::onAccept");
	return new cuNet_SRC(pSR);
}
void      cuNet_Svr::onClose(cuo* pChild)
{
	log(0, "cuNet_Svr::onClose"); 
}
long      cumSC::startServer(const char* ip, int port, const char* AType)
{
	return _startNet(ip, port, AType);
}
```


##### 클라이언트 생성 