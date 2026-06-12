### cus  동적 라이브러리 사용 방법  
- c나 c++의 경우 cutilM 을 이용하여 모듈 인터페이스를 사용 할수 있다 
- python 의 경우  cuplay.pas 를 통해 각 모듈의 객체를 사용 할 수 있다.   
- libs/cusNet 관련 예제 객체 로딩 예제 
```
cuPtr<cuNetS> getServer()
{
    cutil* pU = g_pCUBL->getPUtil("cusNet"); // cusNet.so 또는 cusNet.dll에서 cutil 객체를 가지고 온다. 
    if (pU == NULL)
    {
        g_pCUBL->log(CUERR_CUTIL_FDSET_FACTORY, "cutilM::getFDSet factory error[cusNet]");
        return (cuNet*)nullptr;
    }
    cuo q; 
    q.set(CUID_FATYPE, CUID_FATYPE_CUNETS);
    // 객체를 생성 한다. 
    cuNet* pN = (cuNet*)pU->factory(0, &q); 
    return pN;
}
``` 
- libs/cusNet/cuIDXNet.h
```
#define CUID_FATYPE_FDSET		"FDSET"
#define CUID_FATYPE_FDSETNET	"FDSETNET"
#define CUID_FATYPE_CUNETC		"CUNETC"
#define CUID_FATYPE_CUNETS		"CUNETS"
#define CUID_FATYPE_CUNETSR		"CUNETSR"
```
- libs/cusNet/cutilEx.h,  libs/cusNet/cutilEx.cpp
```
class cutilEx : public cutilP
{
protected:

public:
	cutilEx(cutilM *pMU);
	~cutilEx();
	virtual void getDllVer(cuStr& DllPlugID, cuStr& DllVersion); 
	virtual cub* factory(long KType = 0, cub* pP = NULL, const char* FNM = NULL, const char* FNMID = NULL, const char* value = NULL);
};

cub* cutilEx::factory(long DType, cub* pP, const char* FNM, const char* FNMID, const char* value)
{
	if (!pP)
	{
		log(CUERR_PARAMETER_EMTPY, "cutilEx::factory");
		return nullptr;
	}
	cuStr* pFA = pP->getStr(CUID_FATYPE);
	if (!pFA)
	{
		log(CUERR_PARAMETER_EMTPY, "cuStr* pFA = pP->getStr(CUID_FATYPE)");
		return nullptr;
	}

	if (pFA->isEqual(CUID_FATYPE_CUNETS) == 0)	      return new cuSvr();
	else if (pFA->isEqual(CUID_FATYPE_FDSET) == 0)	  return new cuFDSet((cuo*)pP);
	else if (pFA->isEqual(CUID_FATYPE_FDSETNET) == 0) return new cuFDSetNet((cuo*)pP);
	else if (pFA->isEqual(CUID_FATYPE_CUNETC) == 0)
	{
		cuStr FCType = pP->findCharPtr(CUID_FCTYPE);
		cuStr IP = pP->findCharPtr(CUID_FIP);
		cuStr PORT = pP->findCharPtr(CUID_FPORT);
		if (FCType.isEqual("PROC"))			return new cuNetClientPROC(pP->findCharPtr(CUID_IP), pP->findLong(CUID_PORT));
		else if (FCType.isEqual("CMDR"))			return new cuNetClientCMDR(pP->findCharPtr(CUID_IP), pP->findLong(CUID_PORT));
		else if (FCType.isEqual("CMDQ"))			return new cuNetClientCMDQ(pP->findCharPtr(CUID_IP), pP->findLong(CUID_PORT));
		else if (FCType.isEqual("CUMR"))			return new cuNetClientCUMR(pP->findCharPtr(CUID_IP), pP->findLong(CUID_PORT));
		log(CUERR_ADD_DEFKEY, "unknow ctype[%s]", FCType.getCharPtr());
	}
	return nullptr;
}
```
- c,c++ 에서 사용하는 사용 예제 



#### 기본 모듈 
- c, c++, python 사용 설명서  

##### cusCmd 설명 
##### cusData 설명 
##### cusMysql 설명 
##### cusNet 설명 
##### cusPlay 설명 
##### cusPro 설명 

#### 공통 사용 헤더

##### cuIDXCmd.h 
##### cuIDXData.h 
##### cuIDXMysql.h 
##### cuIDXNet.h 
##### cuIDXPlay.h 
##### cuIDXPro.h 
 
