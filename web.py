import aiohttp.web, aiohttp_cors, asyncpg, json, aredis, aiokafka, asyncio, uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def database(app):
    app.setdefault('database', await asyncpg.create_pool(host='postgres', user='postgres', database='postgres', password='postgres'))
    app.setdefault('cache', aredis.StrictRedis('redis').cache('cache'))
    #producer = aiokafka.AIOKafkaProducer(bootstrap_servers='kafka')
    #await producer.start()
    #await producer.send_and_wait('topic', b"Super message")
    #await producer.stop()
    yield
    await app.get('database').close()

async def post(request):
    body = await request.json()
    body = ' '.join(' '.join((key, str(value))) for key,value in body.items())
    records = await request.app.get('cache').get(body)
    if not records:
        async with request.app.get('database').acquire() as connection: records = json.dumps([*map(dict, await connection.fetch(f'select * from{body}'))], default=str)
        await request.app.get('cache').set(body, records)
    return aiohttp.web.Response(text=records)

app = aiohttp.web.Application()
app.add_routes([aiohttp.web.get('/', lambda _: aiohttp.web.HTTPFound('index.html')),
                aiohttp.web.post('/ajax', post)])
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)
app.cleanup_ctx.append(database)
aiohttp.web.run_app(app)
