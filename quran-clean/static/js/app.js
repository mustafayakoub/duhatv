// ═══════════════════════════════════════════════════════════════
// 📖 Quran Clean - JavaScript Application
// ═══════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────
// الحالة العامة للتطبيق
// ─────────────────────────────────────────────────────────────

const AppState = {
    surahs: [],
    currentSurah: null,
    currentAyahs: [],
    textType: 'text_uthmani',
    fontSize: 28,
    fontFamily: 'UthmanicHafs_V22',
    showIrab: true,
    showMeaning: true
};

// ═══════════════════════════════════════════════════════════════
// تحميل البيانات الأولية
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', async () => {
    await loadSurahs();
    setupEventListeners();
    loadSettings();
    loadStats();
});

// ─────────────────────────────────────────────────────────────
// تحميل السور
// ─────────────────────────────────────────────────────────────

async function loadSurahs() {
    try {
        const response = await fetch('/api/surahs');
        const surahs = await response.json();

        AppState.surahs = surahs;

        const select = document.getElementById('surahSelect');
        select.innerHTML = '<option value="">اختر سورة...</option>';

        surahs.forEach(surah => {
            const option = document.createElement('option');
            option.value = surah.id;
            option.textContent = `${surah.id}. ${surah.name_ar} (${surah.ayah_count} آية)`;
            select.appendChild(option);
        });

    } catch (error) {
        console.error('خطأ في تحميل السور:', error);
        showError('فشل تحميل السور');
    }
}

// ─────────────────────────────────────────────────────────────
// تحميل آيات سورة
// ─────────────────────────────────────────────────────────────

async function loadSurahAyahs(surahId) {
    const container = document.getElementById('ayahsContainer');
    container.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>جاري التحميل...</p></div>';

    try {
        // تحميل معلومات السورة
        const surahResponse = await fetch(`/api/surah/${surahId}`);
        const surah = await surahResponse.json();
        AppState.currentSurah = surah;

        // تحميل الآيات
        const ayahsResponse = await fetch(`/api/ayahs?surah_id=${surahId}&text_type=${AppState.textType}`);
        const ayahs = await ayahsResponse.json();
        AppState.currentAyahs = ayahs;

        // عرض معلومات السورة
        displaySurahInfo(surah);

        // عرض الآيات
        displayAyahs(ayahs);

        // عرض أزرار التنقل
        displayNavigation(surahId);

    } catch (error) {
        console.error('خطأ في تحميل الآيات:', error);
        showError('فشل تحميل الآيات');
    }
}

// ─────────────────────────────────────────────────────────────
// عرض معلومات السورة
// ─────────────────────────────────────────────────────────────

function displaySurahInfo(surah) {
    const infoDiv = document.getElementById('surahInfo');
    const nameEl = document.getElementById('surahName');
    const detailsEl = document.getElementById('surahDetails');

    nameEl.textContent = `سورة ${surah.name_ar}`;
    detailsEl.textContent = `${surah.revelation_place} • ${surah.ayah_count} آية • ${surah.category || ''}`;

    infoDiv.style.display = 'block';
}

// ─────────────────────────────────────────────────────────────
// عرض الآيات
// ─────────────────────────────────────────────────────────────

function displayAyahs(ayahs) {
    const container = document.getElementById('ayahsContainer');

    if (!ayahs || ayahs.length === 0) {
        container.innerHTML = '<div class="loading-state"><p>لا توجد آيات</p></div>';
        return;
    }

    container.innerHTML = '';

    ayahs.forEach(ayah => {
        const ayahDiv = document.createElement('div');
        ayahDiv.className = 'ayah';
        ayahDiv.dataset.surahId = ayah.surah_id;
        ayahDiv.dataset.ayahId = ayah.ayah_id;

        const ayahNumber = document.createElement('span');
        ayahNumber.className = 'ayah-number';
        ayahNumber.textContent = ayah.ayah_id;

        const ayahText = document.createElement('p');
        ayahText.className = 'ayah-text';
        ayahText.style.fontFamily = AppState.fontFamily;
        ayahText.style.fontSize = `${AppState.fontSize}px`;
        ayahText.innerHTML = ayah.text || '[ نص غير متوفر ]';

        ayahDiv.appendChild(ayahNumber);
        ayahDiv.appendChild(ayahText);

        container.appendChild(ayahDiv);
    });

    // إضافة أحداث النقر على الكلمات
    addWordClickEvents();
}

// ─────────────────────────────────────────────────────────────
// إضافة أحداث النقر على الكلمات
// ─────────────────────────────────────────────────────────────

function addWordClickEvents() {
    const ayahs = document.querySelectorAll('.ayah');

    ayahs.forEach(ayahDiv => {
        const ayahText = ayahDiv.querySelector('.ayah-text');
        const surahId = ayahDiv.dataset.surahId;
        const ayahId = ayahDiv.dataset.ayahId;

        // تقسيم النص إلى كلمات
        const text = ayahText.textContent;
        const words = text.split(/\s+/);

        ayahText.innerHTML = '';

        words.forEach((word, index) => {
            const wordSpan = document.createElement('span');
            wordSpan.className = 'word';
            wordSpan.textContent = word;
            wordSpan.dataset.surahId = surahId;
            wordSpan.dataset.ayahId = ayahId;
            wordSpan.dataset.wordIndex = index + 1;

            wordSpan.addEventListener('click', () => showWordDetails(surahId, ayahId, index + 1));

            ayahText.appendChild(wordSpan);

            if (index < words.length - 1) {
                ayahText.appendChild(document.createTextNode(' '));
            }
        });
    });
}

