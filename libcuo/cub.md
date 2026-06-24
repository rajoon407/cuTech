####  cub.h cubl 의 베이스 클래스 
- cubl의 스마트 포인트 cuPtr과 연계되어 모든 객체의 베이스가 되는 클래스 이다  
  cubl의 모든 객체는 cub를 상속 받는다. 


##### cubl 의 객체의 타입 설정 
- 객체는 3단계의 타입으로 설정된다.  
   - 1단계 단순한 객체인가 ? 복잡한 구조의 객체인가. (코드는 단계 범위내 유니크 하다.) 
   ```
        //libcuo/cuIDX.h
        #define CU_DTYPE1_EMPTY         0
        #define CU_DTYPE1_UNKNOW        1
        #define CU_DTYPE1_CUO           2   //Object (Map, Vector, Cuo)
        #define CU_DTYPE1_CUD           3   //Data   (str, Rect ...)

   ```
   - 2단계 클래스 세부적 타입 (코드는 단계 범위내 유니크 하다.)  
     libcuo  라이브러리의 베이스 정적 모듈에 속해 있는 베이스 클래스    
   ```
    #define CU_DTYPE2_UNKNOWN		 CU_DTYPE2(1)
    #define CU_DTYPE2_STR			 CU_DTYPE2(2)
    #define CU_DTYPE2_STREAM		 CU_DTYPE2(4)		
    #define CU_DTYPE2_RECT			 CU_DTYPE2(5)
    #define CU_DTYPE2_POS			 CU_DTYPE2(6)

    #define CU_DTYPE2_VECTOR		 CU_DTYPE2(7)
    #define CU_DTYPE2_MAPA			 CU_DTYPE2(8)
    #define CU_DTYPE2_MAPL			 CU_DTYPE2(9)
    #define CU_DTYPE2_CUO			 CU_DTYPE2(10)	
    #define CU_DTYPE2_CMD            CU_DTYPE2(11)
    #define CU_DTYPE2_RENDER         CU_DTYPE2(12)
    #define CU_DTYPE2_PRO            CU_DTYPE2(13)
    #define CU_DTYPE2_THREAD         CU_DTYPE2(14)
    #define CU_DTYPE2_UTILP          CU_DTYPE2(15)
    #define CU_DTYPE2_UTILM          CU_DTYPE2(16)

    #define CU_DTYPE2_EXT1			 CU_DTYPE2(20)
    #define CU_DTYPE2_DATA           CU_DTYPE2(21)
    #define CU_DTYPE2_CTRI           CU_DTYPE2(21)
    #define CU_DTYPE2_CINDX          CU_DTYPE2(22)
    #define CU_DTYPE2_DBCON          CU_DTYPE2(24)
    #define CU_DTYPE2_DBSQL          CU_DTYPE2(25)
    #define CU_DTYPE2_ENC            CU_DTYPE2(26)
    #define CU_DTYPE2_DLL            CU_DTYPE2(27)
    #define CU_DTYPE2_LOCK           CU_DTYPE2(28)
    #define CU_DTYPE2_CUM            CU_DTYPE2(29)
    #define CU_DTYPE2_MET            CU_DTYPE2(30)
    #define CU_DTYPE2_METRIX         CU_DTYPE2(31)
    #define CU_DTYPE2_CUMM           CU_DTYPE2(32)
    #define CU_DTYPE2_ACTION	     CU_DTYPE2(33)	
    #define CU_DTYPE2_CONF	         CU_DTYPE2(34)	
    #define CU_DTYPE2_CMDATT         CU_DTYPE2(35)	

    #define CU_DTYPE2_FD		     CU_DTYPE2(41)
    #define CU_DTYPE2_NET            CU_DTYPE2(42)
    #define CU_DTYPE2_NETS           CU_DTYPE2(43)
    #define CU_DTYPE2_NETC           CU_DTYPE2(44)
    #define CU_DTYPE2_NETSR          CU_DTYPE2(45)
    #define CU_DTYPE2_NETSC          CU_DTYPE2(46)
    #define CU_DTYPE2_NETCC          CU_DTYPE2(47)
    #define CU_DTYPE2_NETSRC         CU_DTYPE2(48)
    #define CU_DTYPE2_NETD	         CU_DTYPE2(49)   
   ```
   - 3단계 세부 클래스 종류 ( 코드는 2단계 그룹단위로 유니크 하다. ) 

```
//libcuo/cuIDX.h
struct _cutype
{
	unsigned char T1;
	unsigned char T2;
	unsigned char T3;
};

```
