##### libcuo/cuRender.h
- cubl 객체에 대한 Transfrom 기능으로  
  Json, Xml, Tcp/Ip 통신을 위한 메모리, markdown 기능을 제공한다.   
  paserStr 는  스트링 또는 메모리 데이터를  객체로 변환하는 기능  
  makeStr  는 객체를 스트링 또는 메모리로 변환 하는 기능을 제공 한다. 
  특성에 따라 CharPtr , WCharPtr 로 저장 가능하다. 

- Render 종류

```
//T3 Type of CU_DTYPE2_RENDER
#define CU_DTYPE3_RENDERXML		 CU_DTYPE3(1)
#define CU_DTYPE3_RENDERJSON	 CU_DTYPE3(2)
#define CU_DTYPE3_RENDERMD		 CU_DTYPE3(3)
#define CU_DTYPE3_RENDERHTML	 CU_DTYPE3(4)
#define CU_DTYPE3_RENDERTEXT	 CU_DTYPE3(5)
#define CU_DTYPE3_RENDERNETDATA  CU_DTYPE3(6)
```
- 베이스 클래스 정의  
```
class cuRender : public cuo
{
	cuStr* m_pStr; 
protected:
	cuRender(long ctype) : cuo(ctype) {	m_pStr = NULL; 	}
public:
	bool           isStream();
	virtual bool   isExistParent(cub* pD);

	virtual long	paserFile(cuStr* pPath, cub** ppOut);
	virtual long	makeFile (cub* pD, cuStr* pPath  );
	virtual long	paserStr (cuStr* pStr, cub** ppOut) = 0;
	virtual long	makeStr  (cub* pD, cuStr* pStr   ) = 0;
};
```  
-   기본 사용 방법 
```
long CU_DTYPE3_RENDERNETDATA_Test()
{
    cuo c;
    c.set(CUID_USERID, "user"); 
    g_pCUBL->log(0, "set[%s:%s]", CUID_USERID, c.getCharPtr(CUID_USERID));
    cuStr strout; 
    g_pCUBL->makeStr(&c, &strout, CU_DTYPE3_RENDERNETDATA);
    cub* ppOut;
    g_pCUBL->paserStr(&strout, &ppOut, CU_DTYPE3_RENDERNETDATA);
    if (!ppOut)
        return g_pCUBL->log(0, "Empty"); 
    return g_pCUBL->log(0, "ret[%s:%s]", CUID_USERID, ppOut->getCharPtr(CUID_USERID));
}
```
- 결과 
```
[21:23:30.177][00000][cutilM][000000]set[USERID:user]
[21:23:30.180][00030][cutilM][000000]cutilM::getUtil [cusData]
[21:23:30.181][00030][FDLLNM][cusData]cuDll::_Loader Start[cusData.dll]
[21:23:30.231][00000][FDLLNM][cusData]cuDll::_Loader OK[cusData.dll][CUDATA][00000001]
[21:23:36.549][00000][cutilM][000000]ret[USERID:user]
```