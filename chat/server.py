import aiohttp.web, aiohttp, aiokafka, asyncio, uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def websocket(app):
    app.setdefault('websocket', set())
    #consumer = aiokafka.AIOKafkaConsumer('topic', bootstrap_servers='kafka')
    #await consumer.start()
    #async for msg in consumer: print(msg.value, flush=True)
    #await consumer.stop()
    yield
    for _ in app.get('websocket'): await _.close()
    
async def chat(request):
    websocket = aiohttp.web.WebSocketResponse()
    await websocket.prepare(request)
    websocket.name = await websocket.receive_str()
    for _ in request.app.get('websocket'): await _.send_json({'join':'', 'name':websocket.name})
    request.app.get('websocket').add(websocket)
    async for message in websocket:
        if message.type == aiohttp.WSMsgType.TEXT:
            message = message.json()
            if '' in message:
                for _ in request.app.get('websocket'):
                    if _ is not websocket: await _.send_json({'':message.get(''), 'name':websocket.name})
            elif 'offer' in message:
                for _ in request.app.get('websocket'):
                    if _.name == message.get('name'): await _.send_json({'offer':message.get('offer'), 'name':websocket.name})
            elif 'answer' in message:
                for _ in request.app.get('websocket'):
                    if _.name == message.get('name'): await _.send_json({'answer':message.get('answer')})
            elif 'candidate' in message:
                for _ in request.app.get('websocket'):
                    if _.name == message.get('name'): await _.send_json({'candidate':message.get('candidate')})
        else: break
    request.app.get('websocket').discard(websocket)
    for _ in request.app.get('websocket'): await _.send_json({'disconnect':'', 'name':websocket.name})
    return websocket

app = aiohttp.web.Application()
app.add_routes([aiohttp.web.get('/ws', chat)])
app.cleanup_ctx.append(websocket)
aiohttp.web.run_app(app, port=80)
