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
    return {
        "current_episode_id": 1,
        "last_posted_at": None,
        "history": [],
        "threads_access_token": None,
        "token_last_refreshed_at": None
    }

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
    Menunda eksekusi secara acak agar pola jam tayang Threads selalu bervariasi alami.
    Didesain efisien agar sangat hemat kuota menit GitHub Actions (repositori private).
    Dapat disesuaikan lewat env JITTER_MAX_SECONDS (default 60 detik) dan JITTER_MIN_SECONDS (default 10 detik).
    """
    if skip or os.getenv("SKIP_JITTER", "false").lower() in ("true", "1", "yes"):
        logger.info("[JITTER] Dilewati (mode testing).")
        return

    min_sec = int(os.getenv("JITTER_MIN_SECONDS", "10"))
    max_sec = int(os.getenv("JITTER_MAX_SECONDS", "60"))
    delay_seconds = random.randint(min_sec, max_sec)
    logger.info(
        f"[JITTER] Menunda pengiriman selama {delay_seconds} detik "
        "agar pola jam tayang natural dan tetap hemat kuota GitHub Actions..."
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

def refresh_threads_access_token(current_token: str) -> Optional[dict]:
    """
    Memperpanjang masa aktif long-lived Threads access token secara otomatis.
    Endpoint resmi Meta Threads:
    GET https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token={token}
    Token yang berumur minimal 24 jam akan di-reset masa aktifnya menjadi 60 hari (5.184.000 detik).
    """
    if not current_token:
        return None
    try:
        url = "https://graph.threads.net/refresh_access_token"
        params = {
            "grant_type": "th_refresh_token",
            "access_token": current_token
        }
        resp = requests.get(url, params=params, timeout=20)
        if resp.ok:
            data = resp.json()
            expires_in = data.get("expires_in", 5184000)
            days = expires_in // 86400
            logger.info(f"Berhasil memperpanjang token Threads otomatis! Masa aktif di-reset: {days} hari ({expires_in} detik).")
            return data
        else:
            logger.warning(f"Respon perpanjangan token Threads: {resp.text}")
            return None
    except Exception as e:
        logger.error(f"Gagal menghubungi server Meta untuk perpanjangan token: {e}")
def get_public_image_url(image_rel_path: str) -> Optional[str]:
    """
    Menghasilkan URL publik untuk gambar agar dapat diunduh oleh server Meta Threads:
    1. Pastikan berkas gambar ada secara fisik di disk lokal runner.
    2. Jika repo private dan GITHUB_TOKEN tersedia di runner, minta signed download_url
       ke GitHub Contents API (URL bertanda tangan ini dapat diunduh publik selama beberapa menit).
    3. Jika repo public atau token tidak disetel, gunakan format URL raw GitHub.
    """
    if not image_rel_path:
        return None

    local_path = os.path.join(BASE_DIR, image_rel_path)
    if not os.path.exists(local_path):
        return None

    clean_path = image_rel_path.replace("\\", "/").lstrip("/")
    github_token = os.getenv("GITHUB_TOKEN", "").strip()
    github_repo = os.getenv("GITHUB_REPOSITORY", "AlchemiztGOd/threads-galigo-bot").strip()

    if github_token and github_repo:
        try:
            api_url = f"https://api.github.com/repos/{github_repo}/contents/{clean_path}"
            headers = {
                "Authorization": f"Bearer {github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            resp = requests.get(api_url, headers=headers, timeout=15)
            if resp.ok:
                download_url = resp.json().get("download_url")
                if download_url:
                    logger.info("Berhasil membuat signed download_url sementara via GitHub API untuk repo private.")
                    return download_url
        except Exception as e:
            logger.warning(f"Gagal mengambil signed download_url via GitHub API: {e}")

    return f"https://raw.githubusercontent.com/{github_repo}/main/{clean_path}"

class ThreadsPoster:
    def __init__(self, user_id: str, access_token: str, dry_run: bool = False):
        self.user_id = user_id
        self.access_token = access_token
        self.dry_run = dry_run
        self.base_url = "https://graph.threads.net/v1.0"

    def create_media_container(self, text: str, image_url: Optional[str] = None, reply_to_id: Optional[str] = None) -> Optional[str]:
        if self.dry_run:
            fake_id = f"mock_container_{int(time.time() * 1000)}"
            logger.info(f"[DRY-RUN] Buat container media (image={image_url is not None}, reply_to={reply_to_id}) -> ID: {fake_id}")
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

    def publish_thread(self, parts: List[str], image_url: Optional[str] = None) -> Optional[List[str]]:
        """
        Mempublikasikan serial multi-post (Utas / Thread) bersambung:
        - Postingan 1 (Root): Teks Bagian 1 + Lukisan Resolusi Tinggi
        - Postingan 2 dst: Dibalas berantai secara linier di bawah postingan sebelumnya
        Memungkinkan total narasi mencapai 400-450 kata utuh tanpa melanggar batas karakter Threads.
        """
        if not parts:
            return None

        published_ids = []
        parent_id = None

        for idx, part_text in enumerate(parts):
            is_root = (idx == 0)
            img = image_url if is_root else None

            logger.info(f"Mempersiapkan Utas Bagian {idx + 1}/{len(parts)} ({len(part_text)} karakter)...")
            container_id = self.create_media_container(text=part_text, image_url=img, reply_to_id=parent_id)
            if not container_id:
                logger.error(f"Gagal membuat container untuk Utas Bagian {idx + 1}")
                break

            post_id = self.publish_container(container_id)
            if not post_id:
                logger.error(f"Gagal mempublikasikan Utas Bagian {idx + 1}")
                break

            published_ids.append(post_id)
            parent_id = post_id
            logger.info(f"Sukses menerbitkan Utas Bagian {idx + 1}/{len(parts)} (ID: {post_id})")

            # Beri jeda antar balasan agar aman dari rate-limit Meta Threads
            if not self.dry_run and idx < len(parts) - 1:
                time.sleep(4)

        return published_ids if published_ids else None

def get_emergency_fallback_episode(episode_id: int) -> dict:
    """
    Cadangan darurat jika seluruh kuota Gemini API habis terkena limit 429.
    Menghasilkan episode kultural bermutu tinggi tentang kearifan Bugis-Makassar
    dalam format Utas / Thread panjang (~400-450 kata / 4-5 bagian)
    sehingga jadwal posting tidak pernah macet atau gagal.
    """
    era_name, theme_name, is_start = get_content_era(episode_id)
    slot_num = ((episode_id - 1) % 3)
    slots = ["Pagi (07:05 WITA)", "Siang (12:05 WITA)", "Malam (20:05 WITA)"]
    current_slot = slots[slot_num]
    next_slot = slots[(slot_num + 1) % 3]
    day_num = ((episode_id - 1) // 3) + 1

    fallbacks = [
        ("Falsafah Luhur Siriq na Pesse", [
            f"[KHAZANAH FALSAFAH BUGIS: {theme_name.upper()}]\nDalam tradisi agung Bugis-Makassar kuno, martabat manusia dipandu oleh dua pilar tak terpisahkan: Siriq na Pesse. Siriq adalah rasa malu dan keteguhan menjaga kehormatan diri serta keluarga di hadapan semesta. Tanpa siriq, seorang manusia dianggap kehilangan kemuliaan jiwa penegak kebenaran. (1/4)",
            "Pilar kedua yang melengkapi ketegasan siriq adalah pesse (atau pacce dalam dialek Makassar). Pesse adalah kelembutan hati yang turut merasakan kepedihan sesama manusia seolah darah sendiri yang teriris. Bila ada warga kaum yang teraniaya atau lapar, seluruh rumpun keluarga ikut menanggung derita yang sama. (2/4)",
            "Para tetua Luwu dan Bone mengajarkan: ksatria sejati tak diukur dari seberapa banyak musuh yang roboh di ujung kerisnya, melainkan dari seberapa teguh ia memegang sumpah dan melindungi yang lemah. Hukum adat menegaskan bahwa pemimpin yang zalim akan kehilangan tuah berkah tanahnya. (3/4)",
            f"Falsafah abadi inilah yang membuat masyarakat Bugis-Makassar disegani di seantero maritim Nusantara hingga pelabuhan mancanegara. Keberanian diimbangi keadilan, martabat dibungkus persaudaraan. Simak babak epik kelanjutannya {next_slot}! (4/4)"
        ]),
        ("Kearifan Hukum Laut Amanna Gappa", [
            f"[KHAZANAH SEJARAH MARITIM: {theme_name.upper()}]\nJauh sebelum bangsa Eropa memperkenalkan hukum maritim modern di perairan timur, pelaut ulung Bugis telah memiliki undang-undang navigasi tertulis paling komprehensif di dunia yang dikenal sebagai Piagam Adeq Allopiloping Bicaranna Pabbaluq karya Matowa Amanna Gappa. (1/4)",
            "Piagam agung yang dirumuskan di Batavia pada abad ke-17 ini mengatur secara rinci hak dan kewajiban juragan perahu, sewa muatan dagang, pembagian keuntungan pelayaran, hingga keselamatan awak kapal yang berlayar dari Malaka, Sumbawa, Maluku, hingga pesisir utara Australia. (2/4)",
            "Dalam pandangan para pelaut Pinisi, samudra raya bukanlah dinding pemisah kepulauan, melainkan jalan raya kemakmuran bersama yang harus dijaga keamanannya. Setiap perselisihan niaga di atas gelombang diselesaikan melalui musyawarah adat berlandaskan kejujuran dan keadilan mutlak. (3/4)",
            f"Kekuatan hukum laut inilah yang menjadikan kapal layar Bugis penguasa jalur rempah Nusantara selama berabad-abad. Warisan peradaban ini membuktikan tingginya peradaban bahari nenek moyang kita. Simak kisah petualangan samudra berikutnya {next_slot}! (4/4)"
        ]),
        ("Pappaseng: Empat Pilar Kejayaan Negeri", [
            f"[KHAZANAH KEARIFAN LELUHUR: {theme_name.upper()}]\nDalam naskah lontaraq kuno tersimpan Pappaseng, petuah wasiat suci para cendekiawan dan datu masa silam. Salah satu ajaran paling mendasar menegaskan bahwa tegak dan runtuhnya suatu negeri bersandar pada empat pilar yang saling menopang satu sama lain. (1/4)",
            "Empat pilar tersebut adalah: pertama, para hakim dan aparat adat yang jujur serta adil dalam menegakkan hukum tanpa pandang bulu. Kedua, para ksatria dan tentara yang gagah berani melindungi tanah air dengan jiwa raga tanpa pamrih pribadi. (2/4)",
            "Pilar ketiga adalah para cendekiawan dan tetua bijak yang senantiasa memberi nasihat luhur kepada raja tanpa rasa takut. Dan pilar keempat adalah rakyat jelata yang rajin bekerja memakmurkan lumbung padi serta menjaga kebersihan mata air negeri. (3/4)",
            f"Bila salah satu dari keempat pilar ini retak atau dikhianati oleh ketamakan nafsu, maka azab bencana dan perpecahan akan melanda seluruh jagat. Nilai kepemimpinan universal ini tetap relevan melintasi zaman. Simak lanjutan naskah bersejarah {next_slot}! (4/4)"
        ]),
        ("Mitos Bahtera Pasompe dan Pesan Ekologis", [
            f"[LEGENDA & MISTERI NUSANTARA: {theme_name.upper()}]\nKisah pembuatan bahtera Wakka Pasompe dalam naskah Sureq Galigo bukan sekadar cerita pelayaran asmara Sawerigading, melainkan peringatan kosmis tertua di Nusantara tentang batas hubungan antara keserakahan manusia dan kelestarian alam semesta. (1/4)",
            "Ketika pohon suci Welenrengnge ditebang untuk dijadikan lambung kapal raksasa, jagat raya seketika murka. Burung garuda raksasa terbang menghempaskan badai, dan telur-telur keramat di puncaknya jatuh menimbulkan banjir bandang air bah yang menenggelamkan perkampungan. (2/4)",
            "Leluhur Bugis mengajarkan bahwa setiap perusakan alam selalu melahirkan konsekuensi pahit bagi peradaban manusia. Menaklukkan alam tanpa izin ritual, tanpa penghormatan, dan tanpa rasa syukur hanya akan membawa malapetaka bagi keturunan yang hidup setelahnya. (3/4)",
            f"Pesan ekologis ribuan tahun lalu ini menjadi cermin abadi bagi zaman modern: bahwa manusia dan semesta harus senantiasa hidup dalam harmoni yang seimbang. Simak kelanjutan petualangan epik Sawerigading {next_slot}! (4/4)"
        ]),
        ("Sumpah Layar Terkembang Ksatria Samudra", [
            f"[JIWA BAHARI BUGIS-MAKASSAR: {theme_name.upper()}]\nPepatah luhur pelaut Bugis berbunyi: 'Kualleangi tallanga na toalia', yang bermakna lebih baik tenggelam di palung samudra daripada surut kembali ke pantai tanpa membawa kehormatan dan keberhasilan. Ini bukan sekadar tekad buta, melainkan sumpah tanggung jawab seorang ksatria. (1/4)",
            "Ketika layar pinisi telah terkembang dan kemudi telah terpasang mantap ke arah bintang penunjuk jalan, tidak ada tempat untuk rasa gentar di dada para kelasi. Gelombang yang menggunung dan badai gelap dihadapi dengan perhitungan matang serta kepasrahan kepada sang penguasa lautan. (2/4)",
            "Keteguhan mental inilah yang mengantarkan nenek moyang bangsa mengarungi Samudra Hindia hingga Madagaskar dan melintasi Samudra Pasifik berbekal perahu kayu tanpa mesin. Ketahanan fisik ditempa oleh keheningan samudra di bawah gemerlap bintang malam. (3/4)",
            f"Semangat pantang menyerah ini terus mengalir deras dalam darah generasi penerus hingga hari ini. Menghadapi badai kehidupan dengan dada tegak dan kehormatan suci. Ikuti kisah kepahlawanan maritim selanjutnya {next_slot}! (4/4)"
        ])
    ]

    chosen_title, chosen_parts = fallbacks[(episode_id - 1) % len(fallbacks)]
    full_text = "\n\n".join(chosen_parts)

    logger.info(f"[EMERGENCY VAULT] Menggunakan naskah Utas cadangan bermutu untuk Episode {episode_id}")

    return {
        "id": episode_id,
        "arc": theme_name,
        "arc_change": is_start,
        "slot": f"Hari {day_num} - {current_slot}",
        "title": chosen_title,
        "text": full_text,
        "thread_parts": chosen_parts,
        "image_path": f"images/episode_{episode_id}.jpg",
        "image_raw_url": f"https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_{episode_id}.jpg",
        "image_prompt": "Epic classical Bugis Indonesian heritage oil painting, museum quality 8k"
    }

def generate_next_episode_with_gemini(episode_id: int, api_keys_input: str) -> Optional[dict]:
    era_name, theme_name, is_start = get_content_era(episode_id)
    slot_num = ((episode_id - 1) % 3)
    slots = ["Pagi (07:05 WITA)", "Siang (12:05 WITA)", "Malam (20:05 WITA)"]
    current_slot = slots[slot_num]
    next_slot = slots[(slot_num + 1) % 3]
    day_num = ((episode_id - 1) // 3) + 1

    prompt = f"""Kamu adalah sejarawan ulung, sastrawan Bugis-Makassar, dan novelis mitologi Nusantara berwibawa.
