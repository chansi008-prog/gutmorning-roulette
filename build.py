"""sian.html(아티팩트 시안) → index.html(설치형 앱). 시안을 고친 뒤 `python3 build.py` 실행."""
src = open("sian.html", encoding="utf-8").read()
end = src.index("</title>") + len("</title>")
title, rest = src[:end], src[end:]
s, e = rest.index("<style>"), rest.index("</style>") + len("</style>")
links, style, body = rest[:s], rest[s:e], rest[e:]
# 노치 있는 기기에서 위·아래 안전 영역 확보
style = style.replace("    padding-inline: 16px;\n", "    padding-inline: 16px;\n    padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px);\n", 1)
head = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
<meta name="description" content="2026 것모닝코리아 팀 챌린지 Dream US 시상 추첨">
<meta name="theme-color" content="#EEFBF1">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="것모닝 시상">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
{links.strip()}
{style}
</head>
<body>
"""
tail = """
<script>
if ("serviceWorker" in navigator) addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
</script>
</body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(head + body.strip() + "\n" + tail)
print("index.html built")
