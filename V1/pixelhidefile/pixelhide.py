# -*- coding: UTF-8 -*-

__author__ = 'Mr.Bluyee'

import os
import sys
from pixelhidefile.filehandle import HideFile,SaveFile
from pixelhidefile.imagehandle import HideImage


headmessage = {
	'file name': '',
	'file size': '',
	'file MD5': '',
	'encryption': ''
	}

def hide_file_to_image(file_path,image_path,encryption='no'):
	"""将文件隐藏到图片中
		在要隐藏的文件目录下自动生成与文件同名的PNG图片
	Args:
		file_path: 包含具体文件名的路径(str)
		image_path: 包含具体文件名的路径(str)
		encryption='no': 默认加密方式：不加密(功能待添加)
	"""
	img = HideImage(image_path)
	print('image width: ' + str(img.imagewidth) + ' px')
	print('image height: ' + str(img.imageheight) + ' px')
	print('image capacity: ' + str(img.imagecapacity) + ' bits')
	file = HideFile(file_path)
	headmessage['file name'] = file.filename
	headmessage['file size'] = str(file.filesize)
	headmessage['file MD5'] = str(file.fileMD5)
	headmessage['encryption'] = encryption
	print('file name: ' + headmessage['file name'])
	print('file size: ' + headmessage['file size'] + ' bytes')
	print('file MD5: ' + headmessage['file MD5'])
	print('encryption: ' + headmessage['encryption'])
	headmsg = bytes(str(headmessage).encode('utf-8'))
	img.writedatalen = (len(headmsg) + file.filesize) * 8
	print('write datas total length: ' + str(img.writedatalen ) + ' bits')
	if img.writedatalen > img.imagecapacity:
		print('write datas over capacity!')
		return
	img.write_pixels(headmsg)
	file_size_quotients = file.filesize // 100
	file_size_remainder = file.filesize % 100
	if file_size_quotients > 0:
		for i in range(0,file_size_quotients):
			file.set_fileseek(100 * i)
			file_data = file.read_filedatas(file.get_fileseek(),100)
			img.write_pixels(file_data)
		file.set_fileseek(100 * file_size_quotients)	
	file_data = file.read_filedatas(file.get_fileseek(),file_size_remainder)
	img.write_pixels(file_data)
	img.save_change(os.path.splitext(file_path)[0])
	
def read_file_from_image(image_path,created_file_path=''):
	"""读取图片中的隐藏文件
	Args:
		image_path: 包含具体文件名的路径(str)
		created_file_path='': 创建文件的路径(不含文件名)，默认路径为当前代码路径
	"""
	img = HideImage(image_path)
	print('image width: ' + str(img.imagewidth) + ' px')
	print('image height: ' + str(img.imageheight) + ' px')
	print('image capacity: ' + str(img.imagecapacity) + ' bits')
	headmsg_temp = img.read_pixels(12)
	if headmsg_temp != b'{\'file name\'':
		print('image has no hide message or broken!')
		return
	headmsg_temp += img.read_pixels(50)
	if not b'}' in headmsg_temp:
		while not b'}' in headmsg_temp:
			headmsg_temp += img.read_pixels(1)
	headmsg_seek = headmsg_temp.index(b'}')
	img.set_pixelseek((headmsg_seek + 1) * 2)
	headmsg_temp = headmsg_temp[:headmsg_seek+1]
	headmsg = eval(headmsg_temp)
	print(headmsg)
	file = SaveFile(headmsg['file name'])
	if created_file_path == '':
		file.filepath = file.filename
		file.creat_file()
	else:
		file.filepath =  os.path.join(file.filepath,file.filename)
		file.creat_file()
	file.filesize = int(headmsg['file size'])
	file.fileMD5 = headmsg['file MD5']
	file_size_quotients = file.filesize // 100
	file_size_remainder = file.filesize % 100
	if file_size_quotients > 0:
		for i in range(0,file_size_quotients):
			file_data = img.read_pixels(100)
			file.write_filedatas(file_data)
	file_data = img.read_pixels(file_size_remainder)
	file.write_filedatas(file_data)
	file_md5 = file.get_fileMD5()
	if file_md5 != file.fileMD5:  
		print('MD5 check failed , file is broken!')
		os.remove(file.filepath)
	
	
def test():
	"""测试函数用"""
	hide_file_to_image('hello.txt','1.jpg')
	read_file_from_image('hello.png')
	
if __name__ == '__main__':
	test()