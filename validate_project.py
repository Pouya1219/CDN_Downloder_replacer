"""
✅ اعتبارسنجی پروژه
بررسی ساختار پروژه قبل از جایگزینی CDN
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple


class ProjectValidator:
    """اعتبارسنج پروژه"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """بارگذاری کانفیگ"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def validate_project(self, proj_id: str) -> Tuple[bool, List[str]]:
        """اعتبارسنجی یک پروژه"""
        projects = self.config.get('projects', {})
        
        if proj_id not in projects:
            return False, [f"❌ پروژه {proj_id} در کانفیگ یافت نشد"]
        
        proj = projects[proj_id]
        issues = []
        
        project_path = Path(proj.get('path', ''))
        
        if not project_path.exists():
            issues.append(f"❌ مسیر پروژه وجود نداره: {project_path}")
            return False, issues
        
        templates_dir = project_path / proj.get('templates_dir', 'templates')
        
        if not templates_dir.exists():
            issues.append(f"⚠️ پوشه templates یافت نشد: {templates_dir}")
        else:
            template_files = list(templates_dir.rglob('*.html'))
            
            if not template_files:
                issues.append(f"⚠️ هیچ فایل HTML در templates یافت نشد")
            else:
                issues.append(f"✅ {len(template_files)} فایل template پیدا شد")
        
        static_dir = project_path / proj.get('static_dir', 'static')
        
        if not static_dir.exists():
            issues.append(f"⚠️ پوشه static یافت نشد: {static_dir}")
            issues.append(f"💡 توصیه: ابتدا فایل‌های Local رو در {static_dir} قرار بده")
        else:
            css_dir = static_dir / 'css'
            js_dir = static_dir / 'js'
            icons_dir = static_dir / 'auto_icons'
            
            if css_dir.exists():
                css_count = len(list(css_dir.glob('*.css')))
                issues.append(f"✅ {css_count} فایل CSS در static/css")
            else:
                issues.append(f"⚠️ پوشه static/css یافت نشد")
            
            if js_dir.exists():
                js_count = len(list(js_dir.glob('*.js')))
                issues.append(f"✅ {js_count} فایل JS در static/js")
            else:
                issues.append(f"⚠️ پوشه static/js یافت نشد")
            
            if icons_dir.exists():
                issues.append(f"✅ پوشه auto_icons موجود است")
            else:
                issues.append(f"⚠️ پوشه auto_icons یافت نشد")
        
        try:
            test_file = project_path / '.write_test'
            test_file.touch()
            test_file.unlink()
            issues.append(f"✅ دسترسی نوشتن در پروژه OK")
        except Exception as e:
            issues.append(f"❌ مشکل در دسترسی نوشتن: {e}")
            return False, issues
        
        has_critical = any(msg.startswith('❌') for msg in issues)
        
        return not has_critical, issues
    
    def validate_all_enabled_projects(self):
        """اعتبارسنجی همه پروژه‌های فعال"""
        projects = self.config.get('projects', {})
        enabled_projects = {k: v for k, v in projects.items() if v.get('enabled', False)}
        
        if not enabled_projects:
            print("❌ هیچ پروژه فعالی یافت نشد!")
            return
        
        print()
        print("=" * 80)
        print("✅ اعتبارسنجی پروژه‌های فعال")
        print("=" * 80)
        
        for proj_id, proj_data in enabled_projects.items():
            print()
            print(f"📋 {proj_data.get('name', proj_id)}")
            print("-" * 80)
            
            is_valid, issues = self.validate_project(proj_id)
            
            for issue in issues:
                print(f"   {issue}")
            
            if is_valid:
                print(f"\n   🎉 پروژه {proj_id} آماده استفاده است!")
            else:
                print(f"\n   ⚠️ پروژه {proj_id} مشکل دارد و باید اصلاح بشه")
        
        print()
        print("=" * 80)


def main():
    """تابع اصلی"""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 22 + "✅ اعتبارسنج پروژه" + " " * 37 + "║")
    print("╚" + "═" * 78 + "╝")
    
    validator = ProjectValidator()
    validator.validate_all_enabled_projects()
    
    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
