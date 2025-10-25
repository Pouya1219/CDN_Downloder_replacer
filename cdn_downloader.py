"""
📥 دانلودر خودکار فایل‌های CDN
دانلود در temp و کپی به static با پیشوند auto_
"""

import json
import zipfile
import io
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


class CDNDownloader:
    """دانلودر فایل‌های CDN"""
    
    # نسخه‌های پیشنهادی
    VERSIONS = {
        'bootstrap': '5.3.2',
        'jquery': '3.7.1',
        'jquery_ui': '1.13.2',
        'select2': '4.1.0-rc.0',
        'datatables': '1.13.7',
        'sweetalert2': '11.10.1',
        'chartjs': '4.4.0',
        'fontawesome': '6.5.1',
        'popper': '2.11.8'
    }
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        
        # پوشه temp برای دانلود
        self.temp_dir = self.project_path / 'cdn_temp'
        self.temp_dir.mkdir(exist_ok=True)
        
        # پوشه static برای کپی نهایی
        self.static_dir = self.project_path / 'static'
        self.css_dir = self.static_dir / 'css'
        self.js_dir = self.static_dir / 'js'
        self.icons_dir = self.static_dir / 'auto_icons'
        
        # ساخت پوشه‌های static
        self.css_dir.mkdir(parents=True, exist_ok=True)
        self.js_dir.mkdir(parents=True, exist_ok=True)
        self.icons_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Temp: {self.temp_dir}")
        print(f"📦 Static: {self.static_dir}")
        print()
    
    def download_file(self, url: str, save_path: Path) -> bool:
        """دانلود یک فایل"""
        try:
            print(f"   📥 دانلود: {url}")
            
            # ساخت request با headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = Request(url, headers=headers)
            
            # دانلود
            with urlopen(req, timeout=30) as response:
                content = response.read()
            
            # ذخیره
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(content)
            
            size_kb = len(content) / 1024
            print(f"   ✅ دانلود: {save_path.name} ({size_kb:.1f} KB)")
            return True
            
        except HTTPError as e:
            print(f"   ❌ HTTP Error {e.code}: {e.reason}")
            return False
        except URLError as e:
            print(f"   ❌ URL Error: {e.reason}")
            return False
        except Exception as e:
            print(f"   ❌ خطا: {e}")
            return False
    
    def copy_to_static(self, src_path: Path, dest_path: Path) -> bool:
        """کپی فایل از temp به static"""
        try:
            if not src_path.exists():
                print(f"   ⚠️ فایل منبع یافت نشد: {src_path.name}")
                return False
            
            # اگر فایل مقصد وجود داره، حذفش کن
            if dest_path.exists():
                dest_path.unlink()
            
            # کپی
            shutil.copy2(src_path, dest_path)
            print(f"   📋 کپی: {dest_path.name}")
            return True
            
        except Exception as e:
            print(f"   ❌ خطا در کپی: {e}")
            return False
    
    def extract_zip(self, zip_content: bytes, extract_to: Path) -> bool:
        """استخراج فایل ZIP"""
        try:
            with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_file:
                zip_file.extractall(extract_to)
            return True
        except Exception as e:
            print(f"   ❌ خطا در استخراج: {e}")
            return False
    
    def download_bootstrap(self, version: Optional[str] = None) -> bool:
        """دانلود Bootstrap"""
        version = version or self.VERSIONS['bootstrap']
        
        print(f"\n🎨 Bootstrap {version}")
        print("-" * 60)
        
        url = f'https://github.com/twbs/bootstrap/releases/download/v{version}/bootstrap-{version}-dist.zip'
        
        try:
            # دانلود در temp
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = Request(url, headers=headers)
            
            print(f"   📥 دانلود ZIP...")
            with urlopen(req, timeout=60) as response:
                zip_content = response.read()
            
            size_mb = len(zip_content) / (1024 * 1024)
            print(f"   ✅ دانلود شد ({size_mb:.1f} MB)")
            
            # استخراج در temp
            temp_extract = self.temp_dir / 'bootstrap'
            temp_extract.mkdir(exist_ok=True)
            
            print(f"   📦 استخراج...")
            if self.extract_zip(zip_content, temp_extract):
                extracted_dir = temp_extract / f'bootstrap-{version}-dist'
                
                # کپی به static با پیشوند auto_
                print(f"   📋 کپی به static...")
                
                # CSS
                css_src = extracted_dir / 'css' / 'bootstrap.min.css'
                if css_src.exists():
                    self.copy_to_static(css_src, self.css_dir / 'auto_bootstrap.min.css')
                
                # CSS Map (اختیاری)
                css_map_src = extracted_dir / 'css' / 'bootstrap.min.css.map'
                if css_map_src.exists():
                    self.copy_to_static(css_map_src, self.css_dir / 'auto_bootstrap.min.css.map')
                
                # JS Bundle (با Popper)
                js_bundle_src = extracted_dir / 'js' / 'bootstrap.bundle.min.js'
                if js_bundle_src.exists():
                    self.copy_to_static(js_bundle_src, self.js_dir / 'auto_bootstrap.bundle.min.js')
                
                # JS Bundle Map
                js_bundle_map_src = extracted_dir / 'js' / 'bootstrap.bundle.min.js.map'
                if js_bundle_map_src.exists():
                    self.copy_to_static(js_bundle_map_src, self.js_dir / 'auto_bootstrap.bundle.min.js.map')
                
                # JS (بدون Popper)
                js_src = extracted_dir / 'js' / 'bootstrap.min.js'
                if js_src.exists():
                    self.copy_to_static(js_src, self.js_dir / 'auto_bootstrap.min.js')
                
                # پاک کردن temp
                shutil.rmtree(temp_extract)
                
                return True
        
        except Exception as e:
            print(f"   ❌ خطا: {e}")
            return False
    
    def download_jquery(self, version: Optional[str] = None) -> bool:
        """دانلود jQuery"""
        version = version or self.VERSIONS['jquery']
        
        print(f"\n💎 jQuery {version}")
        print("-" * 60)
        
        url = f'https://code.jquery.com/jquery-{version}.min.js'
        
        # دانلود در temp
        temp_file = self.temp_dir / f'jquery-{version}.min.js'
        
        if self.download_file(url, temp_file):
            # کپی به static
            return self.copy_to_static(temp_file, self.js_dir / 'auto_jquery.min.js')
        
        return False
    
    def download_select2(self, version: Optional[str] = None) -> bool:
        """دانلود Select2"""
        version = version or self.VERSIONS['select2']
        
        print(f"\n🔽 Select2 {version}")
        print("-" * 60)
        
        # JS
        js_url = f'https://cdn.jsdelivr.net/npm/select2@{version}/dist/js/select2.min.js'
        temp_js = self.temp_dir / f'select2-{version}.min.js'
        
        js_ok = False
        if self.download_file(js_url, temp_js):
            js_ok = self.copy_to_static(temp_js, self.js_dir / 'auto_select2.min.js')
        
        # CSS
        css_url = f'https://cdn.jsdelivr.net/npm/select2@{version}/dist/css/select2.min.css'
        temp_css = self.temp_dir / f'select2-{version}.min.css'
        
        css_ok = False
        if self.download_file(css_url, temp_css):
            css_ok = self.copy_to_static(temp_css, self.css_dir / 'auto_select2.min.css')
        
        return js_ok and css_ok
    
    def download_datatables(self, version: Optional[str] = None) -> bool:
        """دانلود DataTables"""
        version = version or self.VERSIONS['datatables']
        
        print(f"\n📊 DataTables {version}")
        print("-" * 60)
        
        # JS
        js_url = f'https://cdn.datatables.net/{version}/js/jquery.dataTables.min.js'
        temp_js = self.temp_dir / f'datatables-{version}.min.js'
        
        js_ok = False
        if self.download_file(js_url, temp_js):
            js_ok = self.copy_to_static(temp_js, self.js_dir / 'auto_datatables.min.js')
        
        # CSS
        css_url = f'https://cdn.datatables.net/{version}/css/jquery.dataTables.min.css'
        temp_css = self.temp_dir / f'datatables-{version}.min.css'
        
        css_ok = False
        if self.download_file(css_url, temp_css):
            css_ok = self.copy_to_static(temp_css, self.css_dir / 'auto_datatables.min.css')
        
        return js_ok and css_ok
    
    def download_sweetalert2(self, version: Optional[str] = None) -> bool:
        """دانلود SweetAlert2"""
        version = version or self.VERSIONS['sweetalert2']
        
        print(f"\n🍭 SweetAlert2 {version}")
        print("-" * 60)
        
        # JS
        js_url = f'https://cdn.jsdelivr.net/npm/sweetalert2@{version}/dist/sweetalert2.all.min.js'
        temp_js = self.temp_dir / f'sweetalert2-{version}.min.js'
        
        js_ok = False
        if self.download_file(js_url, temp_js):
            js_ok = self.copy_to_static(temp_js, self.js_dir / 'auto_sweetalert2.min.js')
        
        # CSS
        css_url = f'https://cdn.jsdelivr.net/npm/sweetalert2@{version}/dist/sweetalert2.min.css'
        temp_css = self.temp_dir / f'sweetalert2-{version}.min.css'
        
        css_ok = False
        if self.download_file(css_url, temp_css):
            css_ok = self.copy_to_static(temp_css, self.css_dir / 'auto_sweetalert2.min.css')
        
        return js_ok and css_ok
    
    def download_chartjs(self, version: Optional[str] = None) -> bool:
        """دانلود Chart.js"""
        version = version or self.VERSIONS['chartjs']
        
        print(f"\n📈 Chart.js {version}")
        print("-" * 60)
        
        url = f'https://cdn.jsdelivr.net/npm/chart.js@{version}/dist/chart.umd.min.js'
        temp_file = self.temp_dir / f'chart-{version}.min.js'
        
        if self.download_file(url, temp_file):
            return self.copy_to_static(temp_file, self.js_dir / 'auto_chart.min.js')
        
        return False
    
    def download_fontawesome(self, version: Optional[str] = None) -> bool:
        """دانلود Font Awesome"""
        version = version or self.VERSIONS['fontawesome']
        
        print(f"\n🎨 Font Awesome {version}")
        print("-" * 60)
        
        url = f'https://use.fontawesome.com/releases/v{version}/fontawesome-free-{version}-web.zip'
        
        try:
            # دانلود
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = Request(url, headers=headers)
            
            print(f"   📥 دانلود ZIP (ممکنه کمی طول بکشه)...")
            
            with urlopen(req, timeout=90) as response:
                zip_content = response.read()
            
            size_mb = len(zip_content) / (1024 * 1024)
            print(f"   ✅ دانلود شد ({size_mb:.1f} MB)")
            
            # استخراج در temp
            temp_extract = self.temp_dir / 'fontawesome'
            temp_extract.mkdir(exist_ok=True)
            
            print(f"   📦 استخراج...")
            if self.extract_zip(zip_content, temp_extract):
                extracted_dir = temp_extract / f'fontawesome-free-{version}-web'
                
                # کپی به static
                print(f"   📋 کپی به static...")
                
                fa_dir = self.icons_dir / 'fontawesome'
                fa_dir.mkdir(exist_ok=True)
                
                # CSS
                css_src = extracted_dir / 'css'
                if css_src.exists():
                    css_dest = fa_dir / 'css'
                    if css_dest.exists():
                        shutil.rmtree(css_dest)
                    shutil.copytree(css_src, css_dest)
                    print(f"   ✅ CSS files ({len(list(css_dest.glob('*')))} files)")
                
                # Webfonts
                fonts_src = extracted_dir / 'webfonts'
                if fonts_src.exists():
                    fonts_dest = fa_dir / 'webfonts'
                    if fonts_dest.exists():
                        shutil.rmtree(fonts_dest)
                    shutil.copytree(fonts_src, fonts_dest)
                    print(f"   ✅ Webfonts ({len(list(fonts_dest.glob('*')))} files)")
                
                # پاک کردن temp
                shutil.rmtree(temp_extract)
                
                return True
        
        except Exception as e:
            print(f"   ❌ خطا: {e}")
            return False
    
    def download_jquery_ui(self, version: Optional[str] = None) -> bool:
        """دانلود jQuery UI"""
        version = version or self.VERSIONS['jquery_ui']
        
        print(f"\n🎨 jQuery UI {version}")
        print("-" * 60)
        
        # JS
        js_url = f'https://code.jquery.com/ui/{version}/jquery-ui.min.js'
        temp_js = self.temp_dir / f'jquery-ui-{version}.min.js'
        
        js_ok = False
        if self.download_file(js_url, temp_js):
            js_ok = self.copy_to_static(temp_js, self.js_dir / 'auto_jquery-ui.min.js')
        
        # CSS
        css_url = f'https://code.jquery.com/ui/{version}/themes/base/jquery-ui.min.css'
        temp_css = self.temp_dir / f'jquery-ui-{version}.min.css'
        
        css_ok = False
        if self.download_file(css_url, temp_css):
            css_ok = self.copy_to_static(temp_css, self.css_dir / 'auto_jquery-ui.min.css')
        
        return js_ok and css_ok
    
    def download_popper(self, version: Optional[str] = None) -> bool:
        """دانلود Popper.js"""
        version = version or self.VERSIONS['popper']
        
        print(f"\n🎈 Popper.js {version}")
        print("-" * 60)
        
        url = f'https://cdn.jsdelivr.net/npm/@popperjs/core@{version}/dist/umd/popper.min.js'
        temp_file = self.temp_dir / f'popper-{version}.min.js'
        
        if self.download_file(url, temp_file):
            return self.copy_to_static(temp_file, self.js_dir / 'auto_popper.min.js')
        
        return False
    
    def cleanup_temp(self):
        """پاک کردن پوشه temp"""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                print(f"\n🧹 پاک‌سازی temp: {self.temp_dir}")
        except Exception as e:
            print(f"\n⚠️ خطا در پاک‌سازی temp: {e}")
    
    def download_all(self, libraries: Optional[List[str]] = None):
        """دانلود همه کتابخانه‌ها"""
        
        available = {
            'bootstrap': self.download_bootstrap,
            'jquery': self.download_jquery,
            'select2': self.download_select2,
            'datatables': self.download_datatables,
            'sweetalert2': self.download_sweetalert2,
            'chartjs': self.download_chartjs,
            'fontawesome': self.download_fontawesome,
            'jquery_ui': self.download_jquery_ui,
            'popper': self.download_popper
        }
        
        if libraries is None:
            libraries = list(available.keys())
        
        print()
        print("=" * 70)
        print("📥 دانلود کتابخانه‌های CDN")
        print("=" * 70)
        print(f"📁 پروژه: {self.project_path}")
        
        results = {}
        
        for lib in libraries:
            if lib in available:
                try:
                    results[lib] = available[lib]()
                except Exception as e:
                    print(f"\n❌ خطای غیرمنتظره در {lib}: {e}")
                    results[lib] = False
            else:
                print(f"\n⚠️ {lib} پشتیبانی نمیشه")
                results[lib] = False
        
        # پاک کردن temp
        self.cleanup_temp()
        
        # خلاصه
        print()
        print("=" * 70)
        print("📊 خلاصه:")
        print("=" * 70)
        
        success = sum(1 for v in results.values() if v)
        total = len(results)
        
        print(f"✅ موفق: {success}/{total}")
        print()
        
        for lib, status in results.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {lib}")
        
        print()
        print("=" * 70)


