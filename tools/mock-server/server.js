const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(json.dumps({ status: 'healthy', version: '1.0.0-mock' }));
  } else {
    res.writeHead(200);
    res.end('Mock Server Running');
  }
});

const PORT = 8080;
server.listen(PORT, () => {
  console.log(`QE Mock Server listening on port ${PORT}`);
});