// ─────────────────────────────────────────────────────────────
// عرض تفاصيل الكلمة
// ─────────────────────────────────────────────────────────────

async function showWordDetails(surahId, ayahId, wordIndex) {
    if (!AppState.showIrab && !AppState.showMeaning) {
        return;
    }

    try {
        const response = await fetch(`/api/words?surah_id=${surahId}&ayah_id=${ayahId}`);
        const words = await response.json();

        const word = words[wordIndex - 1];

        if (!word) {
            return;
        }

        const modal = document.getElementById('wordModal');
        const title = document.getElementById('wordModalTitle');
        const details = document.getElementById('wordDetails');

        title.textContent = word.word_text;

        let html = '';

        if (word.word_imlaei1) {
            html += `<p><strong>الكلمة (إملائي):</strong> ${word.word_imlaei1}</p>`;
        }

        if (word.root) {
            html += `<p><strong>الجذر:</strong> ${word.root}</p>`;
        }

        if (AppState.showMeaning && word.meaning) {
            html += `<h4>المعنى</h4><p>${word.meaning}</p>`;
        }

        if (AppState.showIrab && word.irab) {
            html += `<h4>الإعراب</h4><p>${word.irab}</p>`;
        }

        if (word.sarf) {
            html += `<h4>الصرف</h4><p>${word.sarf}</p>`;
        }

        if (word.rasm && word.rasm !== '-') {
            html += `<h4>الرسم القرآني</h4><p>${word.rasm}</p>`;
        }

        details.innerHTML = html || '<p>لا توجد تفاصيل متاحة</p>';

        modal.classList.add('active');

    } catch (error) {
        console.error('خطأ في تحميل تفاصيل الكلمة:', error);
    }
}

// ─────────────────────────────────────────────────────────────
// عرض أزرار التنقل
// ─────────────────────────────────────────────────────────────

function displayNavigation(currentSurahId) {
    const nav = document.getElementById('navigation');
    const prevBtn = document.getElementById('prevSurahBtn');
    const nextBtn = document.getElementById('nextSurahBtn');

    nav.style.display = 'flex';

    prevBtn.disabled = currentSurahId <= 1;
    nextBtn.disabled = currentSurahId >= 114;

    prevBtn.onclick = () => {
        if (currentSurahId > 1) {
            document.getElementById('surahSelect').value = currentSurahId - 1;
            loadSurahAyahs(currentSurahId - 1);
        }
    };

    nextBtn.onclick = () => {
        if (currentSurahId < 114) {
            document.getElementById('surahSelect').value = currentSurahId + 1;
            loadSurahAyahs(currentSurahId + 1);
        }
    };
}

// ═══════════════════════════════════════════════════════════════
// البحث
// ═══════════════════════════════════════════════════════════════

