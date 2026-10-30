#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把排版好的 HTML 推到公众号草稿箱。

和只传封面的脚本不同，这里先把正文里的本地图片上传到微信图床，
拿回 mmbiz 的 URL 替换掉本地路径，否则草稿里的图片全是裂的。

环境变量
  WECHAT_APPID   公众号 AppID
  WECHAT_SECRET  公众号 AppSecret（不要写进任何文件）
  WECHAT_AUTHOR  署名，默认 李亚威

用法
  python push_draft.py --html a.html --title "短标题" --digest "摘要" --cover cover.png
  python push_draft.py --html a.html --title "短标题" --dry-run
"""
import argparse
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
import uuid

API = "https://api.weixin.qq.com/cgi-bin"
DEFAULT_AUTHOR = "李亚威"
IMG_SRC_RE = re.compile(r'(<img[^>]+src=["\'])([^"\']+)(["\'])', re.I)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def http_json(url, data=None, headers=None):
    kw = {"url": url, "data": data, "headers": headers or {}}
    req = urllib.request.Request(**kw)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "ignore")
        try:
            return json.loads(raw)
        except Exception:
            return {"errcode": -1, "errmsg": raw or str(e)}


def build_multipart(field, path):
    boundary = "----WxBoundary" + uuid.uuid4().hex
    fn = os.path.basename(path)
    ctype = mimetypes.guess_type(fn)[0] or "image/png"
    with open(path, "rb") as f:
        body = f.read()
    payload = b""
    payload += ("--%s\r\n" % boundary).encode()
    payload += (
        'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (field, fn)
    ).encode()
    payload += ("Content-Type: %s\r\n\r\n" % ctype).encode()
    payload += body + b"\r\n"
    payload += ("--%s--\r\n" % boundary).encode()
    return payload, "multipart/form-data; boundary=%s" % boundary


def get_token(appid, secret):
    return http_json(
        "%s/token?grant_type=client_credential&appid=%s&secret=%s" % (API, appid, secret)
    )


def upload_content_image(token, path):
    """上传正文图片，返回可在正文里直接引用的 URL。"""
    payload, ctype = build_multipart("media", path)
    return http_json(
        "%s/media/uploadimg?access_token=%s" % (API, token),
        data=payload,
        headers={"Content-Type": ctype},
    )


def upload_cover(token, path):
    """上传封面为永久素材，返回 thumb_media_id。"""
    payload, ctype = build_multipart("media", path)
    return http_json(
        "%s/material/add_material?access_token=%s&type=image" % (API, token),
        data=payload,
        headers={"Content-Type": ctype},
    )


def create_draft(token, article):
    body = json.dumps({"articles": [article]}, ensure_ascii=False).encode("utf-8")
    return http_json(
        "%s/draft/add?access_token=%s" % (API, token),
        data=body,
        headers={"Content-Type": "application/json"},
    )


def is_local(src):
    return not src.lower().startswith(("http://", "https://", "data:", "//"))


def replace_images(html, base_dir, token):
    """把正文里的本地图片换成微信图床 URL。"""
    replaced, failed = 0, []

    def _sub(m):
        nonlocal replaced
        src = m.group(2)
        if not is_local(src):
            return m.group(0)
        local = src if os.path.isabs(src) else os.path.join(base_dir, src)
        local = os.path.normpath(local)
        if not os.path.exists(local):
            failed.append((src, "文件不存在"))
            return m.group(0)
        res = upload_content_image(token, local)
        if "url" in res:
            replaced += 1
            return m.group(1) + res["url"] + m.group(3)
        failed.append((src, json.dumps(res, ensure_ascii=False)))
        return m.group(0)

    new_html = IMG_SRC_RE.sub(_sub, html)
    return new_html, replaced, failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--digest", default="")
    ap.add_argument("--cover", default="")
    ap.add_argument("--author", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    html_path = os.path.abspath(args.html)
    if not os.path.exists(html_path):
        print("ERR: HTML 不存在 %s" % html_path)
        sys.exit(1)

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    title_bytes = len(args.title.encode("utf-8"))
    if title_bytes > 64:
        print("WARN: 标题 %d 字节，超过微信 64 字节上限，建议缩短" % title_bytes)
    if len(args.digest) > 120:
        print("WARN: 摘要 %d 字，超过 120，会被截断" % len(args.digest))

    appid = os.environ.get("WECHAT_APPID")
    secret = os.environ.get("WECHAT_SECRET")
    if not appid or not secret:
        print("ERR: 未设置 WECHAT_APPID / WECHAT_SECRET")
        sys.exit(1)

    tok = get_token(appid, secret)
    if "access_token" not in tok:
        print("ERR get_token: %s" % json.dumps(tok, ensure_ascii=False))
        sys.exit(1)
    token = tok["access_token"]
    print("TOKEN ok, expires_in: %s" % tok.get("expires_in"))

    new_html, replaced, failed = replace_images(html, os.path.dirname(html_path), token)
    print("正文图片替换: 成功 %d 张, 失败 %d 张" % (replaced, len(failed)))
    for src, why in failed:
        print("  FAIL %s -> %s" % (src, why))

    out_path = args.out or (os.path.splitext(html_path)[0] + "_微信版.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("已写出: %s" % out_path)

    if args.dry_run:
        print("DRY_RUN 结束，未建草稿")
        return

    thumb = ""
    if args.cover:
        cover = os.path.abspath(args.cover)
        up = upload_cover(token, cover)
        if "media_id" in up:
            thumb = up["media_id"]
            print("封面 media_id: %s" % thumb)
        else:
            print("WARN 封面上传: %s" % json.dumps(up, ensure_ascii=False))

    article = {
        "title": args.title,
        "author": args.author or os.environ.get("WECHAT_AUTHOR") or DEFAULT_AUTHOR,
        "digest": args.digest,
        "content": new_html,
        "thumb_media_id": thumb,
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }
    res = create_draft(token, article)
    if "media_id" in res:
        print("DRAFT_OK media_id: %s" % res["media_id"])
    else:
        print("ERR create_draft: %s" % json.dumps(res, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
