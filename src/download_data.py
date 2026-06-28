import ssl
import sys
import urllib.request

from src.utils.paths import DATA_RAW, ensure_dirs

BASE = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/"

FILES = {
    "DEMO_J.XPT": "DEMO_J.xpt",
    "BMX_J.XPT": "BMX_J.xpt",
    "DR1TOT_J.XPT": "DR1TOT_J.xpt",
    "SMQ_J.XPT": "SMQ_J.xpt",
    "BPX_J.XPT": "BPX_J.xpt",
    "ALQ_J.XPT": "ALQ_J.xpt",
    "HDL_J.XPT": "HDL_J.xpt",
    "GLU_J.XPT": "GLU_J.xpt",
}

XPORT_MAGIC = b"HEADER R"


def _context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def download():
    ensure_dirs()
    ctx = _context()
    ok, fail = [], []
    for local, remote in FILES.items():
        dst = DATA_RAW / local
        if dst.exists() and dst.stat().st_size > 50000:
            ok.append(local)
            continue
        url = BASE + remote
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
                data = resp.read()
            if data[:8] != XPORT_MAGIC:
                fail.append(local)
                continue
            dst.write_bytes(data)
            ok.append(local)
        except Exception:
            fail.append(local)
    return ok, fail


def main():
    ok, fail = download()
    print(f"Downloaded or cached: {len(ok)} files")
    if fail:
        print(f"Could not download: {fail}")
        print("Run src/make_offline_data.py to generate the reproducible fallback.")
        sys.exit(0)
    print("All NHANES 2017-2018 source files are available in data/raw.")


if __name__ == "__main__":
    main()
