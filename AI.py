#!/usr/bin/env python3

import requests
import sys
import os
import json
import time
import base64
from pathlib import Path
from urllib.parse import urlencode, quote

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    END = '\033[0m'
    BOLD = '\033[1m'

class AKAI:
    def __init__(self):
        self.github = "https://github.com/ak404z"
        self.telegram = "https://t.me/AKserver404"
        self.version = "3.0"
        
    def banner(self):
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ▄▄▄       ██ ▄█▀    ▄▄▄       ██▓                        ║
║    ▒████▄     ██▄█▒    ▒████▄    ▓██▒                        ║
║    ▒██  ▀█▄  ▓███▄░    ▒██  ▀█▄  ▒██▒                        ║
║    ░██▄▄▄▄██ ▓██ █▄    ░██▄▄▄▄██ ░██░                        ║
║     ▓█   ▓██▒▒██▒ █▄    ▓█   ▓██▒░██░                        ║
║     ▒▒   ▓▒█░▒ ▒▒ ▓▒    ▒▒   ▓▒█░░▓                          ║
║      ▒   ▒▒ ░░ ░▒ ▒░     ▒   ▒▒ ░ ▒ ░                        ║
║      ░   ▒   ░ ░░ ░      ░   ▒    ▒ ░                        ║
║          ░  ░░  ░            ░  ░ ░                          ║
║                                                              ║
║          {Colors.YELLOW}🚀 Professional AI Tools 🚀{Colors.CYAN}                         ║
║                                                              ║
║  {Colors.WHITE}Github  : {Colors.GREEN}{self.github:<45}{Colors.CYAN}     ║
║  {Colors.WHITE}Telegram : {Colors.GREEN}{self.telegram:<45}{Colors.CYAN}    ║
║  {Colors.WHITE}Powerd By : {Colors.GREEN}AK {Colors.GREEN}(;{Colors.CYAN}                                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}"""
        print(banner)
    
    def menu(self):
        menu = f"""
{Colors.YELLOW}{Colors.BOLD}Choose an option below:{Colors.END}

{Colors.GREEN}[1]{Colors.END} {Colors.BOLD}🎨 AI Image Generator{Colors.END}      - Create high-quality images
{Colors.GREEN}[2]{Colors.END} {Colors.BOLD}🌐 AI Translator{Colors.END}           - Translate 100+ languages
{Colors.GREEN}[3]{Colors.END} {Colors.BOLD}📧 AI Email Writer{Colors.END}         - Professional emails
{Colors.GREEN}[4]{Colors.END} {Colors.BOLD}💡 AI Code Generator{Colors.END}       - Generate code with AI
{Colors.GREEN}[5]{Colors.END} {Colors.BOLD}🔊 AI Text to Speech{Colors.END}       - Natural voice synthesis
{Colors.GREEN}[6]{Colors.END} {Colors.BOLD}🖼️  AI Image Editor{Colors.END}        - Edit & enhance images

{Colors.RED}[0]{Colors.END} {Colors.BOLD}Exit{Colors.END}