async function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    const searchType = document.querySelector('input[name="searchType"]:checked').value;

    if (!query) {
        alert('الرجاء إدخال نص البحث');
        return;
    }

    const resultsDiv = document.getElementById('searchResults');
    resultsDiv.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>جاري البحث...</p></div>';

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&type=${searchType}&text_type=${AppState.textType}`);
        const data = await response.json();

        displaySearchResults(data);

    } catch (error) {
        console.error('خطأ في البحث:', error);
        resultsDiv.innerHTML = '<p>فشل البحث. حاول مرة أخرى.</p>';
    }
}

// ─────────────────────────────────────────────────────────────
// عرض نتائج البحث
// ─────────────────────────────────────────────────────────────

function displaySearchResults(data) {
    const resultsDiv = document.getElementById('searchResults');

    if (!data.results || data.results.length === 0) {
        resultsDiv.innerHTML = '<p>لا توجد نتائج</p>';
        return;
    }

    resultsDiv.innerHTML = `<p>عدد النتائج: ${data.count}</p>`;

    data.results.forEach(result => {
        const item = document.createElement('div');
        item.className = 'search-result-item';

        const text = document.createElement('div');
        text.className = 'search-result-text';
        text.textContent = result.text || result.word_text || '';

        const meta = document.createElement('div');
        meta.className = 'search-result-meta';
        meta.textContent = `سورة ${result.surah_name} - آية ${result.ayah_id}`;

        item.appendChild(text);
        item.appendChild(meta);

        item.onclick = () => {
            closeModal('searchModal');
            document.getElementById('surahSelect').value = result.surah_id;
            loadSurahAyahs(result.surah_id);
        };

        resultsDiv.appendChild(item);
    });
}

// ═══════════════════════════════════════════════════════════════
// الإحصائيات
// ═══════════════════════════════════════════════════════════════

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();

        const statsDiv = document.getElementById('appStats');
        statsDiv.innerHTML = `
            <p><strong>إحصائيات التطبيق:</strong></p>
            <p>• عدد السور: ${stats.surahs_count}</p>
            <p>• عدد الآيات: ${stats.ayahs_count}</p>
            <p>• عدد الكلمات: ${stats.words_count}</p>
            <p>• عدد الجذور: ${stats.roots_count}</p>
        `;

    } catch (error) {
        console.error('خطأ في تحميل الإحصائيات:', error);
    }
}

// ═══════════════════════════════════════════════════════════════
// إدارة النوافذ المنبثقة (Modals)
// ═══════════════════════════════════════════════════════════════

function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// ═══════════════════════════════════════════════════════════════
// إعداد الأحداث
// ═══════════════════════════════════════════════════════════════

function setupEventListeners() {
    // اختيار السورة
    document.getElementById('surahSelect').addEventListener('change', (e) => {
        const surahId = parseInt(e.target.value);
        if (surahId) {
            loadSurahAyahs(surahId);
        }
    });

    // اختيار النمط/القراءة
    document.getElementById('textTypeSelect').addEventListener('change', (e) => {
        AppState.textType = e.target.value;
        saveSettings();

        if (AppState.currentSurah) {
            loadSurahAyahs(AppState.currentSurah.id);
        }
    });

    // اختيار الخط
    document.getElementById('fontSelect').addEventListener('change', (e) => {
        AppState.fontFamily = e.target.value;
        saveSettings();

        document.querySelectorAll('.ayah-text').forEach(el => {
            el.style.fontFamily = AppState.fontFamily;
        });
    });

    // تغيير حجم الخط
    document.getElementById('fontSizeRange').addEventListener('input', (e) => {
        AppState.fontSize = parseInt(e.target.value);
        document.getElementById('fontSizeLabel').textContent = AppState.fontSize;
        saveSettings();

        document.querySelectorAll('.ayah-text').forEach(el => {
            el.style.fontSize = `${AppState.fontSize}px`;
        });
    });

    // أزرار الهيدر
    document.getElementById('searchBtn').addEventListener('click', () => openModal('searchModal'));
    document.getElementById('settingsBtn').addEventListener('click', () => openModal('settingsModal'));
    document.getElementById('infoBtn').addEventListener('click', () => openModal('infoModal'));

    // زر البحث
    document.getElementById('performSearchBtn').addEventListener('click', performSearch);

    // Enter في حقل البحث
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    // أزرار إغلاق النوافذ
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modalId = e.target.dataset.modal;
            closeModal(modalId);
        });
    });

    // إغلاق النافذة بالنقر خارجها
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });

    // إعدادات العرض
    document.getElementById('showIrabCheckbox').addEventListener('change', (e) => {
        AppState.showIrab = e.target.checked;
        saveSettings();
    });

    document.getElementById('showMeaningCheckbox').addEventListener('change', (e) => {
        AppState.showMeaning = e.target.checked;
        saveSettings();
    });

    // الوضع الليلي
    document.getElementById('darkModeCheckbox').addEventListener('change', (e) => {
        if (e.target.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'true');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'false');
        }
    });
}

// ═══════════════════════════════════════════════════════════════
// حفظ واستعادة الإعدادات
// ═══════════════════════════════════════════════════════════════

function saveSettings() {
    localStorage.setItem('quran_settings', JSON.stringify({
        textType: AppState.textType,
        fontSize: AppState.fontSize,
        fontFamily: AppState.fontFamily,
        showIrab: AppState.showIrab,
        showMeaning: AppState.showMeaning
    }));
}

function loadSettings() {
    const saved = localStorage.getItem('quran_settings');

    if (saved) {
        const settings = JSON.parse(saved);
        AppState.textType = settings.textType || 'text_uthmani';
        AppState.fontSize = settings.fontSize || 28;
        AppState.fontFamily = settings.fontFamily || 'UthmanicHafs_V22';
        AppState.showIrab = settings.showIrab !== false;
        AppState.showMeaning = settings.showMeaning !== false;

        document.getElementById('textTypeSelect').value = AppState.textType;
        document.getElementById('fontSizeRange').value = AppState.fontSize;
        document.getElementById('fontSizeLabel').textContent = AppState.fontSize;
        document.getElementById('fontSelect').value = AppState.fontFamily;
        document.getElementById('showIrabCheckbox').checked = AppState.showIrab;
        document.getElementById('showMeaningCheckbox').checked = AppState.showMeaning;
    }

    // الوضع الليلي
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
        document.getElementById('darkModeCheckbox').checked = true;
    }
}

// ═══════════════════════════════════════════════════════════════
// دوال مساعدة
// ═══════════════════════════════════════════════════════════════

function showError(message) {
    const container = document.getElementById('ayahsContainer');
    container.innerHTML = `
        <div class="loading-state">
            <p style="color: #ff4444;">❌ ${message}</p>
        </div>
    `;
}

console.log('📖 Quran Clean - تم تحميل التطبيق بنجاح');
