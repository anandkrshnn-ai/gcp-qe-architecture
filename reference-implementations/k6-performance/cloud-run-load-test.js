import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '2m',  target: 100 },
    { duration: '1m',  target: 0 },
  ],
  thresholds: {
    'http_req_duration': ['p95 < 800'],
    'http_req_failed': ['rate < 0.01'],
  },
};

export default function () {
  const baseUrl = __ENV.BASE_URL || 'http://localhost:8080';
  const res = http.get(`${baseUrl}/health`); 

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 600ms': (r) => r.timings.duration < 600,
  });

  sleep(1);
}
