import asyncio
import amino
client = amino.AsyncClient()

async def login_acc():
	try:
		await client.login(email=input("email: "),password=input("password: "))
	except Exception as e:
		print(e)
		await login_acc()

async def choose():
	global chatId
	global sub_client
	communities = await client.sub_clients(start=0,size=100)
	for x, name in enumerate(communities.name, 1):
		print(f"{x}.{name}")
	comId = communities.comId[int(input("choose the number of community: "))-1]
	sub_client = amino.AsyncSubClient(comId=comId,profile=client.profile)
	threads = await sub_client.get_chat_threads(start=0,size=100)
	for i, name in enumerate(threads.title, 1):
		print(f"{i}.{name}")
	chatId = threads.chatId[int(input("choose the chat: "))-1]

async def invite(id):
	try:
		await sub_client.invite_to_chat(chatId=chatId, userId = id)
		print(f"{id} invited to chat")
	except:
		pass

async def main():
	await login_acc()
	await choose()
	while True:
		for i in range(0,10000,100):
			users = (await sub_client.get_online_users(start=i, size=100)).profile
			if not users:
				break
			asyncio.gather(*[asyncio.create_task(invite(id=userId)) for userId in users.userId])

asyncio.get_event_loop().run_until_complete(main())