#!/usr/bin/env python3
"""
Bot Auto-Post Epos Sureq Galigo ke Threads dengan Gemini API dan Human Jitter.
Dibuat dengan kepatuhan antislop: narasi bertenaga, bebas em-dash, dan jadwal natural.
"""

import argparse
import datetime
import json
import logging
import os
import random
import sys
import time
from typing import Dict, List, Optional
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("GaligoBot")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EPISODES_FILE = os.path.join(BASE_DIR, "episodes.json")
STATE_FILE = os.path.join(BASE_DIR, "state.json")

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Gagal membaca state.json: {e}. Menggunakan state awal.")
    return {"current_episode_id": 1, "last_posted_at": None, "history": []}

def save_state(state: dict) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    logger.info("State berhasil diperbarui di state.json")

def load_episodes() -> List[dict]:
    if not os.path.exists(EPISODES_FILE):
        logger.error(f"File {EPISODES_FILE} tidak ditemukan.")
        return []
    with open(EPISODES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_episodes(episodes: List[dict]) -> None:
    with open(EPISODES_FILE, "w", encoding="utf-8") as f:
        json.dump(episodes, f, indent=2, ensure_ascii=False)

def apply_human_jitter(skip: bool = False) -> None:
    """
    Menunda eksekusi antara 0 hingga 9 menit (0-540 detik)
    agar jam posting di Threads bervariasi alami dan tidak terdeteksi bot.
    """
    if skip or os.getenv("SKIP_JITTER", "false").lower() in ("true", "1", "yes"):
        logger.info("[JITTER] Dilewati (mode testing / skip_jitter aktif).")
        return

    delay_seconds = random.randint(0, 540)
    delay_minutes = delay_seconds / 60.0
    logger.info(
        f"[JITTER] Menunda pengiriman selama {delay_seconds} detik ({delay_minutes:.2f} menit) "
        "agar pola waktu posting terlihat natural..."
    )
    time.sleep(delay_seconds)
    logger.info("[JITTER] Selesai menunggu, memulai proses posting.")

def clean_and_verify_part(text: str, part_num: int, max_chars: int = 450) -> str:
    # Standar antislop R-02: ganti tanda em-dash dengan tanda baca yang wajar
    cleaned = text.replace("—", ", ").replace("--", ", ")
    cleaned = " ".join(cleaned.split())

    char_len = len(cleaned)
    if char_len > max_chars:
        logger.warning(f"Part {part_num} melebihi batas {max_chars} karakter ({char_len} karakter). Memotong...")
        cleaned = cleaned[:max_chars - 3] + "..."
    return cleaned

def generate_next_episode_with_gemini(episode_id: int, api_key: str) -> Optional[dict]:
    """
    Menghasilkan episode baru Sureq Galigo menggunakan Gemini API
    jika persediaan episode statis telah habis.
    """
    logger.info(f"Menghubungi Gemini API untuk menulis naskah Sureq Galigo Episode {episode_id}...")
    prompt = f"""Kamu adalah sejarawan dan budayawan Bugis-Makassar serta penutur kisah Sureq Galigo yang ulung.
Tuliskan 1 episode kelanjutan epos Sureq Galigo (Episode {episode_id}) yang dramatis, mendebarkan, dan memancing rasa penasaran.

Aturan ketat penulisan:
1. Bagi cerita menjadi tepat 8 atau 9 bagian (parts).
2. Part 1: Hook pembuka di Threads yang sangat memikat, dan akhiri dengan indikasi lanjut di bawah: [Lanjut di bawah]👇
3. Part 2 s/d Part 7/8: Kisah berurutan yang hidup dan berwibawa.
4. Part terakhir: Climax/resolusi episode serta pertanyaan pancingan (Call to Action) agar pembaca berkomentar.
5. Batas karakter: Setiap part WAJIB maksimal 420 karakter (kurang dari 450 karakter).
6. DILARANG menggunakan tanda em dash (— atau --). Gunakan koma, titik, atau tanda kurung.
7. Hindari kata-kata klise AI marketing. Gunakan istilah budaya Bugis yang tepat (misal: Sompe, Bissu, Dewata, Luwu).

Keluarkan HANYA format JSON valid berikut:
{{
  "id": {episode_id},
  "title": "Judul Episode",
  "parts": [
    "Teks Part 1...",
    "Teks Part 2..."
  ]
}}
"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "response_mime_type": "application/json"
            }
        }
        res = requests.post(url, json=payload, timeout=60)
        res.raise_for_status()
        data = res.json()
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(raw_text)

        cleaned_parts = [
            clean_and_verify_part(p, i + 1)
            for i, p in enumerate(parsed.get("parts", []))
        ]
        parsed["parts"] = cleaned_parts
        return parsed
    except Exception as e:
        logger.error(f"Gagal generate episode via Gemini API: {e}")
        return None

class ThreadsPoster:
    def __init__(self, user_id: str, access_token: str, dry_run: bool = False):
        self.user_id = user_id
        self.access_token = access_token
        self.dry_run = dry_run
        self.base_url = "https://graph.threads.net/v1.0"

    def create_text_container(self, text: str, reply_to_id: Optional[str] = None) -> Optional[str]:
        if self.dry_run:
            fake_id = f"mock_container_{int(time.time() * 1000)}"
            logger.info(f"[DRY-RUN] Buat container (reply_to={reply_to_id}): {text[:60]}... -> {fake_id}")
            return fake_id

        url = f"{self.base_url}/{self.user_id}/threads"
        payload = {
            "media_type": "TEXT",
            "text": text,
            "access_token": self.access_token
        }
        if reply_to_id:
            payload["reply_to_id"] = reply_to_id

        resp = requests.post(url, data=payload, timeout=30)
        if not resp.ok:
            logger.error(f"Gagal membuat container Threads: {resp.text}")
            return None
        return resp.json().get("id")

    def publish_container(self, creation_id: str) -> Optional[str]:
        if self.dry_run:
            fake_post_id = f"mock_post_{int(time.time() * 1000)}"
            logger.info(f"[DRY-RUN] Publish container {creation_id} -> post_id: {fake_post_id}")
            return fake_post_id

        url = f"{self.base_url}/{self.user_id}/threads_publish"
        payload = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        resp = requests.post(url, data=payload, timeout=30)
        if not resp.ok:
            logger.error(f"Gagal mempublikasikan container Threads: {resp.text}")
            return None
        return resp.json().get("id")

    def post_thread_series(self, parts: List[str]) -> List[str]:
        """
        Memposting rangkaian thread berurutan:
        Part 1 diunggah sebagai post utama, lalu Part 2 s/d Part N diunggah
        berurutan sebagai reply berantai di bawah post sebelumnya.
        """
        post_ids = []
        parent_id = None

        for idx, part_text in enumerate(parts, 1):
            logger.info(f"Memproses Part {idx}/{len(parts)} ({len(part_text)} karakter)...")
            container_id = self.create_text_container(part_text, reply_to_id=parent_id)
            if not container_id:
                logger.error(f"Gagal membuat container untuk Part {idx}. Berhenti.")
                break

            time.sleep(2)
            published_id = self.publish_container(container_id)
            if not published_id:
                logger.error(f"Gagal mempublikasikan Part {idx}. Berhenti.")
                break

            post_ids.append(published_id)
            parent_id = published_id
            logger.info(f"Part {idx} terbit sukses: {published_id}")

            # Jeda sopan antar bagian agar Threads API memproses rantai komentar
            if idx < len(parts):
                wait_between = 5 if not self.dry_run else 1
                time.sleep(wait_between)

        return post_ids

def main():
    parser = argparse.ArgumentParser(description="Bot Auto-Post Sureq Galigo Threads")
    parser.add_argument("--dry-run", action="store_true", help="Uji coba tanpa posting ke Threads")
    parser.add_argument("--no-jitter", action="store_true", help="Lewati penundaan waktu acak (jitter)")
    parser.add_argument("--force-episode", type=int, help="Paksa nomor episode tertentu")
    args = parser.parse_args()

    state = load_state()
    episodes = load_episodes()

    target_episode_id = args.force_episode or state.get("current_episode_id", 1)
    logger.info(f"Target Episode: {target_episode_id}")

    # Cari episode di penyimpanan lokal
    current_episode = next((ep for ep in episodes if ep.get("id") == target_episode_id), None)

    # Jika episode belum tersedia di lokal, gunakan Gemini API jika tersedia key
    if not current_episode:
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            current_episode = generate_next_episode_with_gemini(target_episode_id, gemini_key)
            if current_episode:
                episodes.append(current_episode)
                save_episodes(episodes)
        else:
            logger.error(
                f"Episode {target_episode_id} tidak ditemukan di episodes.json dan GEMINI_API_KEY tidak disetel."
            )
            sys.exit(1)

    parts = current_episode.get("parts", [])
    if not parts or len(parts) < 8 or len(parts) > 9:
        logger.error(f"Episode {target_episode_id} memiliki {len(parts)} bagian. Syarat: 8 hingga 9 parts.")
        sys.exit(1)

    # Validasi karakter dan antislop
    cleaned_parts = [clean_and_verify_part(p, i + 1) for i, p in enumerate(parts)]
    for idx, p in enumerate(cleaned_parts, 1):
        logger.info(f"Preview Part {idx} [{len(p)} char]: {p[:70]}...")

    # Human Jitter (penundaan acak 0-9 menit)
    apply_human_jitter(skip=args.no_jitter)

    threads_user_id = os.getenv("THREADS_USER_ID", "")
    threads_token = os.getenv("THREADS_ACCESS_TOKEN", "")

    dry_run = args.dry_run or (not threads_user_id or not threads_token)
    if dry_run and not args.dry_run:
        logger.warning("Kredensial Threads API belum lengkap. Otomatis beralih ke mode DRY-RUN simulasi.")

    poster = ThreadsPoster(user_id=threads_user_id, access_token=threads_token, dry_run=dry_run)
    post_ids = poster.post_thread_series(cleaned_parts)

    if len(post_ids) == len(cleaned_parts):
        logger.info(f"Episode {target_episode_id} ('{current_episode.get('title')}') berhasil diposting!")
        if not dry_run or args.force_episode is None:
            state["current_episode_id"] = target_episode_id + 1
            state["last_posted_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            state["history"].append({
                "episode_id": target_episode_id,
                "title": current_episode.get("title"),
                "parts_count": len(cleaned_parts),
                "root_post_id": post_ids[0] if post_ids else None,
                "posted_at": state["last_posted_at"],
                "mode": "live" if not dry_run else "dry-run"
            })
            save_state(state)
            logger.info(f"Urutan episode berikutnya adalah Episode {state['current_episode_id']}")
    else:
        logger.error("Terjadi kegagalan posting sebagian rantai thread.")
        sys.exit(1)

if __name__ == "__main__":
    main()
