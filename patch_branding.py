#!/usr/bin/env python3
import os
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def patch_file(path, replacements):
    full_path = os.path.join(ROOT_DIR, path)
    if not os.path.exists(full_path):
        print(f"[WARN] File not found: {full_path}")
        return False
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    for pattern, repl in replacements:
        if isinstance(pattern, str):
            content = content.replace(pattern, repl)
        else:
            content = pattern.sub(repl, content)
            
    if content != original:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Patched: {path}")
        return True
    else:
        print(f"[SKIP] No changes needed: {path}")
        return False

def apply_branding():
    print("--- Applying RC Desk Branding ---")
    
    # 1. libs/hbb_common/src/config.rs
    patch_file("libs/hbb_common/src/config.rs", [
        (
            'pub static ref APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned());',
            'pub static ref APP_NAME: RwLock<String> = RwLock::new("RC Desk".to_owned());'
        ),
        (
            'pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];',
            'pub const RENDEZVOUS_SERVERS: &[&str] = &["rc2.remoto365.com.br"];'
        ),
        (
            'pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";',
            'pub const RS_PUB_KEY: &str = "ApFNkafMSE4ZgabxvgyaxO7na0lxd44rLn6bqU8ZeDc=";'
        ),
    ])
    
    # 2. libs/portable/src/main.rs
    patch_file("libs/portable/src/main.rs", [
        (
            'const APP_PREFIX: &str = "rustdesk";',
            'const APP_PREFIX: &str = "rcdesk";'
        ),
    ])
    
    # 3. libs/portable/Cargo.toml
    patch_file("libs/portable/Cargo.toml", [
        (
            'LegalCopyright = "Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved."',
            'LegalCopyright = "Copyright © 2026 RC Remote. All rights reserved."'
        ),
        (
            'ProductName = "RustDesk"',
            'ProductName = "RC Desk"'
        ),
        (
            'OriginalFilename = "rustdesk.exe"',
            'OriginalFilename = "rcdesk.exe"'
        ),
        (
            'FileDescription = "RustDesk Remote Desktop"',
            'FileDescription = "RC Desk Remote Desktop"'
        ),
    ])
    
    # 4. flutter/windows/runner/Runner.rc
    patch_file("flutter/windows/runner/Runner.rc", [
        (
            'VALUE "CompanyName", "Purslane Tech Pte. Ltd." "\\0"',
            'VALUE "CompanyName", "RC Remote" "\\0"'
        ),
        (
            'VALUE "FileDescription", "RustDesk Remote Desktop" "\\0"',
            'VALUE "FileDescription", "RC Desk Remote Desktop" "\\0"'
        ),
        (
            'VALUE "InternalName", "rustdesk" "\\0"',
            'VALUE "InternalName", "rcdesk" "\\0"'
        ),
        (
            'VALUE "LegalCopyright", "Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved." "\\0"',
            'VALUE "LegalCopyright", "Copyright © 2026 RC Remote. All rights reserved." "\\0"'
        ),
        (
            'VALUE "OriginalFilename", "rustdesk.exe" "\\0"',
            'VALUE "OriginalFilename", "rcdesk.exe" "\\0"'
        ),
        (
            'VALUE "ProductName", "RustDesk" "\\0"',
            'VALUE "ProductName", "RC Desk" "\\0"'
        ),
    ])
    
    # 5. src/common.rs (Support both rcdesk:// and rustdesk:// uri prefixes)
    patch_file("src/common.rs", [
        (
            'pub fn is_empty_uni_link(arg: &str) -> bool {\n    let prefix = crate::get_uri_prefix();\n    if !arg.starts_with(&prefix) {\n        return false;\n    }\n    arg[prefix.len()..].chars().all(|c| c == \'/\')\n}',
            'pub fn is_empty_uni_link(arg: &str) -> bool {\n    let prefix = crate::get_uri_prefix();\n    if arg.starts_with(&prefix) {\n        return arg[prefix.len()..].chars().all(|c| c == \'/\');\n    }\n    if arg.starts_with("rustdesk://") {\n        return arg["rustdesk://".len()..].chars().all(|c| c == \'/\');\n    }\n    false\n}'
        ),
    ])

    # 6. src/platform/windows.rs (Register both rcdesk and rustdesk protocols in Windows registry)
    target_str = '    reg add HKEY_CLASSES_ROOT\\\\{ext} /f\\n    reg add HKEY_CLASSES_ROOT\\\\{ext} /f /v \\"URL Protocol\\" /t REG_SZ /d \\"\\"\\n    reg add HKEY_CLASSES_ROOT\\\\{ext}\\\\shell /f\\n    reg add HKEY_CLASSES_ROOT\\\\{ext}\\\\shell\\\\open /f\\n    reg add HKEY_CLASSES_ROOT\\\\{ext}\\\\shell\\\\open\\\\command /f\\n    reg add HKEY_CLASSES_ROOT\\\\{ext}\\\\shell\\\\open\\\\command /f /ve /t REG_SZ /d \\"\\\\\\"{nested_exe}\\\\\\" \\\\\\"%%1\\\\\\"\\"'
    repl_str = target_str + '\\n    reg add HKEY_CLASSES_ROOT\\\\rustdesk /f\\n    reg add HKEY_CLASSES_ROOT\\\\rustdesk /f /v \\"URL Protocol\\" /t REG_SZ /d \\"\\"\\n    reg add HKEY_CLASSES_ROOT\\\\rustdesk\\\\shell /f\\n    reg add HKEY_CLASSES_ROOT\\\\rustdesk\\\\shell\\\\open /f\\n    reg add HKEY_CLASSES_ROOT\\\\rustdesk\\\\shell\\\\open\\\\command /f\\n    reg add HKEY_CLASSES_ROOT\\\\rustdesk\\\\shell\\\\open\\\\command /f /ve /t REG_SZ /d \\"\\\\\\"{nested_exe}\\\\\\" \\\\\\"%%1\\\\\\"\\"'
    patch_file("src/platform/windows.rs", [
        (target_str, repl_str)
    ])

    # 7. Translations: src/lang/ptbr.rs
    patch_file("src/lang/ptbr.rs", [
        ('RustDesk', 'RC Desk'),
    ])

    # 8. Translations: src/lang/en.rs
    patch_file("src/lang/en.rs", [
        ('RustDesk', 'RC Desk'),
    ])

    # 9. flutter/lib/common.dart (Hide Powered by RustDesk)
    patch_file("flutter/lib/common.dart", [
        (
            'Widget loadPowered(BuildContext context) {',
            'Widget loadPowered(BuildContext context) {\n  return const SizedBox.shrink();'
        )
    ])

    print("--- RC Desk Branding Applied Successfully ---")

if __name__ == "__main__":
    apply_branding()
