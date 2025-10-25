"""
🔧 اصلاح خودکار config.json
"""

import json
import re
from pathlib import Path


def fix_regex_patterns(config_data):
    """اصلاح pattern های regex"""
    
    if 'cdn_mappings' not in config_data:
        return config_data
    
    for cdn_name, cdn_data in config_data['cdn_mappings'].items():
        if 'pattern' in cdn_data:
            # چک کردن اینکه آیا pattern درست escape شده یا نه
            pattern = cdn_data['pattern']
            
            # اگه backslash یه بار باشه، دوبار می‌کنیم
            # مثلاً \d -> \\d
            fixed_pattern = pattern.replace('\\', '\\\\')
            
            cdn_data['pattern'] = fixed_pattern
            
            print(f"✅ {cdn_name}: pattern اصلاح شد")
    
    return config_data


def validate_json(file_path):
    """بررسی معتبر بودن JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, "✅ فایل JSON معتبر است"
    except json.JSONDecodeError as e:
        return False, f"❌ خطا در خط {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"❌ خطا: {e}"


def main():
    config_file = Path('config.json')
    
    print("🔧 اصلاح خودکار config.json")
    print("=" * 60)
    print()
    
    if not config_file.exists():
        print("❌ فایل config.json یافت نشد!")
        return
    
    # بکاپ
    backup_file = config_file.with_suffix('.json.bak')
    
    try:
        # خواندن محتوا
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ذخیره بکاپ
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 بکاپ: {backup_file}")
        print()
        
        # بررسی اولیه
        is_valid, msg = validate_json(config_file)
        print(f"بررسی اولیه: {msg}")
        print()
        
        if is_valid:
            print("🎉 فایل مشکلی نداره!")
            return
        
        # تلاش برای اصلاح
        print("🔧 تلاش برای اصلاح...")
        print()
        
        # روش 1: اصلاح با regex
        # تبدیل \d به \\d و غیره
        fixed_content = content
        
        # الگوهای رایج که باید escape بشن
        patterns_to_fix = [
            (r'(?<!\\)\\d', r'\\\\d'),
            (r'(?<!\\)\\w', r'\\\\w'),
            (r'(?<!\\)\\s', r'\\\\s'),
            (r'(?<!\\)\\.', r'\\\\.'),
            (r'(?<!\\)\\-', r'\\\\-'),
        ]
        
        for old, new in patterns_to_fix:
            fixed_content = re.sub(old, new, fixed_content)
        
        # ذخیره فایل اصلاح شده
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        # بررسی دوباره
        is_valid, msg = validate_json(config_file)
        print(f"بررسی نهایی: {msg}")
        print()
        
        if is_valid:
            print("🎉 اصلاح موفق!")
            print(f"📝 بکاپ قبلی: {backup_file}")
        else:
            print("❌ اصلاح خودکار ناموفق بود")
            print("💡 بازگردانی از بکاپ...")
            
            # بازگردانی
            with open(backup_file, 'r', encoding='utf-8') as f:
                original = f.read()
            
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(original)
            
            print("✅ فایل به حالت قبل برگشت")
            print()
            print("🔧 لطفاً فایل config.json رو دستی اصلاح کن:")
            print("   - همه \\ باید \\\\ بشه")
            print("   - مثلاً: \\d -> \\\\d")
    
    except Exception as e:
        print(f"❌ خطا: {e}")


if __name__ == "__main__":
    main()
