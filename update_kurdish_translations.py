#!/usr/bin/env python3
"""
Script to update Kurdish translations in Django .po files
"""

import re
import os

# Kurdish Sorani (ckb) Translations
translations_ckb = {
    # Navigation and Main UI
    "Home": "ماڵەوە",
    "Dashboard": "پانێل",
    "Destinations": "شوێنەکانی خوێندن",
    "Resume Builder": "درووستکردنی ژیان نامە", 
    "Communications": "پەیوەندیکردن",
    "Resources": "سەرچاوەکان",
    "Login": "چوونەژوورەوە",
    "Register": "خۆتۆمارکردن",
    "Logout": "چوونەدەرەوە",
    "Profile": "پرۆفایل",
    
    # Regional Names
    "Rojhelat": "ڕۆژهەڵات",
    "Başûr": "باشوور",
    "Bakûr": "باکوور", 
    "Rojava": "ڕۆژئاوا",
    "Diaspora": "دەرەوەی وڵات",
    
    # Educational Terms
    "Bachelor's Degree": "بەکالۆریۆس",
    "Master's Degree": "ماستەر",
    "PhD": "دکتۆرا",
    "Postdoctoral": "پاش دکتۆرا",
    "Certificate": "بڕوانامە",
    "Diploma": "دیپلۆما",
    "Professional Degree": "بڕوانامەی پیشەیی",
    
    # Countries and Places
    "Countries": "وڵاتان",
    "Universities": "زانکۆکان", 
    "Programs": "بەرنامەکان",
    "Scholarships": "بورسەکان",
    "City": "شار",
    "Country": "وڵات",
    
    # Application Terms
    "Apply": "داخوازینامە",
    "Application": "داخوازینامە",
    "Applications": "داخوازینامەکان",
    "Status": "دۆخ",
    "Deadline": "کاتی کۆتایی", 
    "Requirements": "پێداویستیەکان",
    
    # Common Actions
    "Search": "گەڕان",
    "Filter": "پاڵاوتن",
    "View": "بینین",
    "Edit": "دەستکاریکردن",
    "Delete": "سڕینەوە",
    "Save": "پاشەکەوتکردن",
    "Cancel": "هەڵوەشاندنەوە",
    "Submit": "ناردن",
    "Create": "درووستکردن",
    "Update": "نوێکردنەوە",
    
    # Profile and Personal Info
    "Name": "ناو",
    "First Name": "ناوی یەکەم", 
    "Last Name": "ناوی کۆتایی",
    "Email": "ئیمەیل",
    "Phone Number": "ژمارەی تەلەفۆن",
    "Address": "ناونیشان",
    "Date of Birth": "ڕێکەوتی لەدایکبوون",
    "Gender": "ڕەگەز",
    "Biography": "ژیاننامە",
    
    # Academic Information
    "Field of Study": "بواری خوێندن",
    "Current Education Level": "ئاستی خوێندنی ئێستا",
    "Preferred Study Level": "ئاستی خوێندنی دڵخواز",
    "GPA": "نمرەی گشتی",
    "Graduation Year": "ساڵی دەرچوون",
    "University Name": "ناوی زانکۆ",
    "Research Interests": "بەرژەوەندیەکانی تویژینەوە",
    "Academic Awards": "خەڵاتەکانی ئەکادیمی",
    "Publications": "بڵاوکراوەکان",
    
    # Experience
    "Work Experience": "ئەزموونی کار",
    "Volunteer Experience": "ئەزموونی خۆبەخشانە", 
    "Technical Skills": "لێهاتوویی تەکنیکی",
    "Language Skills": "لێهاتوویی زمان",
    "Experience": "ئەزموون",
    "Education": "خوێندن",
    "Skills": "لێهاتووی",
    
    # Welcome Messages
    "Welcome": "بەخێربێیت",
    "Welcome back": "بەخێربگەڕێیتەوە",
    "Get Started": "دەستپێکردن", 
    "Welcome Back": "بەخێربگەڕێیتەوە",
    
    # Kurdish Specific Terms
    "Kurdish Students": "خوێندکارانی کورد",
    "Kurdish Community": "کۆمەڵگای کوردی",
    "Kurdish Language": "زمانی کوردی",
    "Kurdish Region": "هەرێمی کوردی",
    "Kurdish Name": "ناوی کوردی",
    
    # Long Texts
    "Your Journey to Higher Education Starts Here": "گەشتەکەت بۆ خوێندنی بەرز لێرەوە دەستپێدەکات",
    "Supporting Kurdish students from all regions": "پشتگیری خوێندکارانی کورد لە هەموو هەرێمەکان",
    "Find Your Perfect Study Destination": "شوێنی تەواوی خوێندنەکەت بدۆزەرەوە",
    
    # Buttons
    "Learn More": "زیاتر بزانە",
    "View Details": "وردەکاریەکان ببینە",
    "View All": "هەموو ببینە",
    "Continue": "بەردەوامبوون",
    "Next": "دواتر",
    "Previous": "پێشتر",
    
    # Time
    "ago": "لەمەوپێش",
    "Updated": "نوێکراوەتەوە",
    
    # Basic Information
    "Basic Information": "زانیاری بنەڕەتی",
    "Contact Information": "زانیاری پەیوەندیکردن",
    "Academic Information": "زانیاری ئەکادیمی",
    "Regional & Academic Information": "زانیاری هەرێمی و ئەکادیمی",
    
    # More terms
    "Create Account": "هەژماری دروست بکە",
    "Sign in to continue your academic journey": "بچۆرەوە ناوەوە بۆ بەردەوامبوونی گەشتی ئەکادیمیت",
    "Username": "ناوی بەکارهێنەر",
    "Password": "وشەی نهێنی",
    "Sign In": "چوونەژوورەوە",
    "My Resumes": "ژیان نامەکانم",
    "Create New Resume": "ژیان نامەی نوێ دروست بکە",
}

