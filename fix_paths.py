"""
🔧 اصلاح خودکار مسیرها در config.json
"""

import json
from pathlib import Path


def fix_windows_paths(config_file="config.json"):
    """تبدیل \ به / در مسیرها"""
    
    config_path = Path(config_file)
    
    if not config_path.exists():
        print("❌ فایل config.json یافت نشد!")
        return
    
    # بکاپ
    backup_path = config_path.with_suffix('.json.backup')
    
    try:
        # خواندن
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ذخیره بکاپ
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 بکاپ: {backup_path}")
        
        # Parse JSON
        data = json.loads(content)
        
        # اصلاح مسیرها
        if 'projects' in data:
            for proj_id, proj_data in data['projects'].items():
                if 'path' in proj_data:
                    old_path = proj_data['path']
                    new_path = old_path.replace('\\', '/')
                    
                    if old_path != new_path:
                        proj_data['path'] = new_path
                        print(f"✅ {proj_id}: {old_path} → {new_path}")
        
        # ذخیره
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print()
        print("🎉 اصلاح موفق!")
        
    except json.JSONDecodeError as e:
        print(f"❌ خطا در JSON: {e}")
        print(f"💡 خط {e.lineno}: {e.msg}")
    except Exception as e:
        print(f"❌ خطا: {e}")


if __name__ == "__main__":
    fix_windows_paths()
