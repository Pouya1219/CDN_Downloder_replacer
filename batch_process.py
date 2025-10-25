"""
🚀 پردازش دسته‌ای
اجرای خودکار روی همه پروژه‌های فعال
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from replace_cdn import ConfigManager, CDNReplacer


class BatchProcessor:
    """پردازشگر دسته‌ای"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.results = []
    
    def process_all(self, dry_run=False):
        """پردازش همه پروژه‌های فعال"""
        enabled_projects = self.config_manager.get_enabled_projects()
        
        if not enabled_projects:
            print("❌ هیچ پروژه فعالی یافت نشد!")
            return
        
        print()
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "🚀 پردازش دسته‌ای" + " " * 40 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        
        total = len(enabled_projects)
        
        print(f"📋 تعداد پروژه‌های فعال: {total}")
        print()
        
        cdn_mappings = self.config_manager.get_cdn_mappings()
        settings = self.config_manager.get_settings()
        
        for i, (proj_id, proj_data) in enumerate(enabled_projects.items(), 1):
            print(f"\n{'=' * 80}")
            print(f"پروژه {i}/{total}: {proj_data.get('name', proj_id)}")
            print(f"{'=' * 80}\n")
            
            try:
                replacer = CDNReplacer(proj_data, cdn_mappings, settings)
                
                if not dry_run:
                    if not replacer.create_backup():
                        print(f"❌ بکاپ ناموفق بود. رد شد.\n")
                        self.results.append({
                            'project': proj_id,
                            'status': 'failed',
                            'reason': 'backup_failed'
                        })
                        continue
                    print()
                
                replacer.process_all_files(dry_run=dry_run)
                
                if not dry_run:
                    replacer.save_log()
                
                self.results.append({
                    'project': proj_id,
                    'status': 'success',
                    'stats': replacer.stats
                })
                
            except Exception as e:
                print(f"\n❌ خطا در پردازش {proj_id}: {e}\n")
                self.results.append({
                    'project': proj_id,
                    'status': 'error',
                    'error': str(e)
                })
        
        self.print_summary()
    
    def print_summary(self):
        """خلاصه کلی"""
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "📊 خلاصه کلی" + " " * 41 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'success')
        failed = sum(1 for r in self.results if r['status'] == 'failed')
        error = sum(1 for r in self.results if r['status'] == 'error')
        
        print(f"📋 کل پروژه‌ها: {total}")
        print(f"✅ موفق: {success}")
        print(f"❌ ناموفق: {failed}")
        print(f"⚠️ خطا: {error}")
        print()
        
        if success > 0:
            print("✅ پروژه‌های موفق:")
            print("-" * 80)
            
            for result in self.results:
                if result['status'] == 'success':
                    stats = result['stats']
                    print(f"   • {result['project']}: "
                          f"{stats['files_modified']} فایل تغییر یافت، "
                          f"{stats['replacements_made']} جایگزینی")
        
        if failed + error > 0:
            print()
            print("❌ پروژه‌های ناموفق:")
            print("-" * 80)
            
            for result in self.results:
                if result['status'] in ['failed', 'error']:
                    reason = result.get('reason', result.get('error', 'نامشخص'))
                    print(f"   • {result['project']}: {reason}")
        
        print()
        print("=" * 80)


def main():
    """تابع اصلی"""
    print()
    print("🚀 پردازش دسته‌ای - اجرای خودکار روی همه پروژه‌ها")
    print()
    
    processor = BatchProcessor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--dry-run':
            print("⚠️ حالت تست (بدون تغییر)")
            processor.process_all(dry_run=True)
        elif sys.argv[1] == '--run':
            print("⚡ حالت واقعی (با بکاپ)")
            processor.process_all(dry_run=False)
        else:
            print("❌ آرگومان نامعتبر!")
            print("استفاده:")
            print("  python batch_process.py --dry-run   # تست")
            print("  python batch_process.py --run       # واقعی")
    else:
        print("انتخاب حالت:")
        print("1. تست (بدون تغییر)")
        print("2. واقعی (با بکاپ)")
        print()
        
        choice = input("انتخاب (1 یا 2): ").strip()
        
        if choice == '1':
            processor.process_all(dry_run=True)
        elif choice == '2':
            print()
            print("⚠️ این عملیات روی همه پروژه‌های فعال اجرا میشه!")
            confirm = input("ادامه؟ (yes/no): ").strip().lower()
            
            if confirm in ['yes', 'y', 'بله']:
                processor.process_all(dry_run=False)
            else:
                print("❌ لغو شد")
        else:
            print("❌ انتخاب نامعتبر!")
    
    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
