# Bugs — mlpartnersllc.com

## 2026-06-23 — Encrypted upload returned HTTP 405 (shared :8082 backend) — FIXED

**Symptom:** POST /upload-encrypted-raw returned 405 on mlpartnersllc.com AND mlpartnership.com; uploads (e.g. "intern Resource.zip.age") failed.

**Root cause:** :8082 was held by an older deployed server (`mlp-upload.service` → /usr/share/nginx/mlpartnership-html/upload-server.js) that only routes `/upload`. The newer build with `/upload-encrypted` + `/upload-encrypted-raw` (`upload-server.service`, runs repo upload-server.js) couldn't bind the port and was crash-looping (~194k restarts).

**Fix:** Backed up the deployed file to /mnt/ssd/backup/, overwrote it with the repo superset build, restarted `mlp-upload.service`, and disabled `upload-server.service`. Endpoint now returns 401 for bad token (auth reached) instead of 405. Real upload requires the correct token (sha256 at /etc/upload-server/token.sha256).
