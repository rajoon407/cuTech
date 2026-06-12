#### cuNet 을 이용한 Tcp/Ip 네트워크 셈플 활용 


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