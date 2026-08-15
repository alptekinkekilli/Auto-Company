---
description: Prod loop hold'unu kaldır (yalnız operatör-hold'u; latch'e dokunmaz)
---

Prod'daki Auto-Company loop hold'unu kaldır.

Adımlar:

1. `ssh powerupp-ts` ile container'ı bul (`z12a992i3ty202zezspij2fn` prefix'i).
2. ÖNCE hold'un KAYNAĞINI oku (`/api/status` → `hold`): cockpit/operatör hold'u mu, yoksa budget/loop LATCH'i mi?
   - **Budget-latch veya loop'un kendi koyduğu hold ise DUR** — sebebi raporla ve operatöre sor; onların pause'unu geri almak seninle aynı eylem değil.
   - Operatör hold'u ise devam et.
3. `docker exec -u app "$C" curl -s -X POST http://127.0.0.1:8787/api/hold/release`
4. Doğrula: `/api/status.hold` released; `logs/hold-audit.log` son satırı geçişi gösteriyor.
5. Hatırlat: release sonrası İLK cycle yine bir WATCH cycle'dır — uzun bir DELTA keşif izni değil, iş listesidir.

`logs/LOOP_HOLD` dosyasına asla doğrudan dokunma — yalnızca API.
