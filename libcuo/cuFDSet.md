### cuFDSet 

- 스레드에서 작업 대기 관련 처리  

#### libcuo/cuFDSet.h  베이스 헤더 

```   
class cuFDSet : public cuo
{
protected:    
	std::condition_variable			m_cv;
	std::mutex						m_mtx;
	bool							m_bReady; 
	cuPtr<cuVector>					m_RecvList;
public:
	virtual long      cuWait(long mmsec = 100000); 
};  
```


#### libcuo/cuFDSet.cpp 일부  
- 약간의 응용
   - 궁극적인 방법은 종료 시점에 종료 처리 후 Resume() 하는 거지만  
   타임아웃을 짧게 여러번 잡아 외부 상태 감지하도록 하여 한다.   

```
long cuFDSet::cuWait(long mmsec)
{
	std::unique_lock<std::mutex> lock(m_mtx);
	if (mmsec < CUNUM_FDSET_INTERVAL)
		mmsec = 2000;
    
	int v = mmsec / CUNUM_FDSET_INTERVAL; 
    for (int i = 0; i < v; i++)
    {
        m_cv.wait_for(lock, .... [this] (){
			return m_RecvList.size() > 0 || m_bReady; });
		if (m_bReady || m_RecvList.size() > 0) 
		{
			log(0, "cuFDSet::cuWait() Resume Start OK");
			m_bReady = false; 
			return CU_WAIT_OK;
		}

		if(isStop())
		   return CU_WAIT_FAIL; 
    }
    return CU_WAIT_TIMEOUT;
}
```


#### 활용  libtest/test_FDSet/cuThread.cpp

```
long cuThread_test::_work()
{
	cuFDSet* pFD = _getFDSet();
	setStop(false);
	while(!isStop()) 
	{
		long nStatus = pFD->cuWait(100000); 
		if (nStatus == CU_WAIT_OK)
		{
			cuVector* pRL = pFD->getReveList();
			if (pRL)
			{
				if (pRL->size() > 0)
				{
					for (long i = 0; i < pRL->size(); i++)
					{
						cuo* pD = (cuo*)pRL->pop();
						_showlog(pD);
						i--;
					}
				}
			}
			continue;
		}
		else if (nStatus == CU_WAIT_TIMEOUT)
			log(0, "cuThread_test::_work() waiting for data...");
		else
			break;
	}	
	return CUOK;	
}
```


#### 활용 작업 요청 libtest/test_FDSet/cuThread_Action.cpp

```

long	cuThread_CmdAction_Send::action(cuPtr<cuCmdResult> result, cuo* q, cuCmdS* pA)
{
	cuPtr<cuo>  sdata = new cuo();  // 스마트 포인트 객체 생성 
	sdata->set("msg", "cuThread_CmdAction_Send");
	cuStr strXml; 
	strXml.setType(CU_DTYPE3_DX);
	sdata->getString(strXml);
	if(getThread())
		return getThread()->setRecvData(sdata);
	return CUFAIL;
}
```