# -*- coding: UTF-8 -*-

__author__ = 'Mr.Bluyee'

from pixelhidefile import pixelhide


def main():
	pixelhide.hide_file_to_image('hello.txt','1.jpg')
	pixelhide.read_file_from_image('hello.png')
	
if __name__ == '__main__':
	main()