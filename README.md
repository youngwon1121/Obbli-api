# Obbli-api
API written in DRF, python

/user/login/   
	POST : 로그인을 수행한다. 

/user/join/  
	POST : 회원가입을 수행한다.

/user/reset_password/send_mail/
	POST : 해시값 생성 후, 이메일로 전송	
	@param email
		성공 : 201
		body체크 : 400
		user중에 해당 email을 가진유저 없을 떄 : 404
		이메일 발송 실패시 : 500

	PUT : 
	@param email
	@param hash_key
		db에서 제일최근 userid필드를 뽑고 hash_key와 맞는지 비교
		email hash_key : 400
		email에 해당하는데이터 or 3분이내의 데이터가 없는경우 : 404
		hash_key가 달라서 verified가 인증되지않았을때 : 403


/user/reset_password/
	PUT
	@param email
	@param hash_key
	@param password

	email or hash_key없을때 : 400
	파라미터들에 맞는 모델인스턴스가 없을 떄 : 401
	성공 : 200

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
		프로필사진의 selfie resizing적용

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
