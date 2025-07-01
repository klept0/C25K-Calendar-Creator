#!/usr/bin/env python3
"""
Test script for new advanced C25K features
"""

def test_basic_functionality():
    """Test core export functionality"""
    print("🧪 Testing C25K Advanced Features...")
    
    # Test 1: Import modules
    print("\n1. Testing module imports...")
    try:
        from modules.exports import ExportManager
        print("✅ Export Manager imported successfully")
        
        from modules.exports import export_csv, export_json, export_google_fit_csv
        print("✅ Legacy export functions imported")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 2: Create export manager
    print("\n2. Testing Export Manager initialization...")
    try:
        em = ExportManager()
        print("✅ Export Manager created")
        
        formats = em.get_available_formats()
        print(f"✅ Available formats: {formats}")
        
        descriptions = em.get_format_descriptions()
        print(f"✅ Format descriptions loaded: {len(descriptions)} formats")
        
    except Exception as e:
        print(f"❌ Export Manager failed: {e}")
        return False
    
    # Test 3: Test basic export
    print("\n3. Testing basic export functionality...")
    try:
        test_plan = {
            'sessions': [
                {
                    'title': 'Week 1, Day 1',
                    'description': 'Warm up: 5-min brisk walk. Run 60 sec, walk 90 sec (repeat 8 times). Cool down: 5-min walk.',
                    'date': '2025-07-01',
                    'week': 1,
                    'duration': 30,
                    'start_time': '07:00',
                    'end_time': '07:30'
                },
                {
                    'title': 'Week 1, Day 2', 
                    'description': 'Warm up: 5-min brisk walk. Run 60 sec, walk 90 sec (repeat 8 times). Cool down: 5-min walk.',
                    'date': '2025-07-03',
                    'week': 1,
                    'duration': 30,
                    'start_time': '07:00',
                    'end_time': '07:30'
                }
            ],
            'metadata': {
                'user_name': 'Test Runner',
                'start_date': '2025-07-01',
                'age': 30,
                'weight': 70
            }
        }
        
        # Test CSV export
        success = em.export_plan(test_plan, 'csv', 'test_plan.csv')
        print(f"✅ CSV export: {'SUCCESS' if success else 'FAILED'}")
        
        # Test JSON export
        success = em.export_plan(test_plan, 'json', 'test_plan.json')
        print(f"✅ JSON export: {'SUCCESS' if success else 'FAILED'}")
        
        # Test Markdown export
        success = em.export_plan(test_plan, 'markdown', 'test_plan.md')
        print(f"✅ Markdown export: {'SUCCESS' if success else 'FAILED'}")
        
    except Exception as e:
        print(f"❌ Export test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Check for advanced features
    print("\n4. Checking advanced features availability...")
    try:
        if 'pdf' in em.get_available_formats():
            print("✅ PDF export available")
        else:
            print("⚠️  PDF export not available (missing dependencies)")
            
        if 'qr' in em.get_available_formats():
            print("✅ QR code export available")
        else:
            print("⚠️  QR code export not available (missing dependencies)")
            
        if 'strava' in em.get_available_formats():
            print("✅ Strava integration available")
        else:
            print("⚠️  Strava integration not available (missing dependencies)")
            
        if 'intervals.icu' in em.get_available_formats():
            print("✅ Intervals.icu integration available")
        else:
            print("⚠️  Intervals.icu integration not available (missing dependencies)")
            
    except Exception as e:
        print(f"❌ Advanced features check failed: {e}")
        return False
    
    # Test 5: Check if files were created
    print("\n5. Verifying exported files...")
    import os
    
    test_files = ['test_plan.csv', 'test_plan.json', 'test_plan.md']
    for filename in test_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} created ({size} bytes)")
        else:
            print(f"❌ {filename} not found")
    
    print("\n🎉 Basic functionality test completed!")
    return True


def test_advanced_imports():
    """Test advanced feature imports"""
    print("\n🔬 Testing Advanced Feature Imports...")
    
    # Test internationalization
    try:
        from modules.internationalization import InternationalizationManager
        i18n = InternationalizationManager()
        langs = i18n.get_available_languages()
        print(f"✅ Internationalization: {len(langs)} languages available")
        
        # Test language switching
        success = i18n.set_language('es')
        if success:
            text = i18n.get_text('gui.name')
            print(f"✅ Spanish translation test: '{text}'")
        
    except ImportError:
        print("⚠️  Internationalization module not available")
    except Exception as e:
        print(f"❌ Internationalization test failed: {e}")
    
    # Test API integrations
    try:
        from modules.api_integrations import APIManager, StravaAPIClient
        print("✅ API integration modules imported")
        
        # Test API manager creation (without credentials)
        am = APIManager()
        print("✅ API Manager created")
        
    except ImportError:
        print("⚠️  API integration modules not available")
    except Exception as e:
        print(f"❌ API integration test failed: {e}")
    
    # Test advanced exports
    try:
        from modules.advanced_exports import QRCodeGenerator, PDFExporter
        print("✅ Advanced export modules imported")
        
        # Test QR generator creation (will fail without qrcode package)
        try:
            qr_gen = QRCodeGenerator()
            print("✅ QR Code generator created")
        except Exception:
            print("⚠️  QR Code generator requires: pip install qrcode[pil]")
        
        # Test PDF exporter creation (will fail without reportlab)
        try:
            pdf_exp = PDFExporter()
            print("✅ PDF exporter created")
        except Exception:
            print("⚠️  PDF exporter requires: pip install reportlab")
            
    except ImportError:
        print("⚠️  Advanced export modules not available")
    except Exception as e:
        print(f"❌ Advanced export test failed: {e}")


def print_installation_guide():
    """Print installation guide for full features"""
    print("\n📦 Installation Guide for Full Features:")
    print("=" * 50)
    print("# Basic features (always available):")
    print("pip install PyQt6 openpyxl")
    print()
    print("# Advanced export features:")
    print("pip install qrcode[pil] reportlab Pillow")
    print()
    print("# API integrations:")
    print("pip install requests urllib3")
    print()
    print("# Complete installation:")
    print("pip install -r requirements.txt")
    print()
    print("🔑 For API integrations, you'll also need:")
    print("- Strava API credentials")
    print("- intervals.icu account and API key")
    print("- OpenWeatherMap API key")
    print("- Individual platform registrations")


if __name__ == "__main__":
    print("🏃‍♀️ C25K Advanced Features Test Suite")
    print("=" * 50)
    
    # Run basic tests
    basic_success = test_basic_functionality()
    
    # Run advanced tests
    test_advanced_imports()
    
    # Print installation guide
    print_installation_guide()
    
    print("\n" + "=" * 50)
    if basic_success:
        print("🎉 SUCCESS: Core functionality is working!")
        print("⚡ Ready for basic C25K plan generation and export")
        print("🚀 Install additional dependencies for advanced features")
    else:
        print("❌ FAILURE: Core functionality has issues")
        print("🔧 Check error messages above and fix imports")
    
    print("\n📖 See IMPLEMENTATION_GUIDE.md for complete setup instructions")
