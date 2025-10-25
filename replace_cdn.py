"""
🔄 سیستم جایگزینی خودکار CDN → Local
با پشتیبانی از Multi-Project، چک وجود فایل‌ها و کپی خودکار

نویسنده: ClinicPro Team
نسخه: 2.1
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class ConfigManager:
    """مدیریت کانفیگ پروژه‌ها"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """بارگذاری کانفیگ"""
        if not self.config_file.exists():
            print(f"❌ فایل کانفیگ یافت نشد: {self.config_file}")
            print("💡 ساخت فایل کانفیگ پیش‌فرض...")
            self.create_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ خطا در خواندن کانفیگ: {e}")
            return {}
    
    def create_default_config(self):
        """ساخت کانفیگ پیش‌فرض"""
        default_config = {
            "version": "1.0",
            "default_project": "my_project",
            "projects": {
                "my_project": {
                    "name": "پروژه من",
                    "path": "D:/my_project",
                    "templates_dir": "templates",
                    "static_dir": "static",
                    "enabled": True
                }
            },
            "replacement_settings": {
                "create_backup": True,
                "backup_dir_name": "backup_templates_{timestamp}",
                "save_log": True,
                "log_dir": "logs",
                "dry_run_first": True
            },
            "cdn_mappings": {}
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ کانفیگ پیش‌فرض ایجاد شد: {self.config_file}")
    
    def get_projects(self) -> Dict:
        """دریافت لیست پروژه‌ها"""
        return self.config.get('projects', {})
    
    def get_enabled_projects(self) -> Dict:
        """دریافت پروژه‌های فعال"""
        projects = self.get_projects()
        return {k: v for k, v in projects.items() if v.get('enabled', False)}
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """دریافت یک پروژه خاص"""
        return self.config.get('projects', {}).get(project_id)
    
    def get_cdn_mappings(self) -> List[Tuple[str, str, str]]:
        """دریافت نقشه‌های CDN (pattern, replacement, file_path)"""
        mappings = []
        cdn_map = self.config.get('cdn_mappings', {})
        
        for cdn_name, cdn_data in cdn_map.items():
            if cdn_data.get('enabled', True):
                # استخراج مسیر فایل از replacement
                replacement = cdn_data['replacement']
                
                # مثال: {% static 'js/auto_jquery.min.js' %}"
                # استخراج: js/auto_jquery.min.js
                file_path_match = re.search(r"'([^']+)'", replacement)
                if file_path_match:
                    file_path = file_path_match.group(1)
                else:
                    file_path = None
                
                mappings.append((
                    cdn_data['pattern'],
                    cdn_data['replacement'],
                    file_path,
                    cdn_name
                ))
        
        return mappings
    
    def get_settings(self) -> Dict:
        """دریافت تنظیمات"""
        return self.config.get('replacement_settings', {})


class CDNReplacer:
    """جایگزین‌ساز CDN"""
    
    def __init__(self, project_config: Dict, cdn_mappings: List, settings: Dict):
        self.project_name = project_config.get('name', 'Unknown')
        self.project_dir = Path(project_config['path'])
        self.templates_dir = self.project_dir / project_config.get('templates_dir', 'templates')
        self.static_dir = self.project_dir / project_config.get('static_dir', 'static')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = settings.get('backup_dir_name', 'backup_{timestamp}').format(timestamp=timestamp)
        self.backup_dir = self.project_dir / backup_name
        
        self.replacements = cdn_mappings
        self.settings = settings
        
        self.stats = {
            'files_scanned': 0,
            'files_modified': 0,
            'replacements_made': 0,
            'errors': 0,
            'missing_files': [],
            'copied_files': []
        }
        
        self.detailed_log = []
    
    def check_static_files(self):
        """بررسی وجود فایل‌های static"""
        print("🔍 بررسی فایل‌های static...")
        print("-" * 70)
        
        missing_files = []
        
        for pattern, replacement, file_path, cdn_name in self.replacements:
            if not file_path:
                continue
            
            # مسیر کامل فایل
            full_path = self.static_dir / file_path
            
            if not full_path.exists():
                missing_files.append({
                    'name': cdn_name,
                    'path': file_path,
                    'full_path': full_path
                })
                print(f"   ❌ {file_path}")
            else:
                print(f"   ✅ {file_path}")
        
        print()
        
        if missing_files:
            print(f"⚠️ {len(missing_files)} فایل یافت نشد!")
            print()
            print("💡 می‌خوای فایل‌های نمونه (placeholder) بسازم؟")
            print("   این فایل‌ها خالی هستن، باید خودت CDN رو دانلود کنی")
            print()
            
            choice = input("ساخت فایل‌های نمونه؟ (yes/no): ").strip().lower()
            
            if choice in ['yes', 'y', 'بله', 'آره']:
                self.create_placeholder_files(missing_files)
        
        else:
            print("✅ همه فایل‌ها موجود هستند!")
        
        print()
        
        return len(missing_files) == 0
    
    def create_placeholder_files(self, missing_files: List[Dict]):
        """ساخت فایل‌های نمونه خالی"""
        print()
        print("📝 ساخت فایل‌های نمونه...")
        print("-" * 70)
        
        for file_info in missing_files:
            full_path = file_info['full_path']
            
            try:
                # ساخت پوشه
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # ساخت فایل خالی با کامنت
                if full_path.suffix == '.css':
                    content = f"/* Placeholder for {file_info['name']} */\n/* Download from CDN and replace this file */\n"
                elif full_path.suffix == '.js':
                    content = f"// Placeholder for {file_info['name']}\n// Download from CDN and replace this file\n"
                else:
                    content = f"# Placeholder for {file_info['name']}\n"
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ {file_info['path']}")
                self.stats['copied_files'].append(file_info['path'])
                
            except Exception as e:
                print(f"   ❌ خطا: {e}")
                self.stats['errors'] += 1
        
        print()
        print(f"✅ {len(missing_files)} فایل نمونه ایجاد شد")
        print()
        print("⚠️ توجه: این فایل‌ها placeholder هستن!")
        print("💡 باید خودت فایل‌های واقعی CDN رو دانلود کنی:")
        print("   python cdn_downloader_simple.py")
        print()
    
    def create_backup(self) -> bool:
        """ایجاد بکاپ"""
        if not self.settings.get('create_backup', True):
            print("⚠️ بکاپ غیرفعال است")
            return True
        
        print("💾 ایجاد بکاپ...")
        print("-" * 70)
        
        try:
            if self.templates_dir.exists():
                shutil.copytree(self.templates_dir, self.backup_dir)
                print(f"   ✅ بکاپ ایجاد شد: {self.backup_dir.name}")
                return True
            else:
                print(f"   ⚠️ پوشه templates یافت نشد: {self.templates_dir}")
                return False
        except Exception as e:
            print(f"   ❌ خطا در ایجاد بکاپ: {e}")
            return False
    
    def find_template_files(self) -> List[Path]:
        """پیدا کردن فایل‌های template"""
        if not self.templates_dir.exists():
            return []
        
        extensions = ['.html', '.htm', '.jinja', '.jinja2', '.j2']
        template_files = []
        
        for ext in extensions:
            template_files.extend(self.templates_dir.rglob(f'*{ext}'))
        
        return template_files
    
    def replace_in_file(self, file_path: Path) -> Tuple[bool, int, List]:
        """جایگزینی CDN در فایل"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            replacements_count = 0
            replaced_items = []
            
            for pattern, replacement, file_path_in_static, cdn_name in self.replacements:
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                
                if matches:
                    for match in matches:
                        old_link = match.group(0)
                        content = content.replace(old_link, replacement)
                        replacements_count += 1
                        
                        replaced_items.append({
                            'cdn': cdn_name,
                            'from': old_link[:80] + '...' if len(old_link) > 80 else old_link,
                            'to': replacement
                        })
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True, replacements_count, replaced_items
            else:
                return False, 0, []
                
        except Exception as e:
            self.stats['errors'] += 1
            print(f"   ❌ خطا: {e}")
            return False, 0, []
    
    def process_all_files(self, dry_run=False):
        """پردازش همه فایل‌ها"""
        print("=" * 70)
        print(f"🔄 پروژه: {self.project_name}")
        print(f"📁 مسیر: {self.project_dir}")
        print("=" * 70)
        print()
        
        if dry_run:
            print("⚠️ حالت تست (بدون تغییر)")
            print()
        
        template_files = self.find_template_files()
        
        if not template_files:
            print("❌ هیچ فایل template یافت نشد!")
            return
        
        print(f"📄 تعداد فایل‌ها: {len(template_files)}")
        print()
        
        for i, file_path in enumerate(template_files, 1):
            self.stats['files_scanned'] += 1
            
            relative_path = file_path.relative_to(self.templates_dir)
            
            if not dry_run:
                modified, count, items = self.replace_in_file(file_path)
                
                if modified:
                    self.stats['files_modified'] += 1
                    self.stats['replacements_made'] += count
                    
                    print(f"[{i}/{len(template_files)}] ✅ {relative_path} ({count} تغییر)")
                    
                    self.detailed_log.append({
                        'file': str(relative_path),
                        'replacements': count,
                        'items': items
                    })
            else:
                # در حالت dry run فقط نشون بده چی میشه
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    count = 0
                    for pattern, replacement, _, cdn_name in self.replacements:
                        matches = list(re.finditer(pattern, content, re.IGNORECASE))
                        count += len(matches)
                    
                    if count > 0:
                        print(f"[{i}/{len(template_files)}] 🔍 {relative_path} ({count} تغییر ممکن)")
                
                except Exception as e:
                    print(f"[{i}/{len(template_files)}] ❌ {relative_path} - خطا: {e}")
        
        print()
        self.print_summary()
    
    def print_summary(self):
        """خلاصه عملیات"""
        print("=" * 70)
        print("📊 خلاصه:")
        print("=" * 70)
        print(f"📁 بررسی شده: {self.stats['files_scanned']}")
        print(f"✏️  تغییر یافته: {self.stats['files_modified']}")
        print(f"🔄 جایگزینی‌ها: {self.stats['replacements_made']}")
        
        if self.stats['copied_files']:
            print(f"📝 فایل‌های نمونه: {len(self.stats['copied_files'])}")
        
        print(f"❌ خطاها: {self.stats['errors']}")
        print("=" * 70)
    
    def save_log(self):
        """ذخیره لاگ"""
        if not self.settings.get('save_log', True):
            return
        
        if not self.detailed_log:
            return
        
        log_dir = self.project_dir / self.settings.get('log_dir', 'logs')
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"replacement_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'project': self.project_name,
                    'timestamp': datetime.now().isoformat(),
                    'stats': self.stats,
                    'files': self.detailed_log
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n📝 لاگ: {log_file}")
        except Exception as e:
            print(f"\n⚠️ خطا در ذخیره لاگ: {e}")


