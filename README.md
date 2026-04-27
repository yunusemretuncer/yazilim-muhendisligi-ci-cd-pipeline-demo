# DevSecOps Demo — Shift-Left Security Pipeline

Sunum için minimal demo. Dört aşamalı GitHub Actions pipeline'ı:

```
[Secret Scan] → [SAST] → [Dependency Scan] → [Build + Container Scan + Push]
   gitleaks      bandit       pip-audit              Trivy → GHCR
```

Üç güvenlik kapısı (gate) geçilmeden image GHCR'a push edilmez.

## Bilerek Eklenmiş 3 Zafiyet

| # | Tür                  | Nerede             | Hangi Tool Yakalar |
| - | -------------------- | ------------------ | ------------------ |
| 1 | Hardcoded AWS key    | `app.py`           | gitleaks           |
| 2 | SQL Injection (B608) | `app.py:get_user`  | bandit             |
| 3 | Vulnerable Flask 2.0.1 | `requirements.txt` | pip-audit / Trivy |

## Demo Akışı (2 dakika)

1. **Pipeline'ı tetikle** — repo'ya bu haliyle push at, üç job da kırmızıya düşer. GitHub Actions ekranında her aşamanın *hangi* zafiyeti hangi satırda yakaladığını göster.
2. **Fix commit** — aşağıdaki üç değişikliği yap, yeniden push at:
   - `app.py`'deki `AWS_ACCESS_KEY` ve `AWS_SECRET_KEY` satırlarını sil (`os.environ.get(...)` ile değiştir)
   - SQL sorgusunu parametreli yap: `cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))`
   - `requirements.txt`'i güncelle: `Flask>=3.0.0`, `Werkzeug>=3.0.0`
3. **Pipeline yeşile döner**, image GHCR'a push edilir.

## Sunumda Vurgu

- **Shift-left**: Güvenlik production'a değil, geliştirme sürecinin başına çekildi
- Her gate **bağımsız** çalışır (`jobs:` paralel) → hızlı feedback
- `needs: [secrets, sast, deps]` ile build aşaması üç kontrole de bağımlı → fail-fast
- Tek bir `.github/workflows/security.yml` dosyası, ekstra altyapı yok

## Yerel Test (opsiyonel)

```bash
pip install bandit pip-audit
bandit -r . -ll
pip-audit -r requirements.txt
```
