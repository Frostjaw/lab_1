from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		"""os.chdir(os.getcwd() + self.path) #вариант со сменой директории
		cwd = os.getcwd()"""
		
		temp = self.path.split('?')
		path = temp[0]
		cwd = os.getcwd() + path #текущая директория
		if len(temp) == 1:
			query = ''
		else:
			query = temp[1]
			temp_2 = query.split('=')
			query_name = temp_2[0]
			query_param = temp_2[1] #имя папки
			if query_name == 'createdir':
				os.mkdir(cwd+'/'+query_param)
			if query_name == 'deletedir':
				os.rmdir(cwd+'/'+query_param,dir_fd=None)		
		jsonarray = []
		self.send_response(200)	
		if os.path.isfile(cwd):
			self.send_header('content-disposition','attachment') #скачивание файла
		else:
			self.send_header('content-type','application/json')
			for listitem in os.listdir(cwd):
				listitem_path = os.path.join(cwd,listitem)
				json_string = {'Name':os.path.basename(listitem_path),'Path':'/'+os.path.basename(listitem_path),'Size':os.stat(listitem_path).st_size}
				if os.path.isfile(listitem_path):
					json_string.update(Type='file')
				else:
					json_string.update(Type='folder')
				jsonarray.append(json_string)
		self.end_headers()
		jsonobj = json.dumps(jsonarray)
		self.wfile.write(jsonobj.encode())

httpd = HTTPServer(("",8000), myHandler)
httpd.serve_forever()
