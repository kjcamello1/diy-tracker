#!/usr/bin/env python3
import os
import shutil
import utils

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white

template_dir = 'template/forms'
index_src = os.path.join(template_dir, 'index_temp.html')
index_dst = os.path.join(template_dir, 'index.html')

try:
    # Make sure template directory exists
    if not os.path.exists(template_dir):
        os.makedirs(template_dir, exist_ok=True)

    # Copy HTML
    with open(index_src, 'r') as f:
        html = f.read()
    with open(index_dst, 'w') as out:
        out.write(html)

    # Copy PHP handlers from base template (if they exist)
    base_php_dir = 'php'
    for handler in ['info_handler.php', 'result_handler.php', 'error_handler.php']:
        src = os.path.join(base_php_dir, handler)
        dst = os.path.join(template_dir, handler)
        if os.path.exists(src):
            shutil.copy(src, dst)

    # Copy JS folder if missing
    js_src = os.path.join(template_dir, 'js')
    if not os.path.exists(js_src):
        os.makedirs(js_src, exist_ok=True)

    # Set proper permissions
    os.chmod(template_dir, 0o755)
    for root, dirs, files in os.walk(template_dir):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)

    utils.print(f'{G}[+] {C}Form (Consent Demo) template loaded successfully!{W}')

except Exception as e:
    utils.print(f'{R}[-] {C}Error preparing form template: {e}{W}')
