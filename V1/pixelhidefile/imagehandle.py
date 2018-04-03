# -*- coding: UTF-8 -*-

__author__ = 'Mr.Bluyee'

import os
import sys
from PIL import Image
from numpy import *
import struct


class HideImage(object):

	def __init__(self,image_path):
		"""类初始化
		Args:
			image_path: 包含具体文件名的路径(str)
		Raises:
			FileExistsError: 文件不存在错误
		"""	
		if os.path.exists(image_path)==False:
			raise FileExistsError('No exist image!')
		self.imm = Image.open(image_path).convert('RGBA')
		self.imagesize = self.imm.size
		self.imagewidth = self.imagesize[0]
		self.imageheight = self.imagesize[1]
		self.imagecapacity = self.imagewidth * self.imageheight * 4
		self.writedatalen =0
		self.imagearray = array(self.imm)
		self.imagearrayshape = self.imagearray.shape
		self.__pixelseek = 0
	
	def set_pixelseek(self,pixelseek):
		"""设置图片像素点游标
		Args:
			pixelseek: 像素点游标值(int)
		"""	
		self.__pixelseek = pixelseek
		
	def get_pixelseek(self):
		"""获取图片当前像素点游标
		Returns:
			self.__pixelseek: 像素点游标值(int)
		"""	
		return self.__pixelseek
	
	def is_even(self,num):
		"""判断数值是否为偶数
		Args:
			num: 数值(int)
		Returns:
			bool值
		"""
		if (num % 2) == 0:
			return True
		else:
			return False
		
	def odd_handle(self,im):
		"""对数值进行取奇数处理
		Args:
			im: 数值(int)
		Returns:
			处理后的数值(int)
		"""
		if self.is_even(im):
			return im + 1
		else:
			return im
	
	def even_handle(self,im):
		"""对数值进行取偶数处理
		Args:
			im: 数值(int)
		Returns:
			处理后的数值(int)
		"""
		if self.is_even(im):
			return im
		else:
			return im - 1
	
	def bytes2bin(self,datas):
		"""将字节流转为二进制数组
		Args:
			datas: bytes(list)
		Returns:
			data_bitlist: bool(list)
		"""
		data_bitlist = []
		data_len = len(datas)
		for i in range(0,data_len):
			for j in range(0,8):
				if datas[i] & (0x80 >> j):
					data_bitlist.append(True)
				else:
					data_bitlist.append(False)
		return data_bitlist
	
	def bin2bytes(self,bitlist):
		"""将二进制数组转为字节流
		Args:
			bitlist: bool(list)
		Returns:
			data_list: bytes(bytearray)
		"""
		data_list = []
		bit_length = len(bitlist)
		list_seek = 0
		if (bit_length % 8) == 0:
			bytes = bit_length // 8
		else:
			bytes = (bit_length // 8) + 1
		for i in range(0,bytes):
			data = 0
			for j in range(0,8):
				if list_seek > (bit_length - 1):
					return
				if bitlist[list_seek]:
					data |= (0x80 >> j)
				list_seek += 1
			data_list.append(data)
		return bytearray(data_list)
		
	def save_change(self,image_path):
		"""将修改后的像素数组转为图片
		Args:
			image_path: 要保存的具体文件名路径，无文件名后缀(str)
		"""
		new_image = Image.fromarray(self.imagearray)
		new_image.save(image_path + '.png')
		
	def read_pixels(self,datas_num):	
		"""读取像素点隐藏信息
		Args:
			datas_num: 要读取的bytes数据的个数(int)
		Returns:
			bytes: 从像素点中读出的数据bytes(bytearray)
		"""
		data_bitlist = []
		needed_lines = 0
		last_line_needed_pixels = 0
		data_bitlen = datas_num * 8
		needed_pixels = data_bitlen // 4
		img_xlen = self.__pixelseek // self.imagewidth  # 设定的游标对应的图像行数
		img_ylen = self.__pixelseek % self.imagewidth  # 设定的游标对应的图像列数
		if img_xlen > self.imageheight:  # 设定的游标超出图像尺寸
			print('seek over image size!')
			return		
		currentline_pixels_left = self.imagewidth - img_ylen  # 当前行剩余可读的像素点数
		if needed_pixels > currentline_pixels_left:
			needed_lines = (needed_pixels - currentline_pixels_left) // self.imagewidth  
			last_line_needed_pixels = (needed_pixels - currentline_pixels_left) % self.imagewidth
		if last_line_needed_pixels > 0:
			needed_lines += 1  # 除了当前行，还需要的行数
		if (img_xlen + needed_lines) > self.imageheight:
			print('reading datas over image size!')
			return
			
		if needed_pixels <= currentline_pixels_left:  # 要读的像素点数小于游标当前位置剩余像素点数
			for i in range(0,needed_pixels):
				for j in range(0,4):  # RGBA模式，一个像素点有4个通道
					if self.is_even(self.imagearray[img_xlen,img_ylen + i,j]):
						data_bitlist.append(False)
					else:
						data_bitlist.append(True)				
		else:
			for i in range(0,currentline_pixels_left):  # 先读出游标当前位置剩余像素点数的数据
				for j in range(0,4):
					if self.is_even(self.imagearray[img_xlen,img_ylen + i,j]):
						data_bitlist.append(False)
					else:
						data_bitlist.append(True)		
			if needed_lines - 1 > 0:
				for i in range(0,needed_lines - 1):  # 再整行读取除最后一行的像素点的数据
					for j in range(0,self.imagewidth):
						for k in range(0,4):
							if self.is_even(self.imagearray[img_xlen + 1 + i,j,k]):
								data_bitlist.append(False)
							else:
								data_bitlist.append(True)
			for i in range(0,last_line_needed_pixels):  # 读取最后剩余的非整行的像素的数据
				for j in range(0,4):		
					if self.is_even(self.imagearray[img_xlen + needed_lines,i,j]):
						data_bitlist.append(False)
					else:
						data_bitlist.append(True)
		bytes = self.bin2bytes(data_bitlist)
		self.__pixelseek += needed_pixels
		return 	bytes	
	
	def write_pixels(self,datas):
		"""读取像素点隐藏信息
		Args:
			datas_num: 要读取的bytes数据的个数(int)
		Returns:
			bytes: 从像素点中读出的数据bytes(bytearray)
		"""
		if isinstance(datas,str):
			datas = datas.encode('utf-8')
		databit_seek = 0
		needed_lines = 0
		last_line_needed_pixels = 0
		data_len = len(datas)
		data_bitlist = self.bytes2bin(datas)
		data_bitlen = data_len * 8	
		needed_pixels = data_bitlen // 4
		img_xlen = self.__pixelseek // self.imagewidth  # 设定的游标对应的图像行数
		img_ylen = self.__pixelseek % self.imagewidth  # 设定的游标对应的图像列数
		if img_xlen > self.imageheight:  # 设定的游标超出图像尺寸
			print('seek over image size!')
			return		
		currentline_pixels_left = self.imagewidth - img_ylen  # 当前行剩余可写的像素点数
		if needed_pixels > currentline_pixels_left:
			needed_lines = (needed_pixels - currentline_pixels_left) // self.imagewidth  
			last_line_needed_pixels = (needed_pixels - currentline_pixels_left) % self.imagewidth
		if last_line_needed_pixels > 0:
			needed_lines += 1  # 除了当前行，还需要的行数
		if (img_xlen + needed_lines) > self.imageheight:
			print('writing datas over image size!')
			return
			
		if needed_pixels <= currentline_pixels_left:
			for i in range(0,needed_pixels):
				for j in range(0,4):
					if data_bitlist[databit_seek]:
						self.imagearray[img_xlen,img_ylen + i,j] = self.odd_handle(self.imagearray[img_xlen,img_ylen + i,j])
					else:
						self.imagearray[img_xlen,img_ylen + i,j] = self.even_handle(self.imagearray[img_xlen,img_ylen + i,j])
					databit_seek += 1
		else:
			for i in range(0,currentline_pixels_left):
				for j in range(0,4):
					if data_bitlist[databit_seek]:
						self.imagearray[img_xlen,img_ylen + i,j] = self.odd_handle(self.imagearray[img_xlen,img_ylen + i,j])
					else:
						self.imagearray[img_xlen,img_ylen + i,j] = self.even_handle(self.imagearray[img_xlen,img_ylen + i,j])
					databit_seek += 1
			if needed_lines - 1 > 0:
				for i in range(0,needed_lines - 1):
					for j in range(0,self.imagewidth):
						for k in range(0,4):
							if data_bitlist[databit_seek]:
								self.imagearray[img_xlen + 1 + i,j,k] = self.odd_handle(self.imagearray[img_xlen + 1 + i,j,k])
							else:
								self.imagearray[img_xlen + 1 + i,j,k] = self.even_handle(self.imagearray[img_xlen + 1 + i,j,k])
							databit_seek += 1	
			for i in range(0,last_line_needed_pixels):
				for j in range(0,4):
					if data_bitlist[databit_seek]:
						self.imagearray[img_xlen + needed_lines,i,j] = self.odd_handle(self.imagearray[img_xlen + needed_lines,i,j])
					else:
						self.imagearray[img_xlen + needed_lines,i,j] = self.even_handle(self.imagearray[img_xlen + needed_lines,i,j])
					databit_seek += 1				
		self.__pixelseek += needed_pixels

		
def test(imagefilename):
	"""测试方法用"""
	root_dir = os.getcwd()
	image_path = os.path.join(root_dir,imagefilename)
	createfilename = os.path.splitext(image_path)[0]
	im1 = HideImage(image_path)
	im1.set_pixelseek(0)
	#datas = [0x12,0x13,0x14]
	#datas = 'hello world!'
	datas = '你好!'
	im1.write_pixels(datas)
	im1.save_change(createfilename)
	
	im2 = HideImage(createfilename+'.png')
	im2.set_pixelseek(0)
	bytes = im2.read_pixels(len(datas.encode('utf-8')))
	print(bytes.decode('utf-8'))
	
if __name__ == '__main__':
	test('1.jpg')