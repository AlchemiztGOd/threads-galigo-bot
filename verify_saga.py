# Script verifikasi 28 episode Sureq Galigo
# Memastikan panjang karakter < 450 dan bebas em-dash

saga = [
    # ARC 1: Asal Mula Dewata dan Berdirinya Luwu
    {
        "id": 1,
        "arc": "Arc 1: Asal-Usul Dewata dan Berdirinya Luwu",
        "arc_change": True,
        "slot": "Hari 1 - Pagi (07:00 WITA)",
        "title": "Awal Mula Penciptaan Jagat Raya",
        "text": "[ARC 1: ASAL DEWATA]\nSebelum ada manusia, jagat terbagi tiga: Boting Langiq di puncak langit, Uriq Liu di kedalaman laut, dan Ale Lino di tengah yang masih sunyi. Penguasa langit Patotoqe bermusyawarah dengan penguasa laut Guru ri Selleq. Mereka sepakat mengutus darah dewata untuk memakmurkan bumi. Kilat menyambar di cakrawala. Simak kelanjutannya siang nanti jam 12:00 WITA!",
        "image_path": "images/episode_1.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_1.jpg",
        "image_prompt": "Epic classical Bugis mythology art painting, celestial beings Patotoqe and Guru ri Selleq looking down at primordial earth and ocean, mystical gold lighting, 8k"
    },
    {
        "id": 2,
        "arc": "Arc 1: Asal-Usul Dewata dan Berdirinya Luwu",
        "arc_change": False,
        "slot": "Hari 1 - Siang (12:00 WITA)",
        "title": "Turunnya Batara Guru ke Bumi",
        "text": "Kilat membelah cakrawala Luwu diiringi guntur tujuh hari. Putra langit, Batara Guru, diturunkan ke bumi beralaskan bambu gading keramat. Langkah kakinya menyentuh tanah Luwu yang perawan, membawa mandat langit untuk membangun tatanan hidup manusia. Namun bumi belum lengkap tanpa pasangan dari samudra. Nantikan pertemuan agung mereka malam ini jam 20:00 WITA!",
        "image_path": "images/episode_2.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_2.jpg",
        "image_prompt": "Batara Guru descending to ancient Luwu with sacred golden bamboo and lightning, masterpiece 8k"
    },
    {
        "id": 3,
        "arc": "Arc 1: Asal-Usul Dewata dan Berdirinya Luwu",
        "arc_change": False,
        "slot": "Hari 1 - Malam (20:00 WITA)",
        "title": "Kemunculan Putri Samudra We Nyiliq Timo",
        "text": "Dari kedalaman samudra Uriq Liu yang bergolak, muncullah putri jelita We Nyiliq Timo yang menunggangi buih ombak emas. Pertemuan putra langit dan putri samudra di pesisir Luwu menyatukan dua kekuatan kosmis alam semesta. Seluruh alam tunduk memberi hormat pada sang ratu pertama. Ikuti berdirinya kerajaan tertua di Nusantara besok pagi jam 07:00 WITA!",
        "image_path": "images/episode_3.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_3.jpg",
        "image_prompt": "Princess We Nyiliq Timo emerging from golden ocean waves meeting Batara Guru on beach of Luwu, masterpiece 8k"
    },
    {
        "id": 4,
        "arc": "Arc 1: Asal-Usul Dewata dan Berdirinya Luwu",
        "arc_change": False,
        "slot": "Hari 2 - Pagi (07:00 WITA)",
        "title": "Pernikahan Suci dan Berdirinya Kedatuan Luwu",
        "text": "Pernikahan Batara Guru dan We Nyiliq Timo melahirkan Kedatuan Luwu, pusat peradaban tertua bangsa Bugis. Istana megah berdiri, hukum adat ditegakkan, dan tanah Luwu makmur sentosa. Dari trah dewa ini, lahirlah Batara Lattuq sang penerus tahta. Namun langit mulai bergemuruh mengirim tanda petaka baru. Masuki babak kutukan siang nanti jam 12:00 WITA!",
        "image_path": "images/episode_4.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_4.jpg",
        "image_prompt": "Grand royal coronation and wedding in ancient Luwu kingdom palace, ancient Bugis architecture, masterpiece 8k"
    },

    # ARC 2: Kutukan Kembar Emas dan Takdir Terlarang
    {
        "id": 5,
        "arc": "Arc 2: Kutukan Kembar Emas dan Takdir Terlarang",
        "arc_change": True,
        "slot": "Hari 2 - Siang (12:00 WITA)",
        "title": "Lahirnya Kembar Emas yang Mengguncang Jagat",
        "text": "[ARC 2: KUTUKAN KEMBAR EMAS]\nBatara Lattuq memperistri We Datu Sengngeng. Dari rahim sang permaisuri, lahirlah sepasang anak kembar emas: seorang bayi lelaki perkasa Sawerigading, dan saudarinya yang jelita We Tenriabeng. Saat lahir, guncangan gempa melanda Luwu selama tujuh hari. Pertanda apakah ini bagi semesta? Simak malam nanti jam 20:00 WITA!",
        "image_path": "images/episode_5.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_5.jpg",
        "image_prompt": "Queen We Datu Sengngeng giving birth to glowing golden twin babies Sawerigading and We Tenriabeng, masterpiece 8k"
    },
    {
        "id": 6,
        "arc": "Arc 2: Kutukan Kembar Emas dan Takdir Terlarang",
        "arc_change": False,
        "slot": "Hari 2 - Malam (20:00 WITA)",
        "title": "Ramalan Mengerikan Tetua Bissu",
        "text": "Para pendeta suci Bissu gemetar menatap perbintangan. Ramalan kuno berbunyi: jika kedua anak kembar emas ini saling memandang dan memadu kasih, jagat raya akan binasa tertelan murka langit. Lautan akan meluap dan bumi terbelah dua. Demi keselamatan Luwu, sebuah keputusan memilukan harus diambil. Ikuti takdir mereka besok pagi jam 07:00 WITA!",
        "image_path": "images/episode_6.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_6.jpg",
        "image_prompt": "Bissu high priests reading cosmic omens of storm and eclipse, ancient royal court, masterpiece 8k"
    },
    {
        "id": 7,
        "arc": "Arc 2: Kutukan Kembar Emas dan Takdir Terlarang",
        "arc_change": False,
        "slot": "Hari 3 - Pagi (07:00 WITA)",
        "title": "Pemisahan Kembar Emas Sejak Buana",
        "text": "Sejak tarikan napas pertama, kedua bayi dipisahkan. Sawerigading dilarikan ke pedalaman untuk diasuh panglima perang, tanpa pernah tahu ia memiliki saudara kembar. Sementara We Tenriabeng dipingit di kamar rahasia berlapis tujuh sutra emas. Belasan tahun berlalu, takdir yang dipisahkan paksa kini mulai mendekat. Simak siang nanti jam 12:00 WITA!",
        "image_path": "images/episode_7.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_7.jpg",
        "image_prompt": "Baby boy carried away by warrior while baby girl hidden behind golden curtains, masterpiece 8k"
    },
    {
        "id": 8,
        "arc": "Arc 2: Kutukan Kembar Emas dan Takdir Terlarang",
        "arc_change": False,
        "slot": "Hari 3 - Siang (12:00 WITA)",
        "title": "Tirai Sutra dan Api Asmara Terlarang",
        "text": "Sawerigading tumbuh menjadi ksatria perkasa yang tak terkalahkan. Saat ia menginjakkan kaki di istana Luwu, angin nakal menyingkap tirai sutra emas. Matanya tertegun menatap We Tenriabeng yang sedang menenun. Seketika jiwanya terbakar cinta yang tak terbendung, tanpa sadar wanita itu adalah saudarinya sendiri. Babak kutukan dimulai malam ini jam 20:00 WITA!",
        "image_path": "images/episode_8.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_8.jpg",
        "image_prompt": "Sawerigading catching sight of We Tenriabeng behind golden silk curtains, intense romantic gaze, masterpiece 8k"
    },

    # ARC 3: Penebangan Pohon Keramat dan Bahtera Maut
    {
        "id": 9,
        "arc": "Arc 3: Penebangan Pohon Keramat dan Bahtera Maut",
        "arc_change": True,
        "slot": "Hari 3 - Malam (20:00 WITA)",
        "title": "Siasat Cerdik We Tenriabeng",
        "text": "[ARC 3: BAHARU & SAMUDRA]\nUntuk mencegah kiamat Luwu, We Tenriabeng bersiasat: \"Kakandaku, di seberang lautan di Tana Kelling, ada putri We Cudai yang rupa dan suaranya serupa denganku. Pinanglah dia dan arungilah samudra luas.\" Hati Sawerigading tersulut hasrat mengarungi lautan maut. Ikuti persiapan ekspedisinya besok pagi jam 07:00 WITA!",
        "image_path": "images/episode_9.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_9.jpg",
        "image_prompt": "We Tenriabeng pointing to distant ocean on palace balcony, advising Sawerigading, twilight sky, masterpiece 8k"
    },
    {
        "id": 10,
        "arc": "Arc 3: Penebangan Pohon Keramat dan Bahtera Maut",
        "arc_change": False,
        "slot": "Hari 4 - Pagi (07:00 WITA)",
        "title": "Penebangan Pohon Keramat Welenrengnge",
        "text": "Mengarungi samudra butuh perahu terhebat di kolong langit. Sawerigading menuju rimba larangan untuk menebang Welenrengnge, pohon keramat raksasa pelindung kahyangan. Saat mata kapak petir menghantam batangnya, bumi berguncang dan jeritan makhluk gaib memenuhi angkasa. Keberanian menantang alam dimulai! Simak siang nanti jam 12:00 WITA!",
        "image_path": "images/episode_10.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_10.jpg",
        "image_prompt": "Sawerigading striking giant mystical tree Welenrengnge with glowing battleaxe, storm clouds, masterpiece 8k"
    },
    {
        "id": 11,
        "arc": "Arc 3: Penebangan Pohon Keramat dan Bahtera Maut",
        "arc_change": False,
        "slot": "Hari 4 - Siang (12:00 WITA)",
        "title": "Pecahnya Telur Garuda dan Murka Alam",
        "text": "Ketika pohon raksasa itu tumbang menggelegar, sarang burung garuda di puncaknya hancur. Telur raksasanya pecah, menumpahkan cairan yang seketika berubah menjadi banjir bandang melanda lembah Luwu. Murka alam semesta menjadi bayaran mahal atas ambisi manusia. Namun batang kayu suci telah rebah. Simak pemahatan kapalnya malam ini jam 20:00 WITA!",
        "image_path": "images/episode_11.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_11.jpg",
        "image_prompt": "Giant garuda flying in rage over felled tree, flood water rushing through valley, dramatic lighting, masterpiece 8k"
    },
    {
        "id": 12,
        "arc": "Arc 3: Penebangan Pohon Keramat dan Bahtera Maut",
        "arc_change": False,
        "slot": "Hari 4 - Malam (20:00 WITA)",
        "title": "Mahakarya Bahtera Wakka Pasompe",
        "text": "Dari gelondongan kayu Welenrengnge, para empu kapal Bugis memahat bahtera perang legendaris bernama Wakka Pasompe. Setiap pasak ditiupkan mantra sakral, layarnya ditenun dari serat daun lontar pilihan. Perahu ini bukan sekadar kapal, melainkan istana terapung yang kebal badai. Saksikan keberangkatannya besok pagi jam 07:00 WITA!",
        "image_path": "images/episode_12.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_12.jpg",
        "image_prompt": "Ancient Bugis shipwrights carving massive warship Wakka Pasompe on sandy shore, golden sunset, masterpiece 8k"
    },
    {
        "id": 13,
        "arc": "Arc 3: Penebangan Pohon Keramat dan Bahtera Maut",
        "arc_change": False,
        "slot": "Hari 5 - Pagi (07:00 WITA)",
        "title": "Sumpah Keramat dan Sauh Diangkat",
        "text": "Sebelum berlayar, Sawerigading bersumpah di hadapan rakyat Luwu: \"Pantang kakiku kembali menyentuh tanah Luwu sebelum memboyong putri We Cudai ke sisiku!\" Genderang perang bertalu-talu, sauh diangkat, dan Wakka Pasompe membelah teluk Bone menuju samudra lepas yang liar. Pertarungan maut menanti siang ini jam 12:00 WITA!",
        "image_path": "images/episode_13.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_13.jpg",
        "image_prompt": "Sawerigading standing on departure dock making solemn oath, giant ship setting sail into sunrise, masterpiece 8k"
    },

    # ARC 4: Samudra Berdarah dan Penaklukan Tana Kelling
    {
        "id": 14,
        "arc": "Arc 4: Samudra Berdarah dan Penaklukan Tana Kelling",
        "arc_change": True,
        "slot": "Hari 5 - Siang (12:00 WITA)",
        "title": "Menerjang Badai Beracun dan Monster Samudra",
        "text": "[ARC 4: PERANG DI KELLING]\nSamudra ganas menyambut armada Luwu. Kabut beracun menutupi pandangan dan monster laut berkepala naga menyerang dari kedalaman pusaran air. Sawerigading berdiri kokoh di haluan, menghunus tombak pusaka dan menundukkan para penguasa kegelapan samudra. Daratan musuh mulai tampak malam ini jam 20:00 WITA!",
        "image_path": "images/episode_14.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_14.jpg",
        "image_prompt": "Sawerigading with golden spear on ship fighting giant sea monsters in stormy ocean waves, lightning, masterpiece 8k"
    },
    {
        "id": 15,
        "arc": "Arc 4: Samudra Berdarah dan Penaklukan Tana Kelling",
        "arc_change": False,
        "slot": "Hari 5 - Malam (20:00 WITA)",
        "title": "Panji Luwu Berkibar di Pantai Kelling",
        "text": "Armada Wakka Pasompe akhirnya berlabuh di pesisir Tana Kelling. Namun kedatangan ksatria Luwu disambut ribuan prajurit bersenjata panah api. Negeri ini tidak sudi tunduk pada orang asing. Panji perang Luwu dikibarkan tinggi-tinggi di tepi pantai yang berdarah. Saksikan perang penentuan besok pagi jam 07:00 WITA!",
        "image_path": "images/episode_15.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_15.jpg",
        "image_prompt": "Fleet landing on sandy beach of Tana Kelling, Bugis war flags, coastal defensive fortifications, masterpiece 8k"
    },
    {
        "id": 16,
        "arc": "Arc 4: Samudra Berdarah dan Penaklukan Tana Kelling",
        "arc_change": False,
        "slot": "Hari 6 - Pagi (07:00 WITA)",
        "title": "Pertempuran Sengit Meluluhkan Hati We Cudai",
        "text": "Putri We Cudai ternyata seorang panglima perang yang lihai. Pertempuran sengit berkecamuk antara benteng Kelling dan armada Sawerigading. Bukan kekerasan yang meruntuhkan pertahanan sang putri, melainkan ketulusan dan keberanian Sawerigading yang menyelamatkannya dari runtuhan gerbang istana. Cinta pun bertaut siang ini jam 12:00 WITA!",
        "image_path": "images/episode_16.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_16.jpg",
        "image_prompt": "Dramatic duel between warrior Sawerigading and warrior princess We Cudai, sunset battlefield, masterpiece 8k"
    },
    {
        "id": 17,
        "arc": "Arc 4: Samudra Berdarah dan Penaklukan Tana Kelling",
        "arc_change": False,
        "slot": "Hari 6 - Siang (12:00 WITA)",
        "title": "Pernikahan Agung dan Lahirnya I La Galigo",
        "text": "Kedua insan akhirnya bersanding dalam pesta pernikahan termegah dalam sejarah Nusantara. Dari persatuan ksatria Luwu dan putri Kelling, lahirlah seorang putra bernama I La Galigo. Anak inilah yang kelak tumbuh menjadi sang pujangga pengelana, mencatat setiap larik epos keluarganya. Masuki kisah petualangan sang putra malam ini jam 20:00 WITA!",
        "image_path": "images/episode_17.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_17.jpg",
        "image_prompt": "Grand royal wedding of Sawerigading and We Cudai in magnificent palace, newborn baby I La Galigo, masterpiece 8k"
    },

    # ARC 5: Petualangan Liar Sang Pewaris I La Galigo
    {
        "id": 18,
        "arc": "Arc 5: Petualangan Liar Sang Pewaris I La Galigo",
        "arc_change": True,
        "slot": "Hari 6 - Malam (20:00 WITA)",
        "title": "Jiwa Pemberontak I La Galigo",
        "text": "[ARC 5: SANG PEWARIS GALIGO]\nI La Galigo tidak mewarisi ketenangan ibunya. Ia pemuda yang rupawan, berdarah panas, dan gemar menentang aturan istana. Baginya, kehormatan lelaki diuji di medan petualangan bebas dan laga sabung ayam di tanah seberang. Ayahnya menatap sang putra dengan cemas. Ikuti laganya besok pagi jam 07:00 WITA!",
        "image_path": "images/episode_18.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_18.jpg",
        "image_prompt": "Young handsome rebel prince I La Galigo holding gamecock with ornate spurs, royal courtyard, masterpiece 8k"
    },
    {
        "id": 19,
        "arc": "Arc 5: Petualangan Liar Sang Pewaris I La Galigo",
        "arc_change": False,
        "slot": "Hari 7 - Pagi (07:00 WITA)",
        "title": "Sabung Ayam Legendaris di Sunra dan Wajo",
        "text": "I La Galigo mengembara hingga ke negeri Sunra dan Wajo. Di arena sabung ayam yang dihadiri para pangeran terkemuka, ayam jago aduannya yang diberi nama Bakka Lolona tak pernah terkalahkan. Taruhan emas dan intan mengalir, namun kemenangan itu memicu dendam membara dari para penguasa setempat. Simak pelarian asmaranya siang ini jam 12:00 WITA!",
        "image_path": "images/episode_19.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_19.jpg",
        "image_prompt": "Historic traditional cockfighting arena in ancient Bugis kingdom, cheering crowd, dramatic action, masterpiece 8k"
    },
    {
        "id": 20,
        "arc": "Arc 5: Petualangan Liar Sang Pewaris I La Galigo",
        "arc_change": False,
        "slot": "Hari 7 - Siang (12:00 WITA)",
        "title": "Pengembaraan Asmara Menjelajah Nusantara",
        "text": "Bukan hanya arena laga yang ditaklukkannya, pesona I La Galigo memikat banyak putri raja di pelbagai bandar pelabuhan. Ia menjalin asmara di Bontoala hingga Wadeng. Namun di balik kebebasannya, I La Galigo mulai menggoreskan pena lontar, mencatat riwayat tanah leluhurnya dengan syair-syair indah. Lahirnya cucu mahkota malam ini jam 20:00 WITA!",
        "image_path": "images/episode_20.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_20.jpg",
        "image_prompt": "I La Galigo writing on lontar palm leaf manuscript by candle light in a wooden ship cabin, masterpiece 8k"
    },
    {
        "id": 21,
        "arc": "Arc 5: Petualangan Liar Sang Pewaris I La Galigo",
        "arc_change": False,
        "slot": "Hari 7 - Malam (20:00 WITA)",
        "title": "Lahirnya La Tenritatta sang Penyeimbang",
        "text": "Dari hubungan asmara I La Galigo, lahirlah seorang putra bernama La Tenritatta. Berbeda dengan ayahnya yang liar, La Tenritatta memiliki budi pekerti luhur dan kebijaksanaan kakeknya, Sawerigading. Ia dipersiapkan menjadi pemimpin generasi ketiga yang akan menjaga keseimbangan jagat. Masuki babak kerinduan sang kakek besok pagi jam 07:00 WITA!",
        "image_path": "images/episode_21.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_21.jpg",
        "image_prompt": "Wise royal child La Tenritatta blessed by elder priests, golden royal nursery, masterpiece 8k"
    },

    # ARC 6: Perjalanan Terakhir dan Tenggelamnya Bahtera
    {
        "id": 22,
        "arc": "Arc 6: Perjalanan Terakhir dan Tenggelamnya Bahtera",
        "arc_change": True,
        "slot": "Hari 8 - Pagi (07:00 WITA)",
        "title": "Kerinduan Membara Sawerigading Menatap Luwu",
        "text": "[ARC 6: SAMUDRA TERAKHIR]\nPuluhan tahun berlalu di negeri asing, Sawerigading yang mulai sepuh dicekam kerinduan mendalam pada Luwu. Namun sumpahnya mengikat erat: ia tak boleh menginjak daratan Luwu. Maka ia melayarkan kembali Wakka Pasompe ke perairan teluk Bone, sekadar ingin menatap bukit kelahirannya dari jauh. Simak pertemuan haru siang ini jam 12:00 WITA!",
        "image_path": "images/episode_22.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_22.jpg",
        "image_prompt": "Elder warrior Sawerigading gazing with longing at coastal mountains of Luwu from deck of his ship, masterpiece 8k"
    },
    {
        "id": 23,
        "arc": "Arc 6: Perjalanan Terakhir dan Tenggelamnya Bahtera",
        "arc_change": False,
        "slot": "Hari 8 - Siang (12:00 WITA)",
        "title": "Pertemuan Rahasia di Atas Teluk Bone",
        "text": "Mendengar kedatangan sang saudara kembar, We Tenriabeng turun ke laut menggunakan perahu kecil beratap sutra. Tanpa menyentuh daratan Luwu, kedua kembar emas ini bertemu di atas gelombang teluk Bone. Air mata haru mengalir setelah puluhan tahun terpisah. Namun langit mendadak berubah hitam pekat! Petaka besar menghadang malam ini jam 20:00 WITA!",
        "image_path": "images/episode_23.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_23.jpg",
        "image_prompt": "Tearful reunion of Sawerigading and We Tenriabeng between two traditional boats on calm sea, emotional, masterpiece 8k"
    },
    {
        "id": 24,
        "arc": "Arc 6: Perjalanan Terakhir dan Tenggelamnya Bahtera",
        "arc_change": False,
        "slot": "Hari 8 - Malam (20:00 WITA)",
        "title": "Gelombang Dahsyat Murka Kosmis",
        "text": "Pelanggaran jarak antara sepasang kembar emas membangkitkan kembali kutukan kuno dewata. Angin puting beliung menderu membelah langit, kilat menyambar tiang layar Wakka Pasompe, dan laut terbelah menciptakan pusaran air raksasa tak berdasar. Bahtera megah dari kayu Welenrengnge mulai terseret pusaran! Simak detik tenggelamnya besok pagi jam 07:00 WITA!",
        "image_path": "images/episode_24.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_24.jpg",
        "image_prompt": "Massive cosmic whirlpool sucking giant ship into abyss, apocalyptic sea storm, lightning breaking clouds, masterpiece 8k"
    },
    {
        "id": 25,
        "arc": "Arc 6: Perjalanan Terakhir dan Tenggelamnya Bahtera",
        "arc_change": False,
        "slot": "Hari 9 - Pagi (07:00 WITA)",
        "title": "Tenggelamnya Wakka Pasompe ke Dasar Uriq Liu",
        "text": "Dengan tenang Sawerigading menggenggam tangan We Cudai. Wakka Pasompe tenggelam perlahan ke dasar samudra terdalam, Uriq Liu. Namun ini bukan kematian, melainkan perpindahan alam menuju keabadian. Bahtera sakral itu lenyap dari muka bumi Ale Lino, menuju singgasana para dewa bawah laut. Masuki takhta abadi siang ini jam 12:00 WITA!",
        "image_path": "images/episode_25.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_25.jpg",
        "image_prompt": "Ship gently descending into glowing luminous underwater kingdom of Uriq Liu, mythical sea palace, masterpiece 8k"
    },

    # ARC 7: Kembalinya Para Dewata dan Penutupan Epos
    {
        "id": 26,
        "arc": "Arc 7: Kembalinya Para Dewata dan Penutupan Epos",
        "arc_change": True,
        "slot": "Hari 9 - Siang (12:00 WITA)",
        "title": "Takhta Abadi di Puncak Langit dan Dasar Laut",
        "text": "[ARC 7: AKHIR ZAMAN DEWATA]\nTakdir kosmis digenapi. Sawerigading dan We Cudai bertahta abadi sebagai penguasa dunia bawah laut Uriq Liu. Sementara We Tenriabeng diangkat kembali ke puncak kahyangan tertinggi Boting Langiq. Keseimbangan jagat raya yang sempat terancam runtuh kini kokoh selamanya. Penobatan raja manusia malam ini jam 20:00 WITA!",
        "image_path": "images/episode_26.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_26.jpg",
        "image_prompt": "Cosmic balance, divine throne underwater and divine throne in celestial heavens glowing together, masterpiece 8k"
    },
    {
        "id": 27,
        "arc": "Arc 7: Kembalinya Para Dewata dan Penutupan Epos",
        "arc_change": False,
        "slot": "Hari 9 - Malam (20:00 WITA)",
        "title": "Penobatan La Tenritatta Memimpin Manusia Bumi",
        "text": "Di bumi Ale Lino, sang cucu La Tenritatta dinobatkan menjadi Datu Luwu. Tidak ada lagi dewa yang turun langsung campur tangan. Manusia kini belajar berdikari berbekal nilai siriq na pesse, kejujuran, dan adat kesopanan warisan para leluhur dewa. Puncak penutupan kitab naskah lontar terpanjang dunia akan kita ulas besok pagi jam 07:00 WITA!",
        "image_path": "images/episode_27.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_27.jpg",
        "image_prompt": "Coronation of mortal king La Tenritatta holding ceremonial sword in Luwu throne room, sunrise, masterpiece 8k"
    },
    {
        "id": 28,
        "arc": "Arc 7: Kembalinya Para Dewata dan Penutupan Epos",
        "arc_change": False,
        "slot": "Hari 10 - Pagi (07:00 WITA)",
        "title": "Pamitnya Dewata dan Mahakarya Abadi Lontar",
        "text": "Para dewata pamit kembali ke alam asal, pintu langit dan dasar samudra tertutup rapat. Berakhirlah wiracarita agung Sureq Galigo. Warisan 300.000 larik naskah ini adalah saksi kebesaran sastra Nusantara yang diakui UNESCO. Di antara seluruh kisah Sawerigading hingga I La Galigo, babak mana yang paling berkesan dan menggetarkan jiwamu? Tuliskan pendapatmu di kolom komentar!",
        "image_path": "images/episode_28.jpg",
        "image_raw_url": "https://raw.githubusercontent.com/AlchemiztGOd/threads-galigo-bot/main/images/episode_28.jpg",
        "image_prompt": "Ancient sacred lontar palm leaf manuscripts glowing with divine golden light in museum library, epic closing tribute, masterpiece 8k"
    }
]

print(f"Total episode yang disiapkan: {len(saga)}")
valid = True
for ep in saga:
    t = ep["text"]
    char_len = len(t)
    has_em = ("—" in t) or ("--" in t)
    if char_len > 450 or has_em:
        print(f"FAILED Ep {ep['id']}: len={char_len}, em={has_em}")
        valid = False
    else:
        print(f"OK Ep {ep['id']:02d} [{ep['slot']}]: {char_len} char | Arc: {ep['arc'][:25]}...")

if valid:
    print("\nSEMUA 28 EPISODE LOLOS VALIDASI ANTISLOP DAN BATAS KARAKTER!")
