#!/usr/bin/env python3
"""
🧪 Deployment Test Script for FoodSaver
Tests all critical dependencies and configurations
"""

import sys
import importlib
import os

def test_dependencies():
    """Test if all required packages can be imported"""
    print("🔍 Testing dependencies...")
    
    required_packages = [
        'flask',
        'PIL',  # Pillow
        'numpy',
        'requests',
        'sqlite3',  # Built-in
        'hashlib',  # Built-in
        'datetime', # Built-in
    ]
    
    failed = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError as e:
            print(f"❌ {package} - FAILED: {e}")
            failed.append(package)
    
    return failed

def test_environment_variables():
    """Test environment variables setup"""
    print("\n🔧 Testing environment variables...")
    
    required_vars = ['SECRET_KEY', 'HUGGINGFACE_API_KEY']
    optional_vars = ['PORT', 'FLASK_ENV']
    
    missing = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} - Set")
        else:
            print(f"⚠️  {var} - Not set (required for production)")
            missing.append(var)
    
    for var in optional_vars:
        value = os.getenv(var, 'default')
        print(f"ℹ️  {var} - {value}")
    
    return missing

def test_flask_app():
    """Test Flask app creation"""
    print("\n🌐 Testing Flask app...")
    
    try:
        from app import app
        print("✅ Flask app created successfully")
        
        # Test a simple route
        with app.test_client() as client:
            response = client.get('/test')
            if response.status_code == 200:
                print("✅ Test route working")
            else:
                print(f"⚠️  Test route returned status: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Flask app failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 FoodSaver Deployment Test Suite")
    print("=" * 50)
    
    # Test dependencies
    failed_deps = test_dependencies()
    
    # Test environment variables
    missing_vars = test_environment_variables()
    
    # Test Flask app
    app_works = test_flask_app()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    
    if not failed_deps and app_works:
        print("✅ All tests passed! Ready for deployment.")
        if missing_vars:
            print("⚠️  Remember to set environment variables in Render:")
            for var in missing_vars:
                print(f"   - {var}")
        sys.exit(0)
    else:
        print("❌ Some tests failed:")
        if failed_deps:
            print(f"   - Failed dependencies: {', '.join(failed_deps)}")
        if not app_works:
            print("   - Flask app failed to start")
        sys.exit(1)

if __name__ == "__main__":
    main()
