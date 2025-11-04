// حالة التطبيق
const state = {
    currentSurah: null,
    currentVersion: 'hafs_smart_v8',
    fontSize: 28,
    fontFamily: 'uthmanic-hafs-v22',
    viewMode: 'mushaf',
    nightMode: false
};

// عناصر DOM
const elements = {
    sidebar: document.getElementById('sidebar'),
    surahsList: document.getElementById('surahsList'),
    ayahsContainer: document.getElementById('ayahsContainer'),
    searchInput: document.getElementById('searchInput'),
    searchResults: document.getElementById('searchResults'),
    fontSelect: document.getElementById('fontSelect'),
    versionSelect: document.getElementById('versionSelect'),
    fontSizeRange: document.getElementById('fontSizeRange'),
    fontSizeValue: document.getElementById('fontSizeValue'),
    viewMode: document.getElementById('viewMode'),
    toggleNight: document.getElementById('toggleNight'),
    openSidebar: document.getElementById('openSidebar'),
    closeSidebar: document.getElementById('closeSidebar'),
    headerStats: document.getElementById('headerStats'),
    totalAyahs: document.getElementById('totalAyahs'),
    totalWords: document.getElementById('totalWords'),
    totalLetters: document.getElementById('totalLetters')
};

// تحميل البيانات الأولية
async function init() {
    await loadStats();
    await loadVersions();
    await loadSurahs();
    setupEventListeners();
}

// تحميل القراءات المتاحة
async function loadVersions() {
    try {
        const response = await fetch('/api/versions');
        const versions = await response.json();

        elements.versionSelect.innerHTML = '';

        versions.forEach(version => {
            const option = document.createElement('option');
            option.value = version.code;
            option.textContent = `${version.name_ar} (${version.qiraa})`;
            if (version.is_default) {
                option.selected = true;
                state.currentVersion = version.code;
            }
            elements.versionSelect.appendChild(option);
        });
    } catch (error) {
        console.error('خطأ في تحميل القراءات:', error);
        elements.versionSelect.innerHTML = '<option>خطأ في التحميل</option>';
    }
}

// تحميل الإحصائيات
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();

        elements.totalAyahs.textContent = stats.total_ayahs.toLocaleString('ar');
        elements.totalWords.textContent = stats.total_words.toLocaleString('ar');
        elements.totalLetters.textContent = stats.total_letters.toLocaleString('ar');
    } catch (error) {
        console.error('خطأ في تحميل الإحصائيات:', error);
    }
}

// تحميل قائمة السور
async function loadSurahs() {
    try {
        const response = await fetch('/api/surahs');
        const surahs = await response.json();

        elements.surahsList.innerHTML = surahs.map(surah => `
            <div class="surah-item" data-surah="${surah.number}">
                <div class="surah-number">${surah.number}</div>
                <div class="surah-info">
                    <div class="surah-name">${surah.name}</div>
                    <div class="surah-meta">${surah.ayah_count} آية</div>
                </div>
            </div>
        `).join('');

        // إضافة أحداث النقر
        document.querySelectorAll('.surah-item').forEach(item => {
            item.addEventListener('click', () => {
                const surahNo = parseInt(item.dataset.surah);
                loadSurah(surahNo);
            });
        });

    } catch (error) {
        console.error('خطأ في تحميل السور:', error);
        elements.surahsList.innerHTML = '<div class="loading">خطأ في التحميل</div>';
    }
}

// تحميل سورة معينة
async function loadSurah(surahNo) {
    try {
        state.currentSurah = surahNo;

        // تحديث الواجهة
        document.querySelectorAll('.surah-item').forEach(item => {
            item.classList.toggle('active', parseInt(item.dataset.surah) === surahNo);
        });

        elements.ayahsContainer.innerHTML = '<div class="loading">جاري التحميل...</div>';

        const response = await fetch(`/api/surah/${surahNo}?version=${state.currentVersion}`);
        const ayahs = await response.json();

        displayAyahs(ayahs);

        // إغلاق القائمة على الموبايل
        if (window.innerWidth <= 768) {
            elements.sidebar.classList.add('closed');
            elements.openSidebar.style.display = 'block';
        }

    } catch (error) {
        console.error('خطأ في تحميل السورة:', error);
        elements.ayahsContainer.innerHTML = '<div class="loading">خطأ في التحميل</div>';
    }
}

// عرض الآيات
function displayAyahs(ayahs) {
    if (!ayahs || ayahs.length === 0) {
        elements.ayahsContainer.innerHTML = '<div class="loading">لا توجد آيات</div>';
        return;
    }

    const surahName = ayahs[0].sura_no === 1 ? 'الفاتحة' : 'البقرة';

    let html = `
        <div class="surah-header">
            <h2 class="surah-title">سورة ${surahName}</h2>
        </div>
    `;

    // إضافة البسملة (ما عدا سورة التوبة)
    if (ayahs[0].sura_no !== 9) {
        html += `<div class="surah-basmala">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>`;
    }

    if (state.viewMode === 'mushaf') {
        html += '<div class="ayahs-mushaf">';
        ayahs.forEach(ayah => {
            html += `
                <span class="ayah">${ayah.text || ayah.text_emlaey}</span>
                <span class="ayah-number">${ayah.aya_no}</span>
            `;
        });
        html += '</div>';
    } else if (state.viewMode === 'list') {
        ayahs.forEach(ayah => {
            html += `
                <div class="ayah-item">
                    <span class="ayah-number">${ayah.aya_no}</span>
                    <div class="ayah-text">${ayah.text || ayah.text_emlaey}</div>
                </div>
            `;
        });
    } else if (state.viewMode === 'card') {
        ayahs.forEach(ayah => {
            html += `
                <div class="ayah-item">
                    <div class="ayah-number">${ayah.aya_no}</div>
                    <div class="ayah-text">${ayah.text || ayah.text_emlaey}</div>
                </div>
            `;
        });
    }

    elements.ayahsContainer.innerHTML = html;
    elements.ayahsContainer.className = `ayahs-container ${state.viewMode}-view`;

    updateFontSettings();
}

