# -*- coding: UTF-8 -*-

__author__ = 'Mr.Bluyee'

import os
import sys
import hashlib
			
			
class HideFile(object):

	def __init__(self,file_path):
		"""类初始化
		Args:
			file_path: 包含具体文件名的路径(str)
		Raises:
			FileExistsError: 文件不存在错误
		"""	
		self.filepath = file_path
		if os.path.exists(self.filepath) == False:
			raise FileExistsError('No exist file!')
		self.filesize = self.get_filesize()
		self.filename = os.path.split(self.filepath)[1]
		self.fileMD5 = self.get_fileMD5()
		self.__fileseek = 0
	
	def set_fileseek(self,fileseek):
		"""设置文件游标
		Args:
			fileseek: 文件游标值(int)
		"""	
		self.__fileseek = fileseek
		
	def get_fileseek(self):
		"""获取文件当前位置游标
		Returns:
			self.__fileseek: 文件当前游标值(int)
		"""	
		return self.__fileseek
	
	def get_filesize(self):
		"""获取文件大小(单位:bytes)
		Returns:
			self.filesize: 文件大小(int)
		"""	
		self.filesize = os.path.getsize(self.filepath)
		return self.filesize
	
	def get_fileMD5(self):
		"""获取文件MD5值
		Returns:
			md5: 文件MD5值(str)
		"""	
		with open(self.filepath,'rb') as MD5file:
			md5=hashlib.md5(MD5file.read()).hexdigest()
		return md5
		
	def read_filedatas(self,fileseek,data_num):
		"""读取文件数据(以二进制流方式)
		Args:
			fileseek: 开始读取的文件位置(int)
			datas_num: 要读取的bytes数据的个数(int)
		Returns:
			file_datas: 从文件中读出的数据(bytes)
		"""
		if (fileseek + data_num) > self.filesize:
			print('read over file size!')
			return
		with open(self.filepath,'rb') as file:
			file.seek(fileseek)
			file_datas = file.read(data_num)
		return file_datas

		
class SaveFile(HideFile):

	def __init__(self,filename):
		"""类初始化
		Args:
			filename: 具体文件名(str)
		"""	
		self.filename = filename
		self.filepath = ''
		self.filesize = 0
		self.fileMD5 = ''
		
	def get_filesize(self):
		"""获取文件大小(单位:bytes)
		Returns:
			self.filesize: 文件大小(int)
		"""	
		return self.filesize
	
	def creat_file(self):
		"""创建新文件
			注意:如果同名文件存在则覆盖掉
		"""	
		if len(self.filepath) == 0:
			print('invalid file path!')
			return
		if os.path.exists(self.filepath):
			print('delete exist file!')
			os.remove(self.filepath)
		new_file = open(self.filepath,'w')
		new_file.close()
		
	def write_filedatas(self,datas):
		"""写入文件数据(以二进制流追加方式)
		Args:
			datas: 要写入的数据(bytes)
		"""	
		if os.path.exists(self.filepath) == False:
			print('No exist file!')
			return
		with open(self.filepath,'ab') as file:
			file.write(datas)		

		
def test():
	"""测试方法用"""
	root_dir = os.getcwd()
	sf = SaveFile('hello.txt')
	sf.filepath = sf.filename
	sf.creat_file()
	sf.write_filedatas(b'hello world!')
	
	hf = HideFile('hello.txt')
	print(hf.get_filesize())
	print(hf.read_filedatas(2,2))
	print(hf.fileMD5)

if __name__ == '__main__':
	test()