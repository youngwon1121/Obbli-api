class DBConnectionMiddleware:

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		print('HELLO')
		print(request.get_full_path())
		response = self.get_response(request)
		return response