"""
📋 مدیر پروژه‌ها
افزودن، ویرایش، حذف و مدیریت پروژه‌ها
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional


class ProjectManager:
    """مدیریت پروژه‌ها در کانفیگ"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """بارگذاری کانفیگ"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"❌ خطا در خواندن کانفیگ: {e}")
                print(f"💡 مشکل در خط {e.lineno}، ستون {e.colno}")
                print(f"📝 پیام: {e.msg}")
                print()
                print("🔧 آیا می‌خوای کانفیگ جدید بسازم؟ (فایل قبلی backup میشه)")
                
                choice = input("ساخت کانفیگ جدید؟ (yes/no): ").strip().lower()
                
                if choice in ['yes', 'y', 'بله']:
                    # بکاپ فایل قبلی
                    backup_file = self.config_file.with_suffix('.json.backup')
                    self.config_file.rename(backup_file)
                    print(f"✅ بکاپ: {backup_file}")
                    
                    # ساخت کانفیگ جدید
                    return self.create_default_config()
                else:
                    print("❌ لطفاً فایل config.json رو دستی اصلاح کن")
                    exit(1)
            except Exception as e:
                print(f"❌ خطای غیرمنتظره: {e}")
                exit(1)
        
        return self.create_default_config()

    
    def save_config(self):
        """ذخیره کانفیگ"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"✅ کانفیگ ذخیره شد")
    
    def create_default_config(self) -> dict:
        """ساخت کانفیگ پیش‌فرض"""
        return {
            "version": "1.0",
            "default_project": None,
            "projects": {},
            "replacement_settings": {
                "create_backup": True,
                "backup_dir_name": "backup_templates_{timestamp}",
                "save_log": True,
                "log_dir": "logs",
                "dry_run_first": True
            },
            "cdn_mappings": self.get_default_cdn_mappings()
        }
    
    def get_default_cdn_mappings(self) -> dict:
        """CDN های پیش‌فرض"""
        return {
            "bootstrap_css": {
                "pattern": r"https?://(?:cdn\.jsdelivr\.net|stackpath\.bootstrapcdn\.com|maxcdn\.bootstrapcdn\.com)/.*?bootstrap(?:@[\d\.]+)?.*?\.min\.css[\"']?",
                "replacement": "{% static 'css/auto_bootstrap.min.css' %}\"",
                "enabled": True,
                "description": "Bootstrap CSS Framework"
            },
            "bootstrap_js_bundle": {
                "pattern": r"https?://(?:cdn\.jsdelivr\.net|stackpath\.bootstrapcdn\.com|maxcdn\.bootstrapcdn\.com)/.*?bootstrap(?:@[\d\.]+)?.*?\.bundle\.min\.js[\"']?",
                "replacement": "{% static 'js/auto_bootstrap.bundle.min.js' %}\"",
                "enabled": True,
                "description": "Bootstrap JS Bundle (با Popper)"
            },
            "bootstrap_js": {
                "pattern": r"https?://(?:cdn\.jsdelivr\.net|stackpath\.bootstrapcdn\.com)/.*?bootstrap(?:@[\d\.]+)?.*?\.min\.js[\"']?",
                "replacement": "{% static 'js/auto_bootstrap.min.js' %}\"",
                "enabled": True,
                "description": "Bootstrap JS (بدون Popper)"
            },
            "jquery": {
                "pattern": r"https?://(?:code\.jquery\.com|ajax\.googleapis\.com/ajax/libs/jquery)/jquery-[\d\.]+\.min\.js[\"']?",
                "replacement": "{% static 'js/auto_jquery.min.js' %}\"",
                "enabled": True,
                "description": "jQuery Library"
            },
            "select2_js": {
                "pattern": r"https?://cdn\.jsdelivr\.net/npm/select2@[\d\.\-rc]+/dist/js/select2\.min\.js[\"']?",
                "replacement": "{% static 'js/auto_select2.min.js' %}\"",
                "enabled": True,
                "description": "Select2 JavaScript"
            },
            "select2_css": {
                "pattern": r"https?://cdn\.jsdelivr\.net/npm/select2@[\d\.\-rc]+/dist/css/select2\.min\.css[\"']?",
                "replacement": "{% static 'css/auto_select2.min.css' %}\"",
                "enabled": True,
                "description": "Select2 CSS"
            },
            "datatables_js": {
                "pattern": r"https?://cdn\.datatables\.net/[\d\.]+/js/jquery\.dataTables\.min\.js[\"']?",
                "replacement": "{% static 'js/auto_datatables.min.js' %}\"",
                "enabled": True,
                "description": "DataTables JavaScript"
            },
            "sweetalert2_js": {
                "pattern": r"https?://cdn\.jsdelivr\.net/npm/sweetalert2@[\d\.]+/dist/sweetalert2\.(?:all\.)?min\.js[\"']?",
                "replacement": "{% static 'js/auto_sweetalert2.min.js' %}\"",
                "enabled": True,
                "description": "SweetAlert2 JavaScript"
            },
            "font_awesome": {
                "pattern": r"https?://(?:cdnjs\.cloudflare\.com/ajax/libs/font-awesome|use\.fontawesome\.com/releases)/[\d\.]+/css/(?:all|fontawesome)\.min\.css[\"']?",
                "replacement": "{% static 'auto_icons/fontawesome/css/all.min.css' %}\"",
                "enabled": True,
                "description": "Font Awesome Icons"
            }
        }
    
    def list_projects(self):
        """نمایش لیست پروژه‌ها"""
        projects = self.config.get('projects', {})
        
        if not projects:
            print("📋 هیچ پروژه‌ای ثبت نشده")
            return
        
        print()
        print("=" * 80)
        print("📋 لیست پروژه‌ها")
        print("=" * 80)
        
        for i, (proj_id, proj_data) in enumerate(projects.items(), 1):
            status = "✅ فعال" if proj_data.get('enabled', False) else "❌ غیرفعال"
            
            print(f"\n{i}. [{proj_id}] {proj_data.get('name', 'بدون نام')} - {status}")
            print(f"   📁 مسیر: {proj_data.get('path', 'نامشخص')}")
            print(f"   📂 Templates: {proj_data.get('templates_dir', 'templates')}")
            print(f"   📦 Static: {proj_data.get('static_dir', 'static')}")
        
        print()
    
    def add_project(self):
        """افزودن پروژه جدید"""
        print()
        print("=" * 80)
        print("➕ افزودن پروژه جدید")
        print("=" * 80)
        print()
        
        proj_id = input("شناسه پروژه (انگلیسی، بدون فاصله): ").strip()
        
        if not proj_id:
            print("❌ شناسه نمی‌تونه خالی باشه!")
            return
        
        if proj_id in self.config.get('projects', {}):
            print(f"❌ پروژه {proj_id} قبلاً وجود داره!")
            return
        
        name = input("نام پروژه (فارسی/انگلیسی): ").strip()
        if not name:
            name = proj_id
        
        path = input("مسیر پروژه (مثال: D:/projects/myapp): ").strip()
        
        if not path:
            print("❌ مسیر نمی‌تونه خالی باشه!")
            return
        
        if not Path(path).exists():
            print(f"⚠️ مسیر {path} وجود نداره!")
            create = input("ایجاد بشه؟ (yes/no): ").strip().lower()
            
            if create in ['yes', 'y', 'بله']:
                try:
                    Path(path).mkdir(parents=True, exist_ok=True)
                    print(f"✅ مسیر ایجاد شد")
                except Exception as e:
                    print(f"❌ خطا: {e}")
                    return
            else:
                return
        
        templates_dir = input("نام پوشه templates (پیش‌فرض: templates): ").strip() or "templates"
        static_dir = input("نام پوشه static (پیش‌فرض: static): ").strip() or "static"
        
        enabled_input = input("فعال باشه؟ (yes/no, پیش‌فرض: yes): ").strip().lower()
        enabled = enabled_input not in ['no', 'n', 'نه']
        
        if 'projects' not in self.config:
            self.config['projects'] = {}
        
        self.config['projects'][proj_id] = {
            "name": name,
            "path": path,
            "templates_dir": templates_dir,
            "static_dir": static_dir,
            "enabled": enabled
        }
        
        self.save_config()
        
        print()
        print(f"✅ پروژه {name} با موفقیت اضافه شد!")
    
    def edit_project(self):
        """ویرایش پروژه"""
        self.list_projects()
        
        projects = self.config.get('projects', {})
        
        if not projects:
            return
        
        print()
        proj_id = input("شناسه پروژه برای ویرایش: ").strip()
        
        if proj_id not in projects:
            print(f"❌ پروژه {proj_id} یافت نشد!")
            return
        
        proj = projects[proj_id]
        
        print()
        print(f"ویرایش پروژه: {proj.get('name', proj_id)}")
        print("-" * 80)
        
        new_name = input(f"نام جدید (فعلی: {proj.get('name', '-')}، Enter=بدون تغییر): ").strip()
        if new_name:
            proj['name'] = new_name
        
        new_path = input(f"مسیر جدید (فعلی: {proj.get('path', '-')}، Enter=بدون تغییر): ").strip()
        if new_path:
            proj['path'] = new_path
        
        new_templates = input(f"پوشه templates (فعلی: {proj.get('templates_dir', 'templates')}، Enter=بدون تغییر): ").strip()
        if new_templates:
            proj['templates_dir'] = new_templates
        
        new_static = input(f"پوشه static (فعلی: {proj.get('static_dir', 'static')}، Enter=بدون تغییر): ").strip()
        if new_static:
            proj['static_dir'] = new_static
        
        current_status = "فعال" if proj.get('enabled', False) else "غیرفعال"
        toggle = input(f"وضعیت فعلی: {current_status}، تغییر بده؟ (yes/no): ").strip().lower()
        
        if toggle in ['yes', 'y', 'بله']:
            proj['enabled'] = not proj.get('enabled', False)
        
        self.save_config()
        
        print()
        print(f"✅ پروژه {proj_id} ویرایش شد!")
    
    def delete_project(self):
        """حذف پروژه"""
        self.list_projects()
        
        projects = self.config.get('projects', {})
        
        if not projects:
            return
        
        print()
        proj_id = input("شناسه پروژه برای حذف: ").strip()
        
        if proj_id not in projects:
            print(f"❌ پروژه {proj_id} یافت نشد!")
            return
        
        proj_name = projects[proj_id].get('name', proj_id)
        
        print()
        print(f"⚠️ آیا مطمئنی که می‌خوای پروژه '{proj_name}' رو حذف کنی؟")
        confirm = input("این فقط از کانفیگ حذف میشه (فایل‌های پروژه پاک نمیشن) (yes/no): ").strip().lower()
        
        if confirm not in ['yes', 'y', 'بله']:
            print("❌ لغو شد")
            return
        
        del self.config['projects'][proj_id]
        self.save_config()
        
        print()
        print(f"✅ پروژه {proj_name} از کانفیگ حذف شد")
    
    def toggle_project(self):
        """فعال/غیرفعال کردن پروژه"""
        self.list_projects()
        
        projects = self.config.get('projects', {})
        
        if not projects:
            return
        
        print()
        proj_id = input("شناسه پروژه: ").strip()
        
        if proj_id not in projects:
            print(f"❌ پروژه {proj_id} یافت نشد!")
            return
        
        current = projects[proj_id].get('enabled', False)
        projects[proj_id]['enabled'] = not current
        
        status = "فعال" if projects[proj_id]['enabled'] else "غیرفعال"
        
        self.save_config()
        
        print()
        print(f"✅ پروژه {proj_id} حالا {status} است")
    
    def manage_cdn_mappings(self):
        """مدیریت CDN mappings"""
        print()
        print("=" * 80)
        print("🔗 مدیریت CDN Mappings")
        print("=" * 80)
        
        cdn_map = self.config.get('cdn_mappings', {})
        
        if not cdn_map:
            print("\n❌ هیچ CDN mapping یافت نشد!")
            return
        
        print()
        for i, (cdn_id, cdn_data) in enumerate(cdn_map.items(), 1):
            status = "✅" if cdn_data.get('enabled', True) else "❌"
            desc = cdn_data.get('description', 'بدون توضیح')
            
            print(f"{i}. {status} [{cdn_id}] - {desc}")
        
        print()
        print("گزینه‌ها:")
        print("1. فعال/غیرفعال کردن یک CDN")
        print("2. بازگشت")
        
        choice = input("\nانتخاب: ").strip()
        
        if choice == '1':
            cdn_id = input("شناسه CDN: ").strip()
            
            if cdn_id in cdn_map:
                current = cdn_map[cdn_id].get('enabled', True)
                cdn_map[cdn_id]['enabled'] = not current
                
                status = "فعال" if cdn_map[cdn_id]['enabled'] else "غیرفعال"
                self.save_config()
                
                print(f"\n✅ {cdn_id} حالا {status} است")
            else:
                print(f"\n❌ {cdn_id} یافت نشد!")


def main():
    """منوی اصلی"""
    manager = ProjectManager()
    
    while True:
        print()
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "📋 مدیر پروژه‌ها" + " " * 37 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        print("1. نمایش پروژه‌ها")
        print("2. افزودن پروژه جدید")
        print("3. ویرایش پروژه")
        print("4. حذف پروژه")
        print("5. فعال/غیرفعال کردن پروژه")
        print("6. مدیریت CDN Mappings")
        print("0. خروج")
        print()
        
        choice = input("انتخاب کنید: ").strip()
        
        if choice == '1':
            manager.list_projects()
        
        elif choice == '2':
            manager.add_project()
        
        elif choice == '3':
            manager.edit_project()
        
        elif choice == '4':
            manager.delete_project()
        
        elif choice == '5':
            manager.toggle_project()
        
        elif choice == '6':
            manager.manage_cdn_mappings()
        
        elif choice == '0':
            print("\n👋 خداحافظ!")
            break
        
        else:
            print("\n❌ انتخاب نامعتبر!")


if __name__ == "__main__":
    main()
