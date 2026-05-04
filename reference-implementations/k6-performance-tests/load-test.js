import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. Performance Quality Gate Configuration
export const options = {
    thresholds: {
        // Gate: 95% of requests must be under 200ms
        http_req_duration: ['p(95)<200'],
        // Gate: Error rate must be less than 1%
        http_req_failed: ['rate<0.01'],
    },
    stages: [
        { duration: '1m', target: 20 }, // Ramp up to 20 users
        { duration: '3m', target: 20 }, // Stay at 20 users
        { duration: '1m', target: 0 },  // Ramp down
    ],
};

export default function () {
    // 2. Test Execution
    const url = __ENV.TARGET_URL || 'https://example.com';
    const res = http.get(url);

    // 3. Assertions
    check(res, {
        'status is 200': (r) => r.status === 200,
        'transaction time < 500ms': (r) => r.timings.duration < 500,
    });

    sleep(1);
}
