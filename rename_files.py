"""
🔄 تغییر نام فایل‌ها
حذف پیشوند auto_ از فایل‌های دانلود شده و به‌روزرسانی config.json
"""

import json
import shutil
from pathlib import Path


def rename_auto_files(project_path: str):
    """تغییر نام فایل‌های auto_* به نام اصلی"""
    
    project_path = Path(project_path)
    static_dir = project_path / 'static'
    
    css_dir = static_dir / 'css'
    js_dir = static_dir / 'js'
    
    print()
    print("=" * 70)
    print("🔄 تغییر نام فایل‌ها (حذف auto_)")
    print("=" * 70)
    print()
    
    renamed_count = 0
    
    # CSS Files
    if css_dir.exists():
        print("📁 CSS Files:")
        css_files = list(css_dir.glob('auto_*.css'))
        
        if not css_files:
            print("   ⚠️ فایل CSS با پیشوند auto_ یافت نشد")
        
        for file in css_files:
            new_name = file.name.replace('auto_', '')
            new_path = file.parent / new_name
            
            # اگه فایل قبلی وجود داره، حذفش کن
            if new_path.exists():
                print(f"   ⚠️ {new_name} قبلاً وجود داشت، جایگزین می‌شه...")
                new_path.unlink()
            
            file.rename(new_path)
            print(f"   ✅ {file.name} → {new_name}")
            renamed_count += 1
        
        print()
    else:
        print("⚠️ پوشه css یافت نشد")
        print()
    
    # JS Files
    if js_dir.exists():
        print("📁 JS Files:")
        js_files = list(js_dir.glob('auto_*.js'))
        
        if not js_files:
            print("   ⚠️ فایل JS با پیشوند auto_ یافت نشد")
        
        for file in js_files:
            new_name = file.name.replace('auto_', '')
            new_path = file.parent / new_name
            
            if new_path.exists():
                print(f"   ⚠️ {new_name} قبلاً وجود داشت، جایگزین می‌شه...")
                new_path.unlink()
            
            file.rename(new_path)
            print(f"   ✅ {file.name} → {new_name}")
            renamed_count += 1
        
        print()
    else:
        print("⚠️ پوشه js یافت نشد")
        print()
    
    # Icons Directory
    icons_dir = static_dir / 'auto_icons'
    if icons_dir.exists():
        print("📁 Icons Directory:")
        new_icons_dir = static_dir / 'icons'
        
        if new_icons_dir.exists():
            print(f"   ⚠️ {new_icons_dir.name} قبلاً وجود داشت، جایگزین می‌شه...")
            shutil.rmtree(new_icons_dir)
        
        icons_dir.rename(new_icons_dir)
        print(f"   ✅ auto_icons/ → icons/")
        renamed_count += 1
        print()
    else:
        print("⚠️ پوشه auto_icons یافت نشد")
        print()
    
    print("=" * 70)
    print(f"🎉 {renamed_count} مورد تغییر نام یافت")
    print("=" * 70)
    
    return renamed_count > 0


def update_config_mappings():
    """به‌روزرسانی config.json برای حذف auto_ از replacement ها"""
    
    config_file = Path('config.json')
    
    if not config_file.exists():
        print("\n⚠️ فایل config.json یافت نشد، نیازی به به‌روزرسانی نیست")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # بکاپ
        backup_file = config_file.with_suffix('.json.backup')
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print()
        print("=" * 70)
        print("🔧 به‌روزرسانی config.json")
        print("=" * 70)
        print(f"💾 بکاپ: {backup_file}")
        print()
        
        # به‌روزرسانی mappings
        if 'cdn_mappings' in config:
            updated_count = 0
            
            for cdn_name, cdn_data in config['cdn_mappings'].items():
                if 'replacement' in cdn_data:
                    old_replacement = cdn_data['replacement']
                    new_replacement = old_replacement.replace("'auto_", "'")
                    new_replacement = new_replacement.replace('"auto_', '"')
                    new_replacement = new_replacement.replace('/auto_', '/')
                    
                    if old_replacement != new_replacement:
                        cdn_data['replacement'] = new_replacement
                        print(f"✅ {cdn_name}")
                        print(f"   قبل: {old_replacement}")
                        print(f"   بعد: {new_replacement}")
                        print()
                        updated_count += 1
            
            # ذخیره
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print("=" * 70)
            print(f"🎉 {updated_count} mapping به‌روز شد")
            print("=" * 70)
            
            return updated_count > 0
        
        else:
            print("⚠️ cdn_mappings در کانفیگ یافت نشد")
            return False
    
    except Exception as e:
        print(f"❌ خطا در به‌روزرسانی config: {e}")
        return False


def main():
    """تابع اصلی"""
    
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "🔄 File Renamer" + " " * 33 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # بارگذاری کانفیگ
    config_file = Path('config.json')
    
    if not config_file.exists():
        print("❌ فایل config.json یافت نشد!")
        print()
        input("Press Enter to exit...")
        return
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ خطا در خواندن config: {e}")
        print()
        input("Press Enter to exit...")
        return
    
    projects = config.get('projects', {})
    enabled_projects = {k: v for k, v in projects.items() if v.get('enabled', False)}
    
    if not enabled_projects:
        print("❌ هیچ پروژه فعالی یافت نشد!")
        print()
        input("Press Enter to exit...")
        return
    
    # انتخاب پروژه
    print("📋 پروژه‌های فعال:")
    print("-" * 70)
    
    project_list = list(enabled_projects.items())
    
    for i, (proj_id, proj_data) in enumerate(project_list, 1):
        print(f"{i}. {proj_data['name']}")
        print(f"   📁 {proj_data['path']}")
    
    print(f"{len(project_list) + 1}. همه پروژه‌ها")
    print()
    
    try:
        choice = int(input("انتخاب پروژه: ").strip())
        
        if choice < 1 or choice > len(project_list) + 1:
            print("❌ انتخاب نامعتبر!")
            return
        
        # انتخاب پروژه‌ها
        if choice == len(project_list) + 1:
            selected_projects = project_list
        else:
            selected_projects = [project_list[choice - 1]]
        
    except ValueError:
        print("❌ ورودی نامعتبر!")
        return
    
    # تغییر نام فایل‌ها
    total_renamed = 0
    
    for proj_id, proj_data in selected_projects:
        print()
        print("=" * 70)
        print(f"📦 پروژه: {proj_data['name']}")
        print("=" * 70)
        
        if rename_auto_files(proj_data['path']):
            total_renamed += 1
        
        print()
    
    # به‌روزرسانی config
    if total_renamed > 0:
        print()
        choice = input("آیا می‌خوای config.json هم به‌روز بشه? (yes/no): ").strip().lower()
        
        if choice in ['yes', 'y', 'بله', 'آره']:
            update_config_mappings()
    
    print()
    print("🎉 تمام!")
    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
