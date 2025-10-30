#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🚀 تثبيت قاعدة البيانات القرآنية الهرمية على Linux
# Quran Hierarchical Database Installation Script for Linux
# ═══════════════════════════════════════════════════════════════

set -e  # إيقاف التنفيذ عند أي خطأ

# الألوان للطباعة
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════
# الإعدادات
# ═══════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_DIR="$SCRIPT_DIR/sql"
DB_NAME="quran_hierarchical_db"
DB_USER="${PGUSER:-postgres}"
DB_HOST="${PGHOST:-localhost}"
DB_PORT="${PGPORT:-5432}"

# ═══════════════════════════════════════════════════════════════
# دوال المساعدة
# ═══════════════════════════════════════════════════════════════

print_header() {
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════"
    echo "$1"
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# ═══════════════════════════════════════════════════════════════
# التحقق من المتطلبات
# ═══════════════════════════════════════════════════════════════

check_requirements() {
    print_header "🔍 التحقق من المتطلبات"

    # التحقق من PostgreSQL
    if ! command -v psql &> /dev/null; then
        print_error "PostgreSQL غير مثبت"
        print_info "قم بتثبيته باستخدام:"
        echo "  Ubuntu/Debian: sudo apt-get install postgresql-15 postgresql-contrib"
        echo "  CentOS/RHEL: sudo yum install postgresql15-server postgresql15-contrib"
        echo "  Arch Linux: sudo pacman -S postgresql"
        exit 1
    fi
    print_success "PostgreSQL مثبت"

    # التحقق من pgvector
    if ! psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -c "SELECT * FROM pg_available_extensions WHERE name='vector';" -t 2>/dev/null | grep -q vector; then
        print_warning "pgvector غير مثبت - سيتم تثبيته الآن"
        install_pgvector
    else
        print_success "pgvector مثبت"
    fi

    # التحقق من الملفات SQL
    if [ ! -d "$SQL_DIR" ]; then
        print_error "مجلد SQL غير موجود: $SQL_DIR"
        exit 1
    fi

    for file in "01_setup.sql" "02_level0_core_tables.sql" "03_remaining_levels.sql" "04_views_and_functions.sql"; do
        if [ ! -f "$SQL_DIR/$file" ]; then
            print_error "الملف غير موجود: $SQL_DIR/$file"
            exit 1
        fi
    done
    print_success "جميع ملفات SQL موجودة"

    echo ""
}

# ═══════════════════════════════════════════════════════════════
# تثبيت pgvector
# ═══════════════════════════════════════════════════════════════

install_pgvector() {
    print_header "📦 تثبيت pgvector"

    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    print_info "جاري تنزيل pgvector..."
    git clone https://github.com/pgvector/pgvector.git
    cd pgvector

    print_info "جاري الترجمة..."
    make

    print_info "جاري التثبيت..."
    sudo make install

    cd "$SCRIPT_DIR"
    rm -rf "$TEMP_DIR"

    print_success "تم تثبيت pgvector بنجاح"
    echo ""
}

# ═══════════════════════════════════════════════════════════════
# تنفيذ السكريبتات
# ═══════════════════════════════════════════════════════════════

execute_sql_file() {
    local file=$1
    local description=$2
    local database=$3

    print_info "$description..."

    if [ -z "$database" ]; then
        if psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -f "$SQL_DIR/$file"; then
            print_success "تم بنجاح: $file"
        else
            print_error "فشل في: $file"
            exit 1
        fi
    else
        if psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$database" -f "$SQL_DIR/$file"; then
            print_success "تم بنجاح: $file"
        else
            print_error "فشل في: $file"
            exit 1
        fi
    fi
    echo ""
}

# ═══════════════════════════════════════════════════════════════
# البرنامج الرئيسي
# ═══════════════════════════════════════════════════════════════

main() {
    print_header "🚀 بدء تثبيت قاعدة البيانات القرآنية الهرمية"

    echo "معلومات الاتصال:"
    echo "  المستخدم: $DB_USER"
    echo "  الخادم: $DB_HOST"
    echo "  المنفذ: $DB_PORT"
    echo "  قاعدة البيانات: $DB_NAME"
    echo ""

    # التحقق من المتطلبات
    check_requirements

    # طلب التأكيد
    print_warning "هذا السكريبت سينشئ قاعدة بيانات جديدة وجداول"
    read -p "هل تريد المتابعة؟ (نعم/لا): " confirm
    if [[ ! "$confirm" =~ ^(نعم|yes|y|Y)$ ]]; then
        print_info "تم الإلغاء"
        exit 0
    fi
    echo ""

    # بدء الوقت
    START_TIME=$(date +%s)

    # الخطوة 1: إعداد القاعدة والامتدادات
    print_header "📝 الخطوة 1/4: إعداد القاعدة والامتدادات"
    execute_sql_file "01_setup.sql" "إنشاء قاعدة البيانات والامتدادات"

    # الخطوة 2: الجداول الأساسية (Level 0)
    print_header "📊 الخطوة 2/4: إنشاء الجداول الأساسية"
    execute_sql_file "02_level0_core_tables.sql" "إنشاء جداول السور والآيات والكلمات" "$DB_NAME"

    # الخطوة 3: المستويات المتبقية (Levels 1-5)
    print_header "🔗 الخطوة 3/4: إنشاء الجداول المتقدمة"
    execute_sql_file "03_remaining_levels.sql" "إنشاء جداول التحليل والمحتوى والوسائط" "$DB_NAME"

    # الخطوة 4: Views والدوال
    print_header "🔍 الخطوة 4/4: إنشاء Views والدوال"
    execute_sql_file "04_views_and_functions.sql" "إنشاء Views والدوال المساعدة" "$DB_NAME"

    # حساب الوقت
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))

    # النتيجة النهائية
    print_header "🎉 تم التثبيت بنجاح!"

    echo -e "${GREEN}"
    echo "✅ تم إنشاء قاعدة البيانات بنجاح!"
    echo "⏱️  المدة: ${DURATION} ثانية"
    echo ""
    echo "📊 الإحصائيات:"
    echo "  - المخططات (Schemas): 4 (quran, analytics, community, public)"
    echo "  - الجداول: 19 جدول"
    echo "  - الأعمدة: 400+ عمود"
    echo "  - الفهارس: 50+ فهرس"
    echo "  - Views: 5 materialized views"
    echo "  - الدوال: 7 دوال"
    echo ""
    echo "🔍 للتحقق من التثبيت:"
    echo "  psql -U $DB_USER -d $DB_NAME"
    echo ""
    echo "📚 استعلامات الاختبار:"
    echo "  # عرض جميع الجداول"
    echo "  \\dt quran.*"
    echo ""
    echo "  # التحقق من الامتدادات"
    echo "  \\dx"
    echo ""
    echo "  # عرض السور"
    echo "  SELECT COUNT(*) FROM quran.surahs;"
    echo ""
    echo "📖 للمزيد من الاستعلامات، راجع:"
    echo "  - SMART_QUERIES.md"
    echo "  - QUICK_START.md"
    echo "  - README.md"
    echo ""
    echo "🔄 الخطوة التالية: استيراد البيانات"
    echo "  python3 import_from_sqlite.py"
    echo -e "${NC}"
}

# تنفيذ البرنامج
main "$@"
