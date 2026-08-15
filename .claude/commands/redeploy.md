---
description: Güvenli prod redeploy runbook'u (hold → deploy → doğrula → release)
argument-hint: [beklenen commit hash]
---

Auto-Company prod'unu güvenli sırayla redeploy et. Beklenen commit: $ARGUMENTS (boşsa `git log --oneline -1` HEAD'i).

Sıra ÖNEMLİ — atlamak yok:

1. **Preflight:** `git status` temiz mi, HEAD push'lanmış mı (`git status -sb` → origin-eşit)? Değilse dur, önce push.
2. **Hold:** `/hold` akışıyla loop'u hold'a al (redeploy sebebiyle). Yeni container boot'tan saniyeler sonra cycle başlatır; hold persistent volume'da olduğundan yeni container da HELD boot eder — deploy sonrası sakinlik penceresi YOKTUR, tek güvenli yol budur.
3. **Tetikle:**
   ```
   T=$(security find-generic-password -w -a "$(whoami)" -s autocompany-coolify-deploy)
   curl -s -X POST -H "Authorization: Bearer $T" -H "User-Agent: Mozilla/5.0" \
     "https://app.coolify.io/api/v1/deploy?uuid=z12a992i3ty202zezspij2fn"
   ```
   `User-Agent: Mozilla/5.0` zorunlu (Cloudflare 1010).
4. **Bekle:** dakikalar sürebilir. YENİ container adı hash'i görünene kadar `docker ps`'i yokla — "Up" durumu tek başına kanıt değil.
5. **"Committed ≠ deployed" doğrulaması:** container içinde beklenen commit'e ÖZGÜ bir string'i grep'le (örn. o commit'in eklediği bir fonksiyon adı). `git log` + deploy kaydından varsayma.
6. **Held-boot doğrula:** `auto-loop.log`'da `[LOOP-HOLD] Boot under mechanical hold` satırı; sıfır model çağrısı.
7. **Testler:** değişikliğe dokunan `tests/test_*.sh` dosyalarını container İÇİNDE çalıştır, yeşil gör.
8. **Release:** `/release` akışıyla hold'u kaldır; loop'un temiz devam ettiğini (`[OFF-HOURS]` veya normal cycle) logdan teyit et.
9. Özet raporla: eski→yeni container, doğrulanan commit, koşulan testler, hold release saati (UTC).
