import os
import re

# Настройки
M7 = "M7_18_Baza.osim"
M8 = "M8_Caruthers_FullBodyModel2016_Scaled_Arms_Corrected.osim"
REPORT = "analysis_report.txt"

def get_structure(filename):
    if not os.path.exists(filename):
        return f"FILE {filename} NOT FOUND!"
    
    with open(filename, 'r') as f:
        content = f.read()
    
    bodies = re.findall(r'<Body\s+name="([^"]+)"', content)
    joints = re.findall(r'<(\w+)Joint\s+name="([^"]+)"', content)
    
    # Поиск родителей для ключевых костей
    hierarchy = {}
    for body in bodies:
        # Ищем блок тела и внутри него parent_body
        pattern = r'<Body\s+name="' + re.escape(body) + r'".*?<parent_body>([^<]+)</parent_body>'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            hierarchy[body] = match.group(1)
            
    return bodies, joints, hierarchy

def main():
    print("Starting Analysis...")
    
    with open(REPORT, 'w') as rep:
        rep.write("=== OPENSIM MODEL ANALYSIS REPORT ===\n\n")
        
        # Анализ M7
        rep.write(f"--- MODEL: {M7} ---\n")
        if os.path.exists(M7):
            b7, j7, h7 = get_structure(M7)
            rep.write(f"Bodies count: {len(b7)}\n")
            rep.write(f"Joints count: {len(j7)}\n")
            rep.write("Key Hierarchy:\n")
            for key in ['pelvis', 'sacrum', 'lumbar5', 'lumbar4']:
                if key in h7:
                    rep.write(f"  {key} -> Parent: {h7[key]}\n")
        else:
            rep.write("FILE MISSING\n")
            
        rep.write("\n")
        
        # Анализ M8
        rep.write(f"--- MODEL: {M8} ---\n")
        if os.path.exists(M8):
            b8, j8, h8 = get_structure(M8)
            rep.write(f"Bodies count: {len(b8)}\n")
            rep.write(f"Joints count: {len(j8)}\n")
            rep.write("Key Hierarchy:\n")
            for key in ['pelvis', 'sacrum', 'lumbar5', 'lumbar4']:
                if key in h8:
                    rep.write(f"  {key} -> Parent: {h8[key]}\n")
        else:
            rep.write("FILE MISSING\n")
            
        rep.write("\n--- DOCUMENTATION CHECK ---\n")
        if os.path.exists("docs"):
            files = os.listdir("docs")
            rep.write(f"Docs folder found. Files: {len(files)}\n")
        else:
            rep.write("Docs folder NOT found.\n")

    print(f"Report saved to {REPORT}")

if __name__ == "__main__":
    main()