# Kurdish Kurmanji (kmr) Translations  
translations_kmr = {
    # Navigation and Main UI
    "Home": "Malper",
    "Dashboard": "Panel", 
    "Destinations": "Ciyên Xwendinê",
    "Resume Builder": "Avakirina Jiyannameyê",
    "Communications": "Girêdan",
    "Resources": "Çavkanî",
    "Login": "Têkevtin",
    "Register": "Tomarkirin",
    "Logout": "Derketin",
    "Profile": "Profîl",
    
    # Regional Names
    "Rojhelat": "Rojhilat",
    "Başûr": "Başûr",
    "Bakûr": "Bakur", 
    "Rojava": "Rojava",
    "Diaspora": "Derveyî Welat",
    
    # Educational Terms
    "Bachelor's Degree": "Bakalorius",
    "Master's Degree": "Master", 
    "PhD": "Doktora",
    "Postdoctoral": "Piştî Doktorayê",
    "Certificate": "Sertîfîka",
    "Diploma": "Dîploma",
    "Professional Degree": "Dereceya Profesyonel",
    
    # Countries and Places
    "Countries": "Welat",
    "Universities": "Zanîngehan",
    "Programs": "Bername", 
    "Scholarships": "Bursan",
    "City": "Bajar",
    "Country": "Welat",
    
    # Common Actions
    "Search": "Lêgerîn",
    "Filter": "Parzûnkirin", 
    "View": "Dîtin",
    "Edit": "Guharin",
    "Delete": "Jêbirin",
    "Save": "Tomarkirin",
    "Cancel": "Betal",
    "Submit": "Şandin",
    "Create": "Afirandin",
    "Update": "Nûkirin",
    
    # Profile and Personal Info
    "Name": "Nav",
    "First Name": "Navê Yekem",
    "Last Name": "Navê Paşîn",
    "Email": "E-mail",
    "Phone Number": "Hejmara Têlefonê", 
    "Address": "Navnîşan",
    "Biography": "Jiyanname",
    
    # Academic Information
    "Field of Study": "Qada Xwendinê",
    "Current Education Level": "Asta Xwendina Niha",
    "Preferred Study Level": "Asta Xwendina Dilxwaz",
    "GPA": "Nota Giştî",
    "University Name": "Navê Zanîngehê",
    "Research Interests": "Berjewendiyên Lêkolînê",
    
    # Welcome Messages
    "Welcome": "Bi xêr hatî",
    "Welcome back": "Bi xêr vegere",
    "Get Started": "Destpêkirin",
    "Welcome Back": "Bi xêr vegere",
    
    # Kurdish Specific Terms
    "Kurdish Students": "Xwendekarên Kurd",
    "Kurdish Community": "Civaka Kurd", 
    "Kurdish Language": "Zimanê Kurdî",
    "Kurdish Region": "Herêma Kurd",
    "Kurdish Name": "Navê Kurdî",
    
    # Basic Information
    "Basic Information": "Agahdariya Bingehîn",
    "Contact Information": "Agahdariya Girêdanê",
    "Academic Information": "Agahdariya Akademîk",
    "Regional & Academic Information": "Agahdariya Herêmî û Akademîk",
}

def update_po_file(po_file_path, translations):
    """Update a .po file with translations"""
    if not os.path.exists(po_file_path):
        print(f"File not found: {po_file_path}")
        return
        
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_count = 0
    for english, translation in translations.items():
        # Escape quotes in the translation
        escaped_translation = translation.replace('"', '\\"')
        
        # Pattern to match msgid "English" followed by empty msgstr ""
        pattern = rf'(msgid "{re.escape(english)}"\s*\n\s*msgstr\s*)""\s*\n'
        replacement = rf'\1"{escaped_translation}"\n'
        
        new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
        if count > 0:
            content = new_content
            updated_count += count
            print(f"Updated: '{english}' -> '{translation}'")
    
    # Write back to file
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {updated_count} translations in {po_file_path}")

def main():
    base_dir = os.path.dirname(__file__)
    
    # Update Kurdish Sorani translations
    ckb_po_path = os.path.join(base_dir, 'locale/ckb/LC_MESSAGES/django.po')
    print("Updating Kurdish Sorani (ckb) translations...")
    update_po_file(ckb_po_path, translations_ckb)
    
    # Update Kurdish Kurmanji translations
    kmr_po_path = os.path.join(base_dir, 'locale/kmr/LC_MESSAGES/django.po')
    print("\nUpdating Kurdish Kurmanji (kmr) translations...")
    update_po_file(kmr_po_path, translations_kmr)
    
    print("\n✅ Translation update complete!")
    print("Run 'python manage.py compilemessages' to apply changes.")

if __name__ == "__main__":
    main()
