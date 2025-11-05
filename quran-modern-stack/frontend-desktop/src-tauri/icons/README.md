# أيقونات التطبيق / App Icons

## الملفات المطلوبة / Required Files

يجب إنشاء الأيقونات التالية:
- `32x32.png` - أيقونة 32×32 بكسل
- `128x128.png` - أيقونة 128×128 بكسل
- `128x128@2x.png` - أيقونة 256×256 بكسل (Retina)
- `icon.icns` - أيقونة macOS
- `icon.ico` - أيقونة Windows

## إنشاء الأيقونات / Generating Icons

### الخيار 1: استخدام أداة عبر الإنترنت

استخدم موقع مثل:
- https://icon.kitchen/
- https://www.favicon-generator.org/

### الخيار 2: استخدام Tauri Icon

```bash
npm install -D @tauri-apps/cli
npm run tauri icon path/to/source-icon.png
```

### الخيار 3: يدوياً

استخدم برنامج تصميم مثل GIMP أو Photoshop لإنشاء الأيقونات بالأحجام المطلوبة.

## ملاحظة

حالياً، التطبيق سيعمل في وضع التطوير بدون أيقونات (سيظهر أيقونة افتراضية).
لكن لبناء التطبيق النهائي، ستحتاج إلى إنشاء هذه الأيقونات.
