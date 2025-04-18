import socketio

# standard Python
sio = socketio.Client(logger=True, engineio_logger=True)
sio.connect('http://localhost:8848')

sio.emit('test', {'foo': 'bar'})

@sio.on('*')
def on_message(data):
    print('I received a message!')

print('my sid is', sio.sid)

print('my transport is', sio.transport)