def main():
    """تابع اصلی"""
    
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "📥 CDN Downloader" + " " * 32 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # بارگذاری کانفیگ
    config_file = Path('config.json')
    
    if not config_file.exists():
        print("❌ فایل config.json یافت نشد!")
        print("💡 ابتدا با project_manager.py پروژه رو اضافه کن")
        input("\nPress Enter to exit...")
        return
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ خطا در خواندن config: {e}")
        input("\nPress Enter to exit...")
        return
    
    projects = config.get('projects', {})
    enabled_projects = {k: v for k, v in projects.items() if v.get('enabled', False)}
    
    if not enabled_projects:
        print("❌ هیچ پروژه فعالی یافت نشد!")
        input("\nPress Enter to exit...")
        return
    
    # انتخاب پروژه
    print("📋 پروژه‌های فعال:")
    print("-" * 70)
    
    project_list = list(enabled_projects.items())
    
    for i, (proj_id, proj_data) in enumerate(project_list, 1):
        print(f"{i}. {proj_data['name']}")
        print(f"   📁 {proj_data['path']}")
    
    print()
    
    try:
        choice = int(input("انتخاب پروژه: ").strip())
        
        if choice < 1 or choice > len(project_list):
            print("❌ انتخاب نامعتبر!")
            return
        
        proj_id, proj_data = project_list[choice - 1]
        
    except ValueError:
        print("❌ ورودی نامعتبر!")
        return
    
    # انتخاب کتابخانه‌ها
    print()
    print("📦 کتابخانه‌ها:")
    print("-" * 70)
    print("1. Bootstrap")
    print("2. jQuery")
    print("3. Select2")
    print("4. DataTables")
    print("5. SweetAlert2")
    print("6. Chart.js")
    print("7. Font Awesome")
    print("8. jQuery UI")
    print("9. Popper.js")
    print("0. همه")
    print()
    
    selection = input("انتخاب (مثال: 1,2,3 یا 0 برای همه): ").strip()
    
    lib_map = {
        '1': 'bootstrap',
        '2': 'jquery',
        '3': 'select2',
        '4': 'datatables',
        '5': 'sweetalert2',
        '6': 'chartjs',
        '7': 'fontawesome',
        '8': 'jquery_ui',
        '9': 'popper'
    }
    
    if selection == '0':
        selected_libs = None  # همه
    else:
        selected_libs = [lib_map[s.strip()] for s in selection.split(',') if s.strip() in lib_map]
        
        if not selected_libs:
            print("❌ هیچ انتخابی معتبر نیست!")
            return
    
    # دانلود
    downloader = CDNDownloader(proj_data['path'])
    downloader.download_all(selected_libs)
    
    print()
    print("🎉 تمام!")
    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
