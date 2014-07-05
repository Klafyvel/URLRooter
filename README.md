URLRooter
=========
(There is a nice misspelling in the name)

URLRooter is an exercise. The goal is to write a small program who can call the appropriate function when receiving a url.

About this implementation
-------------------------
The functions are in the `functions.py` file. The urls are registered into `urls.py`. `main.py` displays a prompt to test the urls. 

	$ python3 main.py
	>>> Green/Day/is/soooo/cool

You can give arguments to the functions :

	$ python3 main.py
	>>> new/hw:1/2/3

The function will receive this list : `['1','2','3']`

Create your url
---------------------

Just change the `urls.py` !

	from urlrouter import router
	import functions

	urls = router(
		{
			#Some urls ...
			'/useless/say' : functions.say,
		}
	)

The functions `say` has to be defined into `functions.py`. Example:

	def say(a):
		for i in a:
			print(i)

and...

	$ python3 main.py
	>>> useless/say:hey
	hey