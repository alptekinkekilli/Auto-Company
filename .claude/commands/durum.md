---
description: Şirket durumu — repo, prod loop, bütçe, direktif, OPREQ tek bakışta
---

Şirketin anlık durumunu ölç ve raporla (İDDİA değil ÖLÇÜM — hafızadan değil sistemlerden):

1. `python3 scripts/session-brief.py` — repo/prod senkron, hold, cockpit, direktif, OPREQ sayısı.
2. `ssh powerupp-ts` üzerinden container'da:
   - `tail -n 15 /app/logs/auto-loop.log` — loop ne yapıyor ([OFF-HOURS] / cycle / IDLE-SKIP)?
   - Son `[BUDGET]` satırı — Daily/Weekly TOTAL doluluk.
   - `grep -c "Status: OPEN" /app/memories/operator-requests.md` — açık OPREQ.
3. Kısa tablo halinde sun: repo · prod · loop durumu · bütçe · direktif · açık OPREQ · dikkat gerektiren şey (varsa).

Kurallar: sayıları özetlerden/hafızadan TAŞIMA, bu turda ölç. Saatleri UTC etiketiyle ver (Mac yerel saati UTC+3, karıştırma).
