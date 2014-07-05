from urlrouter import router
import functions

urls = router(
	{
		'/Green/Day/is/soooo/cool' : functions.Holliday,
		'/new/hw' : functions.hello_world,
		'/new/foo' : functions.foo,
	}
)