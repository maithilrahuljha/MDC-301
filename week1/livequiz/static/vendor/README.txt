The browser client is vendored so the classroom quiz does not depend on a CDN.

File: socket.io.min.js
Package: socket.io-client 4.8.1
Source: https://registry.npmjs.org/socket.io-client/-/socket.io-client-4.8.1.tgz
License: MIT; see SOCKET.IO-LICENSE.txt

Do not replace this with a remote script URL in the student/host pages. If the
version changes, verify it against the Flask-SocketIO / python-socketio server
versions and repeat the browser smoke test.
