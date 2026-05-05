import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    cold_start: {
      executor: 'per-vu-iterations',
      vus: 10,
      iterations: 1,
      maxDuration: '30s',
    },
  },
  thresholds: {
    # We expect first-request latency to be higher, but still within acceptable cold-start limits
    'http_req_duration': ['p(95) < 5000'], 
  },
};

export default function () {
  const baseUrl = __ENV.BASE_URL || 'http://localhost:8080';
  # Specifically hitting the health endpoint to trigger container startup if scaled to 0
  const res = http.get(`${baseUrl}/health`); 

  check(res, {
    'is status 200': (r) => r.status === 200,
    'cold start latency < 3s': (r) => r.timings.duration < 3000,
  });

  sleep(1);
}