Tugasmu adalah menyusun naskah bersambung Episode {episode_id} dalam format UTAS / THREAD PANJANG (5 Bagian Bersambung, total cerita sekitar 400 hingga 450 kata / 2.000 hingga 2.400 karakter).

Informasi Konteks:
- Era Konten: {era_name}
- Tema / Babak: {theme_name}
- Slot Tayang: Hari {day_num} - {current_slot}

Struktur Utas (5 Bagian Bersambung):
1. Bagian 1 (Pembuka): Pembuka narasi megah, suasana kosmis/lingkungan, dan pengantar adegan. (Jika awal babak [{is_start}], awali teks dengan: [MULAI {theme_name.upper()}]). Akhiri dengan tanda (1/5).
2. Bagian 2 (Konflik/Dinamika): Pertemuan karakter, dialog bermartabat ala bangsawan Bugis, atau ketegangan yang mulai merayap. Akhiri dengan tanda (2/5).
3. Bagian 3 (Puncak/Aksi): Puncak peristiwa, pertarungan ksatria, pelayaran menembus gelombang, atau keputusan genting. Akhiri dengan tanda (3/5).
4. Bagian 4 (Dampak & Resonansi): Dampak peristiwa terhadap jagat/kerajaan, serta sentuhan emosional para tokoh. Akhiri dengan tanda (4/5).
5. Bagian 5 (Falsafah & Pengait): Renungan falsafah luhur leluhur (Siriq na Pesse, Pappaseng) dan kalimat pengait penutup (contoh: Simak kelanjutan kisahnya {next_slot}!). Akhiri dengan tanda (5/5).