// البحث
let searchTimeout;
elements.searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    const query = e.target.value.trim();

    if (query.length < 2) {
        elements.searchResults.classList.remove('show');
        return;
    }

    searchTimeout = setTimeout(async () => {
        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();

            if (results.length === 0) {
                elements.searchResults.innerHTML = '<div class="search-result-item">لا توجد نتائج</div>';
            } else {
                elements.searchResults.innerHTML = results.map(result => `
                    <div class="search-result-item" data-surah="${result.sura_no}">
                        <div class="search-result-text">${result.text || result.text_emlaey}</div>
                        <div class="search-result-meta">سورة ${result.sura_no === 1 ? 'الفاتحة' : 'البقرة'} - الآية ${result.aya_no}</div>
                    </div>
                `).join('');

                // أحداث النقر على النتائج
                elements.searchResults.querySelectorAll('.search-result-item').forEach(item => {
                    item.addEventListener('click', () => {
                        const surahNo = parseInt(item.dataset.surah);
                        loadSurah(surahNo);
                        elements.searchResults.classList.remove('show');
                        elements.searchInput.value = '';
                    });
                });
            }

            elements.searchResults.classList.add('show');

        } catch (error) {
            console.error('خطأ في البحث:', error);
        }
    }, 300);
});

// إغلاق نتائج البحث عند النقر خارجها
document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-box')) {
        elements.searchResults.classList.remove('show');
    }
});

// تحديث إعدادات الخط
function updateFontSettings() {
    const ayahElements = document.querySelectorAll('.ayah, .ayah-text');
    const fontMap = {
        // خطوط عثمانية
        'uthmanic-hafs-v22': "'Uthmanic Hafs V22', serif",
        'uthmanic-hafs-v18': "'Uthmanic Hafs V18', serif",
        'uthman-tn': "'Uthman TN', serif",
        'uthman-tn1': "'Uthman TN1', serif",

        // خطوط كوفية
        'kfgqpc-kufi-ext': "'KFGQPC Kufi Extended', serif",
        'kfgqpc-kufi-sty': "'KFGQPC Kufi Style', serif",
        'dq7-kfi': "'DQ7 KFI', serif",

        // خطوط أخرى
        'aljalil': "'AlJalil', serif",
        'aljalil-dot': "'AlJalilDot', serif",
        'kfgqpc-an': "'KFGQPC An', sans-serif",
        'kfgqpc-an-light': "'KFGQPC An Light', sans-serif",

        // خطوط ويب
        'amiri': "'Amiri', serif",
        'cairo': "'Cairo', sans-serif",
        'scheherazade': "'Scheherazade New', serif"
    };

    ayahElements.forEach(el => {
        el.style.fontFamily = fontMap[state.fontFamily];
        el.style.fontSize = `${state.fontSize}px`;
    });

    document.documentElement.style.setProperty('--ayah-font-size', `${state.fontSize}px`);
}

// إعدادات الخط
elements.fontSelect.addEventListener('change', (e) => {
    state.fontFamily = e.target.value;
    updateFontSettings();
});

elements.fontSizeRange.addEventListener('input', (e) => {
    state.fontSize = parseInt(e.target.value);
    elements.fontSizeValue.textContent = state.fontSize;
    updateFontSettings();
});

// اختيار القراءة
elements.versionSelect.addEventListener('change', (e) => {
    state.currentVersion = e.target.value;
    if (state.currentSurah) {
        loadSurah(state.currentSurah);
    }
});

// طريقة العرض
elements.viewMode.addEventListener('change', (e) => {
    state.viewMode = e.target.value;
    if (state.currentSurah) {
        loadSurah(state.currentSurah);
    }
});

// الوضع الليلي
elements.toggleNight.addEventListener('click', () => {
    state.nightMode = !state.nightMode;
    document.body.classList.toggle('night-mode');
    elements.toggleNight.textContent = state.nightMode ? '☀️ الوضع النهاري' : '🌙 الوضع الليلي';
});

// القائمة الجانبية (موبايل)
elements.openSidebar.addEventListener('click', () => {
    elements.sidebar.classList.remove('closed');
    elements.openSidebar.style.display = 'none';
});

elements.closeSidebar.addEventListener('click', () => {
    elements.sidebar.classList.add('closed');
    elements.openSidebar.style.display = 'block';
});

// Responsive
function handleResize() {
    if (window.innerWidth > 768) {
        elements.sidebar.classList.remove('closed');
        elements.openSidebar.style.display = 'none';
    } else {
        elements.sidebar.classList.add('closed');
        elements.openSidebar.style.display = 'block';
    }
}

window.addEventListener('resize', handleResize);
handleResize();

// إعداد مستمعي الأحداث
function setupEventListeners() {
    // تم إعدادها أعلاه
}

// تهيئة التطبيق عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', init);
