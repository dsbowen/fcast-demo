import survey
from fcast_app import create_fcast_app

from hemlock import create_app

app = create_app()
create_fcast_app(app, src='/fcast/')
create_fcast_app(app, src='/fcast-instr/', instructions=True)

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)