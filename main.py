from urls import urls
from urlrouter import UnknowURL, MalformedURL

if __name__ == '__main__':
	while True:
		try:
			urls.run(str(input('>>> ')))
		except UnknowURL as msg:
			print('Error : {}'.format(msg))
		except MalformedURL as msg:
			print('Error : {}'.format(msg))
		except KeyboardInterrupt:
			break
		except EOFError:
			break
	print('\nBye !')