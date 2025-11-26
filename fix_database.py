"""
Database.py dosyasını otomatik düzelt
Tüm conn.commit() ve return ifadelerinden önce conn.close() ekle
"""

import re

# Dosyayı oku
with open('src/database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# İlk önce tüm conn.commit() ifadelerinden sonra conn.close() ekle
# Ama zaten conn.close() varsa tekrar ekleme
content = re.sub(
    r'(conn\.commit\(\))\n(\s+)(?!conn\.close)',
    r'\1\n\2conn.close()\n\2',
    content
)

# SELECT sorgularında conn.close() ekle
# Patern: cursor.fetchone() veya cursor.fetchall() sonrası return'den önce
def add_close_before_return(match):
    indent = match.group(1)
    fetch_line = match.group(2)
    return_line = match.group(3)
    
    # Eğer close yoksa ekle
    if 'conn.close()' not in fetch_line:
        return f"{indent}{fetch_line}\n{indent}conn.close()\n{indent}{return_line}"
    return match.group(0)

# fetchone() sonrası return
content = re.sub(
    r'(\s+)(.*cursor\.fetchone\(\).*)\n(\s+)(return .*)',
    lambda m: f"{m.group(1)}{m.group(2)}\n{m.group(1)}conn.close()\n{m.group(3)}{m.group(4)}",
    content
)

# fetchall() sonrası return
content = re.sub(
    r'(\s+)(.*cursor\.fetchall\(\).*)\n(\s+)(return .*)',
    lambda m: f"{m.group(1)}{m.group(2)}\n{m.group(1)}conn.close()\n{m.group(3)}{m.group(4)}",
    content
)

# Dosyayı kaydet
with open('src/database_fixed.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ database_fixed.py oluşturuldu")
print("✓ Kontrol et ve doğruysa: move src\\database_fixed.py src\\database.py")