{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""
        print(menu)
    
    def image_generator(self):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}🎨 AI Image Generator{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
        
        prompt = input(f"{Colors.YELLOW}Description:{Colors.END} ").strip()
        if not prompt:
            print(f"{Colors.RED}[✗] Empty!{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}Quality:{Colors.END} [1] Ultra  [2] High  [3] Medium  [4] Fast")
        q = input(f"{Colors.YELLOW}Choose [1]:{Colors.END} ").strip() or "1"
        
        qmap = {
            "1": ", ultra detailed, 8k uhd, masterpiece, high quality, sharp focus",
            "2": ", highly detailed, 4k, high resolution",
            "3": ", detailed, good quality",
            "4": ""
        }
        
        enhanced = prompt + qmap.get(q, qmap["1"])
        output = input(f"{Colors.YELLOW}Filename [output.jpg]:{Colors.END} ").strip() or "output.jpg"
        
        if not output.endswith(('.jpg', '.png')):
            output += '.jpg'
        
        print(f"\n{Colors.BLUE}[*]{Colors.END} Generating image (this may take a moment)...")
        
        try:
            # Step 1: Generate image
            params = {'text': enhanced}
            url = f"https://zecora0.serv00.net/ai/NanoBanana.php?{urlencode(params)}"
            
            response = requests.get(url, timeout=120)
            
            if response.status_code != 200:
                print(f"{Colors.RED}[✗]{Colors.END} API server error")
                return
            
            result = response.json()
            
            if not result.get('success'):
                error = result.get('error', 'Unknown error')
                print(f"{Colors.RED}[✗]{Colors.END} Generation failed: {error}")
                return
            
            img_url = result.get('url')
            if not img_url:
                print(f"{Colors.RED}[✗]{Colors.END} No image URL received")
                return
            
            print(f"{Colors.GREEN}[✓]{Colors.END} Image generated!")
            print(f"{Colors.BLUE}[*]{Colors.END} Downloading from: {img_url[:50]}...")
            
            # Step 2: Download image with retries
            max_attempts = 3
            
            for attempt in range(max_attempts):
                try:
                    if attempt > 0:
                        print(f"{Colors.YELLOW}[!]{Colors.END} Retry {attempt + 1}/{max_attempts}...")
                        time.sleep(2)
                    
                    img_response = requests.get(
                        img_url, 
                        timeout=180,  # 3 minutes timeout
                        stream=True,
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    
                    if img_response.status_code == 200:
                        # Download in chunks
                        total_size = 0
                        with open(output, 'wb') as f:
                            for chunk in img_response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    total_size += len(chunk)
                        
                        file_size = total_size / 1024
                        print(f"{Colors.GREEN}[✓]{Colors.END} Downloaded successfully!")
                        print(f"{Colors.GREEN}[✓]{Colors.END} Saved: {Colors.BOLD}{os.path.abspath(output)}{Colors.END}")
                        print(f"{Colors.GREEN}[✓]{Colors.END} Size: {file_size:.1f} KB")
                        return  # Success!
                    else:
                        print(f"{Colors.RED}[✗]{Colors.END} Download failed: HTTP {img_response.status_code}")
                        
                except requests.exceptions.Timeout:
                    if attempt < max_attempts - 1:
                        print(f"{Colors.YELLOW}[!]{Colors.END} Download timeout - retrying...")
                    else:
                        print(f"{Colors.RED}[✗]{Colors.END} Download timeout after {max_attempts} attempts")
                        print(f"{Colors.YELLOW}[!]{Colors.END} The image server is very slow")
                        print(f"{Colors.YELLOW}[!]{Colors.END} Image URL: {img_url}")
                        print(f"{Colors.YELLOW}[!]{Colors.END} You can try downloading manually")
                
                except requests.exceptions.ConnectionError:
                    if attempt < max_attempts - 1:
                        print(f"{Colors.YELLOW}[!]{Colors.END} Connection error - retrying...")
                    else:
                        print(f"{Colors.RED}[✗]{Colors.END} Connection failed after {max_attempts} attempts")
                
                except Exception as e:
                    if attempt < max_attempts - 1:
                        print(f"{Colors.YELLOW}[!]{Colors.END} Error: {str(e)[:50]} - retrying...")
                    else:
                        print(f"{Colors.RED}[✗]{Colors.END} Failed: {str(e)[:80]}")
            
        except requests.exceptions.Timeout:
            print(f"{Colors.RED}[✗]{Colors.END} API timeout - server is slow")
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}[✗]{Colors.END} Cannot connect to API server")
        except Exception as e:
            print(f"{Colors.RED}[✗]{Colors.END} Error: {str(e)[:80]}")
    
    def translator(self):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}🌐 AI Translator{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
        
        text = input(f"{Colors.YELLOW}Text:{Colors.END} ").strip()
        if not text:
            return
        
        print(f"\n{Colors.CYAN}Language:{Colors.END} [1] Arabic  [2] English  [3] Spanish  [4] French  [5] German")
        lang = input(f"{Colors.YELLOW}Choose:{Colors.END} ").strip() or "1"
        
        langs = {"1": "ar", "2": "en", "3": "es", "4": "fr", "5": "de"}
        target = langs.get(lang, "ar")
        
        print(f"\n{Colors.BLUE}[*]{Colors.END} Translating...")
        
        try:
            # Try Google Translate first (fastest)
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target}&dt=t&q={quote(text)}"
            r = requests.get(url, timeout=10)
            
            if r.status_code == 200:
                result = r.json()
                translated = ''.join([item[0] for item in result[0] if item[0]])
                
                if translated:
                    print(f"\n{Colors.GREEN}{'─'*60}{Colors.END}")
                    print(f"{Colors.CYAN}{translated}{Colors.END}")
                    print(f"{Colors.GREEN}{'─'*60}{Colors.END}")
                    return
        except:
            pass
        
        # Fallback to MyMemory
        try:
            url = f"https://api.mymemory.translated.net/get?q={quote(text)}&langpair=auto|{target}"
            r = requests.get(url, timeout=10)
            
            if r.status_code == 200:
                translated = r.json().get('responseData', {}).get('translatedText', '')
                
                if translated:
                    print(f"\n{Colors.GREEN}{'─'*60}{Colors.END}")
                    print(f"{Colors.CYAN}{translated}{Colors.END}")
                    print(f"{Colors.GREEN}{'─'*60}{Colors.END}")
                    return
        except:
            pass
        
        print(f"{Colors.RED}[✗]{Colors.END} Translation failed - try again")
    
    def email_writer(self):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}📧 AI Email Writer{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
        
        print(f"{Colors.CYAN}Templates:{Colors.END}")
        print("[1] Business  [2] Job Application  [3] Follow-up  [4] Thank You")
        
        choice = input(f"\n{Colors.YELLOW}Template:{Colors.END} ").strip() or "1"
        recipient = input(f"{Colors.YELLOW}Recipient:{Colors.END} ").strip() or "Recipient"
        subject = input(f"{Colors.YELLOW}Subject:{Colors.END} ").strip()
        context = input(f"{Colors.YELLOW}Details:{Colors.END} ").strip()
        
        templates = {
            "1": f"""Subject: {subject}

Dear {recipient},

I hope this email finds you well. I am writing to discuss {context}.

{context}

I would welcome the opportunity to discuss this further at your convenience.

Best regards,
AK""",
            "2": f"""Subject: Application - {subject}

Dear {recipient},

I am writing to express my interest in the {subject} position.

{context}

Thank you for considering my application.

Best regards,
AK""",
            "3": f"""Subject: Follow-up - {subject}

Dear {recipient},

I wanted to follow up on {subject}.

{context}

Looking forward to your response.

Best regards,
AK""",
            "4": f"""Subject: Thank You - {subject}

Dear {recipient},

Thank you for {context}.

Your support is greatly appreciated.

Warm regards,
AK"""
        }
        
        email = templates.get(choice, templates["1"])
        
        print(f"\n{Colors.GREEN}{'─'*60}{Colors.END}")
        print(f"{Colors.CYAN}{email}{Colors.END}")
        print(f"{Colors.GREEN}{'─'*60}{Colors.END}")
    
    def code_generator(self):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}💡 AI Code Generator - Powered by AI{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
        
        print(f"{Colors.CYAN}Programming Language:{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Python")
        print(f"{Colors.GREEN}[2]{Colors.END} JavaScript")
        print(f"{Colors.GREEN}[3]{Colors.END} Bash/Shell")
        print(f"{Colors.GREEN}[4]{Colors.END} PHP")
        print(f"{Colors.GREEN}[5]{Colors.END} Java")
        print(f"{Colors.GREEN}[6]{Colors.END} C++")
        
        lang_choice = input(f"\n{Colors.YELLOW}Language [1]:{Colors.END} ").strip() or "1"
        
        lang_map = {
            "1": ("python", "py"),
            "2": ("javascript", "js"),
            "3": ("bash", "sh"),
            "4": ("php", "php"),
            "5": ("java", "java"),
            "6": ("cpp", "cpp")
        }
        
        lang_name, ext = lang_map.get(lang_choice, ("python", "py"))
        
        description = input(f"\n{Colors.YELLOW}Describe what code you need:{Colors.END} ").strip()
        
        if not description:
            print(f"{Colors.RED}[✗] Empty description!{Colors.END}")
            return
        
        print(f"\n{Colors.BLUE}[*]{Colors.END} Generating {Colors.GREEN}{lang_name.upper()}{Colors.END} code with AI...")
        print(f"{Colors.BLUE}[*]{Colors.END} This may take a moment...\n")
        
        prompt = f"""Write a complete, functional, production-ready {lang_name} code for: {description}

Requirements:
- Complete working code, not pseudocode
- Include all necessary imports and dependencies
- Add error handling
- Include comments explaining key parts
- Follow best practices for {lang_name}
- Make it ready to run immediately

Generate ONLY the code, no explanations before or after."""
        
        try:
            apis = [
                {
                    "url": "https://api.blackbox.ai/api/chat",
                    "method": "post",
                    "data": {
                        "messages": [{"role": "user", "content": prompt}],
                        "previewToken": None,
                        "codeModelMode": True,
                        "agentMode": {},
                        "trendingAgentMode": {},
                        "isMicMode": False
                    }
                }
            ]
            
            code = None
            
            for api in apis:
                try:
                    if api["method"] == "post":
                        response = requests.post(api["url"], json=api["data"], timeout=30)
                    else:
                        response = requests.get(api["url"], timeout=30)
                    
                    if response.status_code == 200:
                        result = response.text
                        
                        if result and len(result) > 50:
                            code = result
                            
                            if '```' in code:
                                parts = code.split('```')
                                for part in parts:
                                    if lang_name in part.lower() or ext in part.lower():
                                        code = part.split('\n', 1)[1] if '\n' in part else part
                                        break
                                else:
                                    if len(parts) > 1:
                                        code = parts[1].split('\n', 1)[1] if '\n' in parts[1] else parts[1]
                            
                            code = code.strip()
                            break
                            
                except:
                    continue
            
            if not code or len(code) < 50:
                print(f"{Colors.YELLOW}[!]{Colors.END} AI service unavailable. Using enhanced template...\n")
                
                templates = {
                    "python": f'''#!/usr/bin/env python3
"""
{description}
Generated by AK AI Tool
"""

import sys
import os
import json
import requests
from pathlib import Path

class {description.replace(' ', '')}:
    def __init__(self):
        """Initialize the tool"""
        self.setup()
    
    def setup(self):
        """Setup configuration"""
        print("[*] Initializing {description}...")
    
    def run(self):
        """Main execution"""
        try:
            print("[*] Starting execution...")
            
            # TODO: Implement {description}
            # Add your main logic here
            
            print("[✓] Execution completed successfully!")
            
        except Exception as e:
            print(f"[✗] Error: {{e}}")
            return False
        
        return True

def main():
    """Entry point"""
    tool = {description.replace(' ', '')}()
    success = tool.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
''',
                    "javascript": f'''/**
 * {description}
 * Generated by AK AI Tool
 */

const axios = require('axios');
const fs = require('fs');

class {description.replace(' ', '')} {{
    constructor() {{
        this.init();
    }}
    
    init() {{
        console.log('[*] Initializing {description}...');
    }}
    
    async run() {{
        try {{
            console.log('[*] Starting execution...');
            
            // TODO: Implement {description}
            // Add your main logic here
            
            console.log('[✓] Execution completed!');
            return true;
            
        }} catch (error) {{
            console.error('[✗] Error:', error);
            return false;
        }}
    }}
}}

async function main() {{
    const tool = new {description.replace(' ', '')}();
    const success = await tool.run();
    process.exit(success ? 0 : 1);
}}

main();
''',
                    "bash": f'''#!/bin/bash
# {description}
# Generated by AK AI Tool

set -e

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

log_info() {{
    echo -e "${{YELLOW}}[*]${{NC}} $1"
}}

log_success() {{
    echo -e "${{GREEN}}[✓]${{NC}} $1"
}}

log_error() {{
    echo -e "${{RED}}[✗]${{NC}} $1"
}}

main() {{
    log_info "Starting {description}..."
    
    # TODO: Implement {description}
    # Add your main logic here
    
    log_success "Execution completed!"
}}

main "$@"
''',
                    "php": f'''<?php
/**
 * {description}
 * Generated by AK AI Tool
 */

class {description.replace(' ', '')} {{
    
    public function __construct() {{
        $this->init();
    }}
    
    private function init() {{
        echo "[*] Initializing {description}...\\n";
    }}
    
    public function run() {{
        try {{
            echo "[*] Starting execution...\\n";
            
            // TODO: Implement {description}
            // Add your main logic here
            
            echo "[✓] Execution completed!\\n";
            return true;
            
        }} catch (Exception $e) {{
            echo "[✗] Error: " . $e->getMessage() . "\\n";
            return false;
        }}
    }}
}}

function main() {{
    $tool = new {description.replace(' ', '')}();
    $success = $tool->run();
    exit($success ? 0 : 1);
}}

main();
?>
'''
                }
                
                code = templates.get(lang_name, templates["python"])
            
            print(f"{Colors.GREEN}{'─'*60}{Colors.END}")
            print(f"{Colors.CYAN}{code}{Colors.END}")
            print(f"{Colors.GREEN}{'─'*60}{Colors.END}\n")
            
            save = input(f"{Colors.YELLOW}Save code? (y/n):{Colors.END} ").strip().lower()
            if save == 'y':
                filename = input(f"{Colors.YELLOW}Filename [code.{ext}]:{Colors.END} ").strip() or f"code.{ext}"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                if ext in ['py', 'sh']:
                    os.chmod(filename, 0o755)
                    print(f"{Colors.GREEN}[✓]{Colors.END} Saved and made executable: {Colors.BOLD}{filename}{Colors.END}")
                else:
                    print(f"{Colors.GREEN}[✓]{Colors.END} Saved: {Colors.BOLD}{filename}{Colors.END}")
                
        except Exception as e:
            print(f"{Colors.RED}[✗]{Colors.END} Error: {str(e)}")
    
    def text_to_speech(self):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}🔊 AI Text to Speech{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
        
        text = input(f"{Colors.YELLOW}Text:{Colors.END} ").strip()
        if not text:
            return
        
        print(f"\n{Colors.CYAN}Language:{Colors.END} [1] English  [2] Arabic  [3] Spanish")
        lang_choice = input(f"{Colors.YELLOW}Choose [1]:{Colors.END} ").strip() or "1"
        
        lang_map = {"1": "en", "2": "ar", "3": "es"}
        lang = lang_map.get(lang_choice, "en")
        
        output = input(f"{Colors.YELLOW}Output [speech.mp3]:{Colors.END} ").strip() or "speech.mp3"
        
        print(f"\n{Colors.BLUE}[*]{Colors.END} Generating...")
        
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=lang)
            tts.save(output)
            print(f"{Colors.GREEN}[✓]{Colors.END} Saved: {output}")
        except ImportError:
            print(f"{Colors.RED}[✗]{Colors.END} Install: pip install gtts")
        except Exception as e:
            print(f"{Colors.RED}[✗]{Colors.END} Error: {str(e)}")
    
    def image_editor(self):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}🖼️  Image Enhancer (Local Processing){Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
        
        img_path = input(f"{Colors.YELLOW}Image path:{Colors.END} ").strip()
        if not os.path.exists(img_path):
            print(f"{Colors.RED}[✗]{Colors.END} File not found")
            return
        
        print(f"\n{Colors.CYAN}Enhancement Options:{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Sharpen")
        print(f"{Colors.GREEN}[2]{Colors.END} Increase Brightness")
        print(f"{Colors.GREEN}[3]{Colors.END} Increase Contrast")
        print(f"{Colors.GREEN}[4]{Colors.END} Auto Enhance (all)")
        
        choice = input(f"\n{Colors.YELLOW}Choose [4]:{Colors.END} ").strip() or "4"
        output = input(f"{Colors.YELLOW}Output [enhanced.jpg]:{Colors.END} ").strip() or "enhanced.jpg"
        
        if not output.endswith(('.jpg', '.png')):
            output += '.jpg'
        
        print(f"\n{Colors.BLUE}[*]{Colors.END} Processing...")
        
        try:
            from PIL import Image, ImageEnhance, ImageFilter
            
            img = Image.open(img_path)
            
            if choice == "1":
                img = img.filter(ImageFilter.SHARPEN)
                img = img.filter(ImageFilter.SHARPEN)  # Apply twice
                print(f"{Colors.GREEN}[✓]{Colors.END} Sharpened")
                
            elif choice == "2":
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.2)
                print(f"{Colors.GREEN}[✓]{Colors.END} Brightness increased")
                
            elif choice == "3":
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.3)
                print(f"{Colors.GREEN}[✓]{Colors.END} Contrast increased")
                
            else:  # Auto enhance
                # Sharpen
                img = img.filter(ImageFilter.SHARPEN)
                # Enhance color
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.2)
                # Enhance contrast
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.1)
                # Enhance sharpness
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.3)
                print(f"{Colors.GREEN}[✓]{Colors.END} Auto enhanced")
            
            img.save(output, quality=95)
            
            orig_size = os.path.getsize(img_path) / 1024
            new_size = os.path.getsize(output) / 1024
            
            print(f"{Colors.GREEN}[✓]{Colors.END} Saved: {Colors.BOLD}{os.path.abspath(output)}{Colors.END}")
            print(f"{Colors.CYAN}[i]{Colors.END} Original: {orig_size:.1f} KB → Enhanced: {new_size:.1f} KB")
            
        except ImportError:
            print(f"{Colors.RED}[✗]{Colors.END} Pillow not installed")
            print(f"{Colors.YELLOW}[!]{Colors.END} Install: pip install pillow")
        except Exception as e:
            print(f"{Colors.RED}[✗]{Colors.END} Error: {str(e)}")
    
    def run(self):
        while True:
            os.system('clear' if os.name != 'nt' else 'cls')
            self.banner()
            self.menu()
            
            try:
                choice = input(f"{Colors.YELLOW}➤ Choice:{Colors.END} ").strip()
                
                if choice == '0':
                    print(f"\n{Colors.CYAN}Thanks for using AK AI Tool! 👋{Colors.END}\n")
                    break
                elif choice == '1':
                    self.image_generator()
                elif choice == '2':
                    self.translator()
                elif choice == '3':
                    self.email_writer()
                elif choice == '4':
                    self.code_generator()
                elif choice == '5':
                    self.text_to_speech()
                elif choice == '6':
                    self.image_editor()
                else:
                    print(f"\n{Colors.RED}[✗] Invalid!{Colors.END}")
                
                input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
                
            except KeyboardInterrupt:
                print(f"\n\n{Colors.CYAN}Goodbye! 👋{Colors.END}\n")
                break
            except Exception as e:
                print(f"\n{Colors.RED}[✗] {str(e)}{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")

if __name__ == "__main__":
    AKAI().run()