Aturan Penulisan Ketat:
- Setiap bagian HARUS berkisar antara 350 hingga 430 karakter (TIDAK BOLEH melebihi 450 karakter per bagian).
- DILARANG KERAS menggunakan tanda em-dash (— atau --). Gunakan koma, titik, atau tanda kurung.
- Bahasa Indonesia sastrawi tinggi berbobot, bebas dari kata klise AI yang dangkal.

Keluarkan HANYA format JSON valid berikut:
{{
  "id": {episode_id},
  "arc": "{theme_name}",
  "arc_change": {str(is_start).lower()},
  "slot": "Hari {day_num} - {current_slot}",
  "title": "Judul Episode",
  "thread_parts": [
    "Teks Bagian 1 (1/5)...",
    "Teks Bagian 2 (2/5)...",
    "Teks Bagian 3 (3/5)...",
    "Teks Bagian 4 (4/5)...",
    "Teks Bagian 5 (5/5)..."
  ],
  "image_prompt": "Epic classical Bugis Indonesian historical art painting of..."
}}
"""
    # Dukungan multi-key: pisahkan berdasarkan koma jika ada beberapa API key cadangan
    keys = [k.strip() for k in api_keys_input.split(",") if k.strip()]
    models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "response_mime_type": "application/json"}
    }

    for key_idx, key in enumerate(keys, 1):
        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            try:
                logger.info(f"Mencoba Gemini API (Key #{key_idx}, Model: {model}) untuk Utas Episode {episode_id}...")
                res = requests.post(url, json=payload, timeout=45)
                if res.status_code == 429:
                    logger.warning(f"Key #{key_idx} pada model {model} mencapai kuota/rate-limit harian (429). Mencoba alternatif...")
                    continue
                res.raise_for_status()
                data = res.json()
                raw_json = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(raw_json)
                raw_parts = parsed.get("thread_parts", [])
                if isinstance(raw_parts, list) and raw_parts:
                    parsed["thread_parts"] = [clean_and_verify_text(p) for p in raw_parts if p.strip()]
                    parsed["text"] = "\n\n".join(parsed["thread_parts"])
                else:
                    parsed["text"] = clean_and_verify_text(parsed.get("text", ""))
                    parsed["thread_parts"] = [parsed["text"]]

                parsed["image_path"] = f"images/episode_{episode_id}.jpg"
                parsed["image_raw_url"] = f"https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_{episode_id}.jpg"
                logger.info(f"Sukses menghasilkan Utas Episode {episode_id} ({len(parsed['thread_parts'])} bagian) via Gemini {model}!")
                return parsed
            except Exception as e:
                logger.warning(f"Percobaan dengan {model} gagal: {e}")

    logger.error("Seluruh kuota Gemini API habis atau terkena rate limit. Mengaktifkan Emergency Fallback Vault...")
    return get_emergency_fallback_episode(episode_id)

def main():
    parser = argparse.ArgumentParser(description="Bot Auto-Post Serial Epos Nusantara Tanpa Henti")
    parser.add_argument("--dry-run", action="store_true", help="Uji coba tanpa posting ke Threads")
    parser.add_argument("--no-jitter", action="store_true", help="Lewati penundaan human jitter 0-9 menit")
    parser.add_argument("--force-episode", type=int, help="Paksa nomor episode tertentu")
    parser.add_argument("--refresh-token", action="store_true", help="Perpanjang masa aktif token Threads ke Meta API sekarang")
    args = parser.parse_args()

    state = load_state()
    episodes = load_episodes()

    # Prioritaskan token aktif hasil perpanjangan di state.json, lalu fallback ke environment variable
    stored_token = state.get("threads_access_token")
    threads_token = (stored_token or os.getenv("THREADS_ACCESS_TOKEN", "")).strip()

    # Periksa apakah perlu memperpanjang masa aktif token (jika sudah >= 7 hari atau diminta via argumen)
    last_refresh_str = state.get("token_last_refreshed_at")
    should_refresh = args.refresh_token
    if not should_refresh and threads_token:
        if not last_refresh_str:
            should_refresh = True
        else:
            try:
                last_dt = datetime.datetime.fromisoformat(last_refresh_str)
                now_dt = datetime.datetime.now(datetime.timezone.utc)
                if (now_dt - last_dt).days >= 7:
                    should_refresh = True
            except Exception:
                should_refresh = True

    if should_refresh and threads_token and not args.dry_run:
        logger.info("Memeriksa dan memperpanjang masa aktif token Threads ke Meta API...")
        refresh_res = refresh_threads_access_token(threads_token)
        if refresh_res and refresh_res.get("access_token"):
            new_token = refresh_res.get("access_token")
            threads_token = new_token
            state["threads_access_token"] = new_token
            state["token_last_refreshed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            save_state(state)
            logger.info("Token baru telah tersimpan di state.json dan akan di-commit otomatis ke repositori.")

    if args.refresh_token:
        logger.info("Mode perpanjangan token selesai dieksekusi.")
        return

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
    raw_thread_parts = current_episode.get("thread_parts")
    if isinstance(raw_thread_parts, list) and len(raw_thread_parts) > 1:
        thread_parts = [clean_and_verify_text(p) for p in raw_thread_parts if p.strip()]
    else:
        # Jika thread_parts belum lengkap (hanya teks pendek), lakukan ekspansi otomatis ke Utas 5 bagian!
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            logger.info(f"Episode {target_id} belum memiliki Utas lengkap. Menjalankan ekspansi otomatis via Gemini API...")
            expanded = generate_next_episode_with_gemini(target_id, gemini_key)
            if expanded and expanded.get("thread_parts") and len(expanded.get("thread_parts")) > 1:
                current_episode = expanded
                thread_parts = expanded["thread_parts"]
                title = current_episode.get("title", title)
                # Perbarui episodes.json agar tidak perlu memanggil ulang di masa depan
                for idx_ep, ep_item in enumerate(episodes):
                    if ep_item.get("id") == target_id:
                        episodes[idx_ep] = expanded
                        break
                else:
                    episodes.append(expanded)
                save_episodes(episodes)
            else:
                fallback_ep = get_emergency_fallback_episode(target_id)
                thread_parts = fallback_ep.get("thread_parts", [clean_and_verify_text(current_episode.get("text", ""))])
        else:
            fallback_ep = get_emergency_fallback_episode(target_id)
            thread_parts = fallback_ep.get("thread_parts", [clean_and_verify_text(current_episode.get("text", ""))])

    image_url = current_episode.get("image_raw_url")
    local_image = os.path.join(BASE_DIR, current_episode.get("image_path", ""))

    if is_arc_change:
        logger.info(f"[PERGANTIAN BABAK / ARC] Memulai babak baru: {arc}")

    total_words = sum(len(p.split()) for p in thread_parts)
    total_chars = sum(len(p) for p in thread_parts)
    logger.info(f"Arc / Babak: {arc}")
    logger.info(f"Slot: {slot}")
    logger.info(f"Judul: {title}")
    logger.info(f"Format Tayang: Utas / Thread ({len(thread_parts)} bagian bersambung, total {total_words} kata, {total_chars} karakter)")
    for i, p in enumerate(thread_parts, 1):
        logger.info(f"  - Bagian {i}/{len(thread_parts)} ({len(p)} char): {p[:90]}...")
    logger.info(f"Gambar URL: {image_url}")
    logger.info(f"Berkas Gambar Lokal Ada: {os.path.exists(local_image)}")

    # Eksekusi Human Jitter 10-60 detik
    apply_human_jitter(skip=args.no_jitter)

    threads_user_id = os.getenv("THREADS_USER_ID", "").strip()

    # Jika THREADS_USER_ID belum diisi tetapi THREADS_ACCESS_TOKEN tersedia, ambil ID otomatis
    if not threads_user_id and threads_token and not args.dry_run:
        try:
            logger.info("THREADS_USER_ID belum diisi, mencoba mengambil otomatis via Threads API...")
            me_resp = requests.get(
                f"https://graph.threads.net/v1.0/me?fields=id,username&access_token={threads_token}",
                timeout=15
            )
            if me_resp.ok:
                me_data = me_resp.json()
                threads_user_id = me_data.get("id", "")
                logger.info(f"Berhasil mendeteksi User ID otomatis: {threads_user_id} (Akun: @{me_data.get('username')})")
            else:
                logger.warning(f"Gagal mengambil ID dari /me: {me_resp.text}")
        except Exception as e:
            logger.warning(f"Error saat mengambil ID otomatis: {e}")

    dry_run = args.dry_run or (not threads_user_id or not threads_token)
    if dry_run and not args.dry_run:
        logger.warning("Kredensial Threads API belum diisi. Menjalankan dalam mode simulasi DRY-RUN.")

    poster = ThreadsPoster(user_id=threads_user_id, access_token=threads_token, dry_run=dry_run)
    valid_image_url = get_public_image_url(current_episode.get("image_path", ""))
    if not valid_image_url:
        logger.info("Gambar lokal belum tersedia, memposting utas dengan format teks murni.")
    else:
        logger.info("URL gambar siap dikirimkan bersama postingan utama Utas.")

    published_ids = poster.publish_thread(parts=thread_parts, image_url=valid_image_url)
    if not published_ids:
        logger.error("Gagal mempublikasikan Utas postingan ke Threads.")
        sys.exit(1)

    root_post_id = published_ids[0]
    logger.info(f"Sukses mempublikasikan Utas Episode {target_id} ({len(published_ids)} bagian) ke Threads! (Root ID: {root_post_id})")

    # Perbarui urutan ke episode selanjutnya (hanya disimpan bila posting nyata)
    if not dry_run:
        state["current_episode_id"] = target_id + 1
        state["last_posted_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        state["history"].append({
            "episode_id": target_id,
            "title": title,
            "arc": arc,
            "slot": slot,
            "post_id": root_post_id,
            "thread_ids": published_ids,
            "parts_count": len(published_ids),
            "posted_at": state["last_posted_at"],
            "image_url": valid_image_url,
            "mode": "live"
        })
        save_state(state)
        logger.info(f"Episode berikutnya yang dijadwalkan: Episode {state['current_episode_id']}")
    else:
        logger.info(f"[DRY-RUN] Simulasi penayangan Utas Episode {target_id} berhasil. state.json tidak diubah.")

if __name__ == "__main__":
    main()
