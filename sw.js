const CACHE_NAME = 'hanja-v46';

// 설치 즉시 대기 건너뜀 → 새 SW가 바로 활성화
self.addEventListener('install', (e) => {
  self.skipWaiting();
});

// 활성화 시 이전 버전 캐시 모두 삭제 후 즉시 제어권 획득
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// 네트워크 우선: 온라인이면 항상 최신 버전, 오프라인이면 캐시 fallback
self.addEventListener('fetch', (e) => {
  // Firebase / 외부 API 요청은 SW가 개입하지 않음
  const url = new URL(e.request.url);
  if (url.hostname !== self.location.hostname) return;

  e.respondWith(
    fetch(e.request)
      .then(response => {
        // 성공 응답은 캐시에 저장
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        }
        return response;
      })
      .catch(() => caches.match(e.request))
  );
});
