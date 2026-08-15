---
description: Prod loop'u mekanik hold'a al (LOOP_HOLD) ve doğrula
argument-hint: [sebep]
---

Prod'daki Auto-Company loop'unu hold'a al. Sebep: $ARGUMENTS (boşsa "operator hold — interactive session" kullan).

Adımlar:

1. `ssh powerupp-ts` ile container'ı bul:
   `C=$(docker ps --filter "name=z12a992i3ty202zezspij2fn" --format "{{.Names}}" | head -1)`
2. Cockpit'e container İÇİNDEN POST at (port 8787 dışa açık değil):
   `docker exec -u app "$C" curl -s -X POST http://127.0.0.1:8787/api/hold -H "Content-Type: application/json" -d '{"reason":"<sebep>"}'`
3. Doğrula: `/api/status` çıktısındaki `hold` alanını oku ve `logs/hold-audit.log` son satırını göster.
4. Tek satırda raporla: HELD + sebep + UTC saat + hangi container.

Kurallar:
- `logs/LOOP_HOLD` dosyasına ASLA doğrudan yazma — yalnızca API üzerinden.
- Zaten hold'daysa (özellikle budget-latch kaynaklıysa) üstüne yazma; mevcut hold'un kaynağını ve sebebini raporla, dur.
