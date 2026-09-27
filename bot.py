#!/usr/bin/env python3
"""
Bot Auto-Post Serial Epos Sureq Galigo dan Sejarah Budaya Nusantara ke Threads.
Didesain untuk beroperasi tanpa batas waktu (tidak pernah kehabisan ide konten),
didukung integrasi Gemini API, human jitter 0-9 menit, jadwal 3 kali sehari,
dan kepatuhan antislop ketat (bebas em-dash).
"""

import argparse
import datetime
import json
import logging
import os
import random
import sys
import time
from typing import Dict, List, Optional, Tuple
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
IMAGES_DIR = os.path.join(BASE_DIR, "images")

def get_content_era(episode_id: int) -> Tuple[str, str, bool]:
    """
    Menentukan era, tema narasi, dan apakah episode merupakan awal babak baru.
    Mendukung penyiaran kontinu tanpa batas:
    - Episode 1 s/d 300: 12 Jilid Lengkap Epos Sureq Galigo
    - Episode 301 s/d 500: Kronik Lontaraq Kerajaan Bugis-Makassar (To Manurung, Luwu, Bone, Gowa)
    - Episode 501 s/d 700: Falsafah Luhur Siriq na Pesse, Hukum Laut Amanna Gappa, dan Tradisi Bissu
    - Episode 701 s/d seterusnya: Sudut Pandang Alternatif Tokoh dan Legenda Maritim Nusantara
    """
    # Era 1: 12 Jilid Naskah Asli Sureq Galigo (Episode 1 - 300)
    if episode_id <= 300:
        jilid_map = {
            1: ("Jilid 1: Zaman Purba dan Turunnya Batara Guru ke Luwu", 1, 25),
            2: ("Jilid 2: Masa Keemasan Batara Lattuq dan Kelahiran Kembar Emas", 26, 50),
            3: ("Jilid 3: Masa Remaja Sawerigading dan Pendidikan Ksatria", 51, 75),
            4: ("Jilid 4: Pertemuan Terlarang dan Goncangan Kosmis Luwu", 76, 100),
            5: ("Jilid 5: Pohon Keramat Welenrengnge dan Amukan Garuda", 101, 125),
            6: ("Jilid 6: Pembuatan Bahtera Wakka Pasompe dan Sumpah Sawerigading", 126, 150),
            7: ("Jilid 7: Pelayaran Akbar Mengarungi Lautan Nusantara", 151, 175),
            8: ("Jilid 8: Pendaratan di Tana Kelling dan Perang Penaklukan", 176, 200),
            9: ("Jilid 9: Meluluhkan Hati Putri We Cudai dan Pernikahan Akbar", 201, 225),
            10: ("Jilid 10: Lahirnya I La Galigo dan Petualangan Masa Mudanya", 226, 250),
            11: ("Jilid 11: Pelayaran I La Galigo dan Munculnya Generasi Ketiga", 251, 275),
            12: ("Jilid 12: Kepulangan Terakhir, Tenggelamnya Bahtera dan Pamitnya Dewata", 276, 300),
        }
        for j_num, (j_title, start_ep, end_ep) in jilid_map.items():
            if start_ep <= episode_id <= end_ep:
                is_start = (episode_id == start_ep)
                return f"Era 1: Epos Sureq Galigo", f"{j_title}", is_start

    # Era 2: Kronik Sejarah Lontaraq Kerajaan Nusantara (Episode 301 - 500)
    elif 301 <= episode_id <= 500:
        sub_era = ((episode_id - 301) // 50) + 1
        era_titles = {
            1: "Zaman Sianre Bale dan Turunnya To Manurung Penegak Keadilan",
            2: "Kejayaan Kerajaan Bone, Bendera Samparaja dan Arung Palakka",
            3: "Kemaharajaan Maritim Gowa-Tallo dan Sultan Hasanuddin",
            4: "Kearifan Demokrasi Tanah Wajo dan Tokoh Cendekiawan Bugis"
        }
        title = era_titles.get(sub_era, "Kronik Lontaraq Kerajaan Nusantara")
        is_start = ((episode_id - 301) % 50 == 0)
        return "Era 2: Kronik Sejarah Lontaraq", title, is_start

    # Era 3: Falsafah Hidup, Maritim Pinisi, dan Kearifan Bissu (Episode 501 - 700)
    elif 501 <= episode_id <= 700:
        sub_era = ((episode_id - 501) // 50) + 1
        era_titles = {
            1: "Falsafah Luhur Siriq na Pesse dan Tuntunan Moral Leluhur",
            2: "Kearifan Maritim Pinisi dan Hukum Laut Dunia Amanna Gappa",
            3: "Misteri Peran Suci Bissu dan Penjaga Bahasa Dewata",
            4: "Pahlawan Manuskrip: Kisah Colliq Pujié Menyalin 300.000 Larik Lontar"
        }
        title = era_titles.get(sub_era, "Falsafah dan Kearifan Budaya Bugis-Makassar")
        is_start = ((episode_id - 501) % 50 == 0)
        return "Era 3: Falsafah & Kearifan Nusantara", title, is_start

    # Era 4: Kisah Sudut Pandang Alternatif dan Hikayat Maritim Abadi (Episode 701+)
    sub_cycle = ((episode_id - 701) // 100) + 1
    is_start = ((episode_id - 701) % 100 == 0)
    return "Era 4: Sudut Pandang Alternatif", f"Hikayat Nusantara Musim {sub_cycle}", is_start

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
    logger.info("State berhasil disimpan ke state.json")

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
    agar pola jam tayang Threads selalu bervariasi alami.
    """
    if skip or os.getenv("SKIP_JITTER", "false").lower() in ("true", "1", "yes"):
        logger.info("[JITTER] Dilewati (mode testing).")
        return

    delay_seconds = random.randint(0, 540)
    delay_minutes = delay_seconds / 60.0
    logger.info(
        f"[JITTER] Menunda pengiriman selama {delay_seconds} detik ({delay_minutes:.2f} menit) "
        "agar pola waktu posting terlihat natural..."
    )
    time.sleep(delay_seconds)
    logger.info("[JITTER] Selesai menunggu, melanjutkan pengunggahan.")

def clean_and_verify_text(text: str, max_chars: int = 450) -> str:
    cleaned = text.replace("—", ", ").replace("--", ", ")
    cleaned = " ".join(cleaned.split())
    if len(cleaned) > max_chars:
        logger.warning(f"Teks melebihi batas {max_chars} karakter ({len(cleaned)}). Memotong secara aman...")
        cleaned = cleaned[:max_chars - 3] + "..."
    return cleaned

class ThreadsPoster:
    def __init__(self, user_id: str, access_token: str, dry_run: bool = False):
        self.user_id = user_id
        self.access_token = access_token
        self.dry_run = dry_run
        self.base_url = "https://graph.threads.net/v1.0"

    def create_media_container(self, text: str, image_url: Optional[str] = None) -> Optional[str]:
        if self.dry_run:
            fake_id = f"mock_container_{int(time.time() * 1000)}"
            logger.info(f"[DRY-RUN] Buat container media (image={image_url is not None}) -> ID: {fake_id}")
            return fake_id

        url = f"{self.base_url}/{self.user_id}/threads"
        payload = {
            "text": text,
            "access_token": self.access_token
        }
        if image_url:
            payload["media_type"] = "IMAGE"
            payload["image_url"] = image_url
        else:
            payload["media_type"] = "TEXT"

        resp = requests.post(url, data=payload, timeout=30)
        if not resp.ok:
            logger.error(f"Gagal membuat container Threads: {resp.text}")
            return None
        return resp.json().get("id")

    def publish_container(self, creation_id: str) -> Optional[str]:
        if self.dry_run:
            fake_post_id = f"mock_post_{int(time.time() * 1000)}"
            logger.info(f"[DRY-RUN] Publish container {creation_id} -> Post ID: {fake_post_id}")
            return fake_post_id

        time.sleep(5)
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

def generate_next_episode_with_gemini(episode_id: int, api_key: str) -> Optional[dict]:
    era_name, theme_name, is_start = get_content_era(episode_id)
    slot_num = ((episode_id - 1) % 3)
    slots = ["Pagi (07:00 WITA)", "Siang (12:00 WITA)", "Malam (20:00 WITA)"]
    current_slot = slots[slot_num]
    next_slot = slots[(slot_num + 1) % 3]
    day_num = ((episode_id - 1) // 3) + 1

    logger.info(f"Menghubungi Gemini API untuk memproduksi Episode {episode_id} ({theme_name})...")

    prompt = f"""Kamu adalah sejarawan ulung, budayawan Bugis-Makassar, dan pencerita mitologi serta sejarah Nusantara berwibawa.
Tugasmu adalah menyusun naskah Episode {episode_id} untuk serial berkelanjutan di Threads.

Informasi Konteks:
- Era Konten: {era_name}
- Tema / Babak: {theme_name}
- Slot Tayang: Hari {day_num} - {current_slot}

Aturan Penulisan Ketat:
1. Jika ini awal babak baru ({is_start}), awali teks dengan: [MULAI {theme_name.upper()}].
2. Tulis teks narasi yang berbobot, emosional, dan mendebarkan dengan panjang maksimal 400 karakter (di bawah 450 karakter).
3. Di kalimat terakhir, berikan kalimat pengait alami untuk mengarahkan pembaca ke episode berikutnya (contoh: Simak kelanjutannya {next_slot}!).
4. DILARANG menggunakan tanda em-dash (— atau --). Gunakan koma, titik, atau tanda kurung.
5. Tuliskan deskripsi prompt gambar (image_prompt) bergaya lukisan klasik sejarah Nusantara 8k untuk adegan kisah ini.

Keluarkan HANYA format JSON valid berikut:
{{
  "id": {episode_id},
  "arc": "{theme_name}",
  "arc_change": {str(is_start).lower()},
  "slot": "Hari {day_num} - {current_slot}",
  "title": "Judul Episode",
  "text": "Teks narasi di bawah 400 karakter...",
  "image_prompt": "Epic classical Bugis Indonesian historical art painting of..."
}}
"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "response_mime_type": "application/json"}
        }
        res = requests.post(url, json=payload, timeout=60)
        res.raise_for_status()
        data = res.json()
        parsed = json.loads(data["candidates"][0]["content"]["parts"][0]["text"])
        parsed["text"] = clean_and_verify_text(parsed.get("text", ""))
        parsed["image_path"] = f"images/episode_{episode_id}.jpg"
        parsed["image_raw_url"] = f"https://raw.githubusercontent.com/Versi3Dvision/threads-galigo-bot/main/images/episode_{episode_id}.jpg"
        return parsed
    except Exception as e:
        logger.error(f"Gagal generate episode via Gemini API: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Bot Auto-Post Serial Epos Nusantara Tanpa Henti")
    parser.add_argument("--dry-run", action="store_true", help="Uji coba tanpa posting ke Threads")
    parser.add_argument("--no-jitter", action="store_true", help="Lewati penundaan human jitter 0-9 menit")
    parser.add_argument("--force-episode", type=int, help="Paksa nomor episode tertentu")
    args = parser.parse_args()

    state = load_state()
    episodes = load_episodes()

    target_id = args.force_episode or state.get("current_episode_id", 1)
    logger.info(f"Target Episode: {target_id}")

    current_episode = next((ep for ep in episodes if ep.get("id") == target_id), None)

    # Jika episode belum tersimpan di episodes.json, produksi otomatis lewat Gemini API
    if not current_episode:
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            current_episode = generate_next_episode_with_gemini(target_id, gemini_key)
            if current_episode:
                episodes.append(current_episode)
                save_episodes(episodes)
        else:
            logger.error(
                f"Episode {target_id} belum ada di episodes.json dan GEMINI_API_KEY belum disetel. "
                "Setel GEMINI_API_KEY agar bot dapat memproduksi ide episode baru secara otomatis."
            )
            sys.exit(1)

    title = current_episode.get("title", "")
    slot = current_episode.get("slot", "")
    arc = current_episode.get("arc", "")
    is_arc_change = current_episode.get("arc_change", False)
    text = clean_and_verify_text(current_episode.get("text", ""))
    image_url = current_episode.get("image_raw_url")
    local_image = os.path.join(BASE_DIR, current_episode.get("image_path", ""))

    if is_arc_change:
        logger.info(f"[PERGANTIAN BABAK / ARC] Memulai babak baru: {arc}")

    logger.info(f"Arc / Babak: {arc}")
    logger.info(f"Slot: {slot}")
    logger.info(f"Judul: {title}")
    logger.info(f"Panjang Teks: {len(text)} karakter (Batas Threads: 500, Batas Bot: 450)")
    logger.info(f"Teks: {text}")
    logger.info(f"Gambar URL: {image_url}")
    logger.info(f"Berkas Gambar Lokal Ada: {os.path.exists(local_image)}")

    # Eksekusi Human Jitter 0-9 menit
    apply_human_jitter(skip=args.no_jitter)

    threads_user_id = os.getenv("THREADS_USER_ID", "")
    threads_token = os.getenv("THREADS_ACCESS_TOKEN", "")

    dry_run = args.dry_run or (not threads_user_id or not threads_token)
    if dry_run and not args.dry_run:
        logger.warning("Kredensial Threads API belum diisi. Menjalankan dalam mode simulasi DRY-RUN.")

    poster = ThreadsPoster(user_id=threads_user_id, access_token=threads_token, dry_run=dry_run)
    valid_image_url = image_url if os.path.exists(local_image) else None
    if not valid_image_url and image_url:
        logger.info("Gambar lokal belum tersedia, memposting dengan format teks murni.")

    container_id = poster.create_media_container(text=text, image_url=valid_image_url)
    if not container_id:
        logger.error("Gagal membuat container postingan.")
        sys.exit(1)

    post_id = poster.publish_container(container_id)
    if not post_id:
        logger.error("Gagal mempublikasikan postingan.")
        sys.exit(1)

    logger.info(f"Sukses mempublikasikan Episode {target_id} ke Threads! (ID: {post_id})")

    # Perbarui urutan ke episode selanjutnya
    if not dry_run or args.force_episode is None:
        state["current_episode_id"] = target_id + 1
        state["last_posted_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        state["history"].append({
            "episode_id": target_id,
            "title": title,
            "arc": arc,
            "slot": slot,
            "post_id": post_id,
            "posted_at": state["last_posted_at"],
            "image_url": image_url,
            "mode": "live" if not dry_run else "dry-run"
        })
        save_state(state)
        logger.info(f"Episode berikutnya yang dijadwalkan: Episode {state['current_episode_id']}")

if __name__ == "__main__":
    main()