def main():
    """تابع اصلی"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "🔄 CDN Replacer v2.1" + " " * 33 + "║")
    print("║" + " " * 12 + "Multi-Project Support" + " " * 36 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    config_manager = ConfigManager()
    
    enabled_projects = config_manager.get_enabled_projects()
    
    if not enabled_projects:
        print("❌ هیچ پروژه فعالی در کانفیگ یافت نشد!")
        print("💡 فایل config.json رو ویرایش کن و پروژه‌هات رو اضافه کن")
        input("\nPress Enter to exit...")
        return
    
    print("📋 پروژه‌های فعال:")
    print("-" * 70)
    
    project_list = list(enabled_projects.items())
    
    for i, (proj_id, proj_data) in enumerate(project_list, 1):
        print(f"{i}. {proj_data['name']}")
        print(f"   📁 {proj_data['path']}")
    
    print(f"{len(project_list) + 1}. همه پروژه‌ها")
    print()
    
    try:
        choice = int(input("انتخاب کنید: ").strip())
        
        if choice < 1 or choice > len(project_list) + 1:
            print("❌ انتخاب نامعتبر!")
            return
        
        if choice == len(project_list) + 1:
            selected_projects = project_list
        else:
            selected_projects = [project_list[choice - 1]]
        
    except ValueError:
        print("❌ ورودی نامعتبر!")
        return
    
    print()
    print("انتخاب حالت:")
    print("1. تست (بدون تغییر)")
    print("2. اجرای واقعی (با بکاپ)")
    print()
    
    mode = input("انتخاب (1 یا 2): ").strip()
    
    if mode not in ['1', '2']:
        print("❌ انتخاب نامعتبر!")
        return
    
    dry_run = (mode == '1')
    
    if mode == '2':
        print()
        print("⚠️ این عملیات فایل‌ها رو تغییر میده!")
        confirm = input("ادامه؟ (yes/no): ").strip().lower()
        
        if confirm not in ['yes', 'y', 'بله', 'آره']:
            print("❌ لغو شد")
            return
    
    print()
    
    cdn_mappings = config_manager.get_cdn_mappings()
    settings = config_manager.get_settings()
    
    if not cdn_mappings:
        print("❌ هیچ CDN mapping فعالی یافت نشد!")
        return
    
    for proj_id, proj_data in selected_projects:
        replacer = CDNReplacer(proj_data, cdn_mappings, settings)
        
        # بررسی فایل‌های static
        if not dry_run:
            files_ok = replacer.check_static_files()
            
            if not files_ok:
                print("⚠️ بعضی فایل‌ها موجود نیستند")
                print("💡 می‌تونی الان دانلودشون کنی:")
                print("   python cdn_downloader_simple.py")
                print()
                
                cont = input("ادامه به جایگزینی؟ (yes/no): ").strip().lower()
                if cont not in ['yes', 'y', 'بله', 'آره']:
                    print("❌ رد شد")
                    continue
                print()
        
        # ایجاد بکاپ
        if not dry_run:
            if not replacer.create_backup():
                print(f"❌ بکاپ {proj_data['name']} ناموفق بود. رد شد.")
                continue
            print()
        
        # جایگزینی
        replacer.process_all_files(dry_run=dry_run)
        
        # ذخیره لاگ
        if not dry_run:
            replacer.save_log()
        
        print()
        print("-" * 70)
        print()
    
    if dry_run:
        print("💡 این تست بود. برای اجرای واقعی گزینه 2 رو انتخاب کن.")
    else:
        print("🎉 تمام!")
    
    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
