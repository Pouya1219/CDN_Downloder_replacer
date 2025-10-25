# 🔄 CDN to Local Replacer
درود و سپاس

این کار هایی هست که این نرم افزار برای شما انجام میده 
1. فایل های static  دانلود میکنه !
2. پروژ یا چند پروژه تو بهش میدی مسیر تمپلیت و استاتیک میدی و برات فایل هایی که داخلش از cdn  استفاده کردی و پیدا میکنه
3. با فایل هایی که دانلود کرده و در استاتیک برات کپی کرده مثل bootstrap , allin , aos , ... همه را پیدا میکنه و با  مثلا {% 'static 'js/auto_bootstrap %} جایگزین میکنه!!! راستی به ایکون ها هم نمیخواد دست بزنی بزار فرمتش همون باشه !😉😉😉😉😉 برات هندل میکنه!
4. دیگه نمیخواد بشینی دونه دونه فایل هارو پیدا کنی که اگر اینتر نت قطع شد پروژه عزیز شما بخوابه !
5. مرسی و منتظر استفاده با لذت شما هستم !!! بدرور
![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Stars](https://img.shields.io/github/stars/yourusername/cdn-replacer?style=social)

**سیستم جایگزینی خودکار CDN با فایل‌های Local برای پروژه‌های Django/Flask**

[فارسی](#-فارسی) | [English](#-english)



---

## 📖 فارسی

### 🎯 ویژگی‌ها

- ✅ **پشتیبانی از چندین پروژه** - مدیریت همزمان چند پروژه
- 🔧 **کانفیگ خارجی** - تنظیمات جدا از کد
- 💾 **بکاپ خودکار** - ایمنی کامل قبل از تغییر
- 📊 **لاگ دقیق** - گزارش کامل تغییرات
- 🧪 **حالت تست** - بررسی قبل از اجرا
- 🚀 **پردازش دسته‌ای** - اجرای خودکار روی همه پروژه‌ها
- 🔗 **16+ CDN پشتیبانی شده** - Bootstrap, jQuery, Font Awesome و...

### 🛠 نصب

```bash
# کلون کردن
git clone https://github.com/Pouya1219/CDN-Replacer.git
cd cdn-replacer

# نیازی به نصب پکیج خارجی نیست!
# همه چیز با Standard Library پایتون کار می‌کنه



ترتیب کامل استفاده


# 1. اضافه کردن پروژه
python project_manager.py

# 2. دانلود فایل‌های CDN
python cdn_downloader.py

# 3. اعتبارسنجی
python validate_project.py

# 4. جایگزینی لینک‌ها
python replace_cdn.py




