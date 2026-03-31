import json
import datetime
import subprocess
import sys

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stderr)
        sys.exit(1)

# Read data
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("data.json not found.")
    sys.exit(1)

# Generate HTML
html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cockpit de Pilotage Financier - Vision Empire 2027</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; line-height: 1.6;}}
        .container {{max-width: 900px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);}}
        h1, h2, h3 {{color: #FF8C00; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 20px;}}
        .objectif {{background-color: #FFF3E0; border-left: 5px solid #FFA500; padding: 15px; margin-bottom: 20px; font-size: 1.1em; font-weight: bold;}}
        .section-header {{display: flex; justify-content: space-between; align-items: center; margin-top: 20px;}}
        .details-button {{background-color: #FFA500; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; font-size: 0.9em; transition: background-color 0.3s ease;}}
        .details-button:hover {{background-color: #FF8C00;}}
        .details-content {{border: 1px solid #ddd; padding: 15px; margin-top: 10px; border-radius: 5px; background-color: #f9f9f9; display: none;}}
        .progress-bar-container {{width: 100%; background-color: #e0e0e0; border-radius: 5px; margin-top: 10px; overflow: hidden;}}
        .progress-bar {{height: 20px; background-color: #FFA500; text-align: center; line-height: 20px; color: white; font-size: 0.8em; border-radius: 5px; transition: width 0.5s ease-in-out;}}
        .projet, .idee-labo {{background-color: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 5px;}}
        .projet h3, .idee-labo h3 {{margin-top: 0; color: #FF8C00;}}
        .footer {{margin-top: 40px; border-top: 1px solid #eee; padding-top: 15px; text-align: center; font-size: 0.8em; color: #888;}}
    </style>
</head>
<body>
    <div class="container">
        <h1>Cockpit de Pilotage Financier - Vision Empire 2027</h1>
        <div class="objectif">
            <h2>Objectif Final :</h2>
            <p>{data.get('objective', '')}</p>
        </div>
        <div class="section-header">
            <h2>🟢 ZONE PROJETS ACTIFS</h2>
        </div>
        <div id="projetsActifs">
"""

for p in data.get('projects', []):
    html += f"""
            <div class="projet">
                <h3>{p['title']}</h3>
                <p>Action : {p['action']}</p>
                <p>Tâche : {p['task']}</p>
                <div class="progress-bar-container"><div class="progress-bar" style="width: {p['progress']}%;">{p['progress']}%</div></div>
                <button class="details-button" onclick="toggleDetails('{p['id']}')">Piloter</button>
                <div id="{p['id']}" class="details-content">
                    <p>Détails techniques : {p['details']}</p>
                    <h4>Choix disponibles :</h4>
                    <ul>
"""
    for opt in p.get('options', []):
        html += f"                        <li>**{opt['title']}**<ul>"
        html += f"<li>Coût : {opt['cost']}</li>"
        html += f"<li>ROI estimé : {opt['roi']}</li>"
        html += f"<li>Alternative gratuite : {opt['alternative']}</li>"
        html += f"<li>Action requise de Michel : {opt['action']}</li></ul></li>\n"
    html += """                    </ul>
                </div>
            </div>
"""

um = data.get('urgentMission')
if um:
    html += f"""
             <div class="projet">
                <h3>{um['title']}</h3>
                <p>Action : {um['action']}</p>
                <p>Tâche : {um['task']}</p>
                <div class="progress-bar-container"><div class="progress-bar" style="width: {um['progress']}%;">{um['progress']}%</div></div>
                <a href="{um['link']}" class="details-button">{um['linkText']}</a>
            </div>
"""

html += """
        </div>
        <div class="section-header">
            <h2>🧪 ZONE LABORATOIRE D'IDÉES</h2>
        </div>
        <div id="laboratoireIdees">
"""

for lab in data.get('labIdeas', []):
    html += f"""
            <div class="idee-labo">
                <h3>{lab['title']}</h3>
                <p>Score Potentiel : {lab['score']}</p>
                <button class="details-button" onclick="toggleDetails('{lab['id']}')">Creuser</button>
                <div id="{lab['id']}" class="details-content">
                    <p>Détails techniques : {lab['details']}</p>
                    <p>Analyse :</p>
                    <ul>
"""
    for a in lab.get('analysis', []):
        html += f"                        <li>{a}</li>\n"
    
    html += f"""                    </ul>
                    <p>Action requise de Michel : {lab['action']}</p>
                </div>
            </div>
"""

now = datetime.datetime.now(datetime.timezone.utc)
time_str = now.strftime('%Y-%m-%d à %H:%M:%S UTC')

html += f"""
        </div>
    </div>
    <div class="footer">
        <p>Dernière mise à jour par Pétole : <span id="lastUpdated">{time_str}</span></p>
    </div>
    <script>
        function toggleDetails(id) {{
            const element = document.getElementById(id);
            if (element.style.display === "none" || element.style.display === "") {{
                element.style.display = "block";
            }} else {{
                element.style.display = "none";
            }}
        }}
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated index.html")

# Git operations
run_command("git add data.json update_site.py index.html")
run_command('git commit -m "Automated update via script"')
run_command('git push origin main')
print("Pushed to GitHub")
