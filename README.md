# Obbli-api
API written in DRF, python

/user/login/   
	POST : 로그인을 수행한다.  

/user/join/  
	POST : 회원가입을 수행한다.  

/user/me/  
	GET : 본인 정보 가져오기(포함 : 본인이 접수한 목록) 토큰으로가져옴  
	User Applying + Announce   

/user/me/applying/
	GET : 본인 지원목록 가져오기  
		output : url & announce제목 & 마감일자  

/user/me/announce/  
	GET : 본인이 올린 글 가져오기    

/user/me/announce/\<pk\>/  
	GET : 올린 글 상세정보(접수자까지 보기)   

/user/me/profile/   
	GET : 본인 프로필 가져오기   
	POST : 프로필 등록   

/user/me/profile/\<pk\>/   
	GET : 본인 프로필 상세보기   
	PUT : 본인 프로필 수정하기   
	DELETE : 본인 프로필 삭제하기   

/announce/  
	GET : 구인목록  
	POST : 구인글쓰기  

/announce/\<pk\>/  
	GET : 구인 글 상세보기(전체 보기 가능)  
	PUT : 구인 글 수정(작성자만 가능)	  
	DELETE : 구인 글 삭제(작성자만 가능)  

/announce/\<pk\>/applying/  
	POST : announce pk=pk인 글에 이력서 접수하기(성공)  
