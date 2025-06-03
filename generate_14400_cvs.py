# Étape 1 : Installer les dépendances
#pip install faker reportlab python-docx pandas googletrans==3.1.0a0

# Étape 2 : Importer les bibliothèques
import random
import os
import zipfile
import uuid
import pandas as pd
from faker import Faker
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Étape 3 : Initialiser Faker pour différentes langues
fake_fr = Faker('fr_FR')
fake_en = Faker('en_US')
fake_ru = Faker('ru_RU')
fake_it = Faker('it_IT')

# Initialiser le traducteur
translator = Translator()

# Listes de prénoms et noms djiboutiens
djiboutian_first_names = [
    # Masculins
    "Ahmed", "Hassan", "Mahad", "Ismail", "Abdourahman", "Ali", "Ibrahim", "Abdi", "Youssouf", "Souleiman",
    "Jamal", "Zakaria", "Mohamed", "Farhan", "Idriss", "Faysal", "Yassin", "Bilal", "Omar", "Abdallah",
    "Barkhad", "Anwar", "Saïd", "Nour", "Dini", "Mahamoud", "Khaled", "Awaleh", "Bileh", "Muse",
    "Saad", "Salah", "Warsame", "Guedi", "Walid", "Abdirahman", "Haroun", "Moustapha", "Abshir",
    "Suleyman", "Dawoud", "Houssein", "Abokor", "Aweis", "Hersi", "Aaden", "Ayub", "Farah", "Ayman",
    "Rachid", "Madar", "Nuradin", "Hassanali", "Kalif", "Deria", "Saidou", "Samatar", "Tahlil",
    "Wais", "Darar", "Robleh", "Barre", "Aliyow", "Djamal", "Sharmarke", "Kamil", "Mahdi", "Gedi",
    "Duale", "Barkat",
    # Féminins
    "Fadumo", "Ayan", "Hibo", "Ifrah", "Nimo", "Hawa", "Sagal", "Asha", "Safia", "Hodan",
    "Zamzam", "Amal", "Faiza", "Rahma", "Amina", "Khadija", "Naima", "Yasmin", "Salma", "Ikram",
    "Roda", "Halima", "Saida", "Habiba", "Mariam", "Fatouma", "Asli", "Souad", "Batula", "Anisa",
    "Hani", "Deeqa", "Shaafi", "Sahra", "Rihana", "Munira", "Bilan", "Layla", "Nadra", "Muna",
    "Mako", "Sucaad", "Faisa", "Anab", "Haniyo", "Sulekha", "Fawzia", "Farhia", "Ifra", "Sudi",
    "Lubna", "Bashira", "Nura", "Zamzama", "Zaynab", "Deka", "Ikran", "Saynab", "Jawahir",
    "Farhiyo", "Ubah", "Shukri", "Ismahan", "Barwaqo", "Rukia", "Misra", "Nasteexo", "Samia",
    "Asma", "Rahimo"
]
djiboutian_last_names = [
    "Abdi Farah", "Ali Robleh", "Hassan Dini", "Youssouf Omar", "Mohamed Farhan", "Ismail Awaleh",
    "Ahmed Gedi", "Ibrahim Duale", "Mahad Saïd", "Abdirahman Muse", "Farhan Mahamoud", "Guedi Warsame",
    "Omar Abdi", "Abdourahman Walid", "Khaled Awaleh", "Abshir Robleh", "Suleyman Barre",
    "Djamal Samatar", "Robleh Tahlil", "Barkhad Robleh", "Souleiman Abdi", "Saïd Deria",
    "Warsame Madar", "Nour Hassan", "Mahdi Robleh", "Dawoud Robleh", "Abokor Wais", "Deria Saïd",
    "Saad Abdi", "Houssein Hassan", "Moustapha Abdi", "Walid Barkhad", "Aliyow Djamal",
    "Abdi Sharmarke", "Salah Djamal", "Ayub Farah", "Rachid Madar", "Mahamoud Saidou",
    "Awaleh Barkat", "Yassin Madar", "Abdi Barre", "Barkat Kalif", "Madar Guedi", "Jamal Sharmarke",
    "Bilal Saïd", "Robleh Wais", "Barre Awaleh", "Khalif Warsame", "Farah Hersi", "Abdallah Madar",
    "Hersi Samatar", "Nouradin Tahlil", "Saidou Hassan", "Kalif Dawoud", "Walid Saidou",
    "Djamal Barkat", "Barkat Awaleh", "Faysal Barre", "Samatar Guedi", "Deria Hersi",
    "Aweis Tahlil", "Robleh Barkhad", "Awaleh Saidou", "Ali Tahlil", "Abdirahman Barkhad",
    "Madar Warsame", "Ismail Deria", "Omar Abdi", "Jamal Saidou", "Saïd Abshir", "Ali Robleh",
    "Youssouf Madar", "Barkhad Muse", "Tahlil Warsame", "Barkat Duale", "Awaleh Guedi",
    "Samatar Mahdi", "Walid Nour", "Muse Saïd", "Saidou Barkat", "Mahamoud Djamal",
    "Sharmarke Warsame", "Deria Robleh", "Guedi Awaleh", "Hassan Kalif"
]

# Noms étrangers spécifiques par nationalité
foreign_first_names = {
    "French": ["Lucas", "Hugo", "Enzo", "Arthur", "Léo", "Nathan", "Raphaël", "Jules", "Tom", "Clément",
               "Louis", "Adam", "Noé", "Théo", "Maxime"],
    "English": ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles", "Joseph",
                "Thomas", "Daniel", "Matthew", "Andrew", "Kevin", "Brian"],
    "Russian": ["Ivan", "Dimitri", "Alexei", "Nikolai", "Mikhail", "Vladimir", "Yuri", "Andrei", "Sergei",
                "Pavel"],
    "Italian": ["Luca", "Matteo", "Marco", "Andrea", "Alessandro", "Gabriele", "Giovanni", "Antonio",
                "Stefano", "Francesco"],
    "Ethiopian": ["Bekele", "Tadesse", "Tesfaye", "Abebe", "Dawit", "Getachew", "Hailu", "Kassahun",
                  "Solomon", "Yosef"],
    "Other": ["Ali", "Omar", "Amir", "Malik", "Ibrahim", "Hamza", "Sami", "Elias", "Youssef", "Karim"]
}
foreign_last_names = [
    "Dubois", "Lefèvre", "Bernard", "Girard", "Morel",
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Petrov", "Sokolov", "Kuznetsov", "Ivanov", "Makarov",
    "Rossi", "Bianchi", "Romano", "Conti", "Gallo",
    "Teshome", "Gebre", "Mekonnen", "Alemu", "Desta",
    "El Fassi", "Ben Omar", "Diouf", "Bamba", "Haddad"
]

# Liste des 200 métiers
jobs = [
    "Enseignant", "Médecin", "Ingénieur informatique", "Infirmier", "Commerçant", "Comptable", "Avocat",
    "Chauffeur", "Électricien", "Pharmacien", "Journaliste", "Développeur web", "Cuisinier", "Secrétaire",
    "Logisticien", "Pêcheur", "Agriculteur", "Architecte", "Dentiste", "Vétérinaire", "Banquier", "Marketeur",
    "Plombier", "Mécanicien", "Coiffeur", "Tailleur", "Boulanger", "Pâtissier", "Serveur", "Barman",
    "Agent immobilier", "Agent de sécurité", "Policier", "Pompier", "Militaire", "Technicien de maintenance",
    "Analyste financier", "Consultant", "Graphiste", "Photographe", "Vidéaste", "Monteur vidéo", "Rédacteur",
    "Traducteur", "Interprète", "Bibliothécaire", "Archiviste", "Conservateur de musée", "Guide touristique",
    "Agent de voyage", "Pilote", "Hôtesse de l'air", "Contrôleur aérien", "Marin", "Capitaine de navire",
    "Paysagiste", "Jardinier", "Fleuriste", "Écologiste", "Biologiste", "Chimiste", "Physicien", "Mathématicien",
    "Statisticien", "Data scientist", "Data analyst", "Ingénieur civil", "Ingénieur mécanique", "Ingénieur électrique",
    "Urbaniste", "Géologue", "Météorologue", "Océanographe", "Astronome", "Psychologue", "Psychiatre",
    "Travailleur social", "Conseiller d'orientation", "Coach", "Formateur", "Animateur", "Éducateur spécialisé",
    "Orthophoniste", "Kinésithérapeute", "Ergothérapeute", "Opticien", "Audioprothésiste", "Sage-femme",
    "Aide-soignant", "Ambulancier", "Laborantin", "Chercheur", "Professeur d'université", "Assistant de recherche",
    "Économiste", "Sociologue", "Anthropologue", "Historien", "Géographe", "Politicien", "Diplomate",
    "Agent des douanes", "Inspecteur fiscal", "Auditeur", "Actuaire", "Assureur", "Courtier", "Notaire"
    # Removed the rest of the jobs to keep only the first 100
]

# Compétences spécifiques par métier (5 à 15 par métier)
job_skills = {
    "Enseignant": ["Pédagogie", "Gestion de classe", "Planification de cours", "Évaluation des élèves", "Technologies éducatives", "Communication", "Adaptabilité", "Créativité", "Travail d'équipe", "Motivation des élèves"],
    "Médecin": ["Diagnostic médical", "Soins aux patients", "Pharmacologie", "Chirurgie", "Gestion des urgences", "Empathie", "Analyse de dossiers médicaux", "Communication patient", "Éthique médicale", "Mise à jour des connaissances"],
    "Ingénieur informatique": ["Programmation", "Résolution de problèmes", "Conception de systèmes", "Gestion de bases de données", "Cybersécurité", "Cloud computing", "DevOps", "Analyse des besoins", "Test de logiciels", "Maintenance système", "Python", "Java", "Agilité"],
    "Infirmier": ["Soins infirmiers", "Administration de médicaments", "Surveillance des patients", "Premiers secours", "Gestion des dossiers médicaux", "Empathie", "Communication", "Travail sous pression", "Hygiène hospitalière", "Collaboration médicale"],
    "Commerçant": ["Négociation", "Gestion des stocks", "Service client", "Vente", "Marketing", "Comptabilité de base", "Analyse de marché", "Fidélisation client", "Gestion du temps", "Résolution de conflits"],
    "Comptable": ["Comptabilité générale", "Analyse financière", "Fiscalité", "Logiciels comptables", "Budgétisation", "Audit", "Reporting", "Gestion de la paie", "Conformité réglementaire", "Excel avancé"],
    "Avocat": ["Droit", "Plaidoyer", "Rédaction juridique", "Négociation", "Recherche juridique", "Éthique professionnelle", "Gestion de dossiers", "Communication client", "Résolution de litiges", "Connaissance des lois"],
    "Chauffeur": ["Conduite sécuritaire", "Navigation GPS", "Entretien du véhicule", "Respect des horaires", "Service client", "Connaissance des routes", "Gestion du stress", "Premiers secours", "Règles de circulation"],
    "Électricien": ["Installation électrique", "Dépannage", "Lecture de schémas", "Normes de sécurité", "Maintenance", "Câblage", "Test de circuits", "Utilisation d'outils électriques", "Connaissance des normes"],
    "Pharmacien": ["Pharmacologie", "Dispensation de médicaments", "Conseil aux patients", "Gestion des stocks", "Réglementation pharmaceutique", "Communication", "Analyse des prescriptions", "Vigilance médicamenteuse"],
    "Journaliste": ["Rédaction", "Recherche d'informations", "Interview", "Éthique journalistique", "Montage vidéo", "Réseaux sociaux", "Analyse de données", "Communication", "Photographie"],
    "Développeur web": ["HTML/CSS", "JavaScript", "Frameworks (React, Angular)", "Backend (Node.js, Django)", "Bases de données", "SEO", "Tests unitaires", "Git", "UX/UI", "Responsive design"],
    "Cuisinier": ["Cuisine", "Gestion des ingrédients", "Hygiène alimentaire", "Créativité culinaire", "Gestion du temps", "Service client", "Menu planning", "Techniques de cuisson"],
    "Secrétaire": ["Gestion d'agenda", "Rédaction de courriers", "Accueil", "Organisation", "Informatique (Office)", "Communication", "Classement", "Prise de notes"],
    "Logisticien": ["Gestion de la chaîne d'approvisionnement", "Planification logistique", "Gestion des stocks", "Transport", "Négociation avec fournisseurs", "Analyse des coûts", "ERP", "Coordination"],
    "Pêcheur": ["Pêche artisanale", "Navigation maritime", "Entretien des filets", "Connaissance des espèces", "Sécurité en mer", "Réparation de bateaux", "Gestion des captures", "Météorologie"],
    "Agriculteur": ["Culture agricole", "Gestion des sols", "Irrigation", "Récolte", "Utilisation de machines agricoles", "Connaissance des semences", "Protection des cultures", "Comptabilité agricole"],
    "Architecte": ["Conception architecturale", "CAO (AutoCAD)", "Gestion de projets", "Normes de construction", "Urbanisme", "Rendu 3D", "Communication client", "Budgétisation", "Durabilité"],
    "Dentiste": ["Soins dentaires", "Chirurgie dentaire", "Diagnostic oral", "Radiologie dentaire", "Prothèses", "Hygiène buccale", "Communication patient", "Gestion de cabinet"],
    "Vétérinaire": ["Soins animaux", "Chirurgie vétérinaire", "Diagnostic", "Pharmacologie vétérinaire", "Communication client", "Gestion de clinique", "Bien-être animal"],
    "Banquier": ["Gestion de comptes", "Analyse de crédit", "Conseil financier", "Conformité réglementaire", "Vente de produits bancaires", "Communication client", "Analyse de risques"],
    "Marketeur": ["Stratégie marketing", "Analyse de marché", "Publicité", "Réseaux sociaux", "SEO/SEM", "Gestion de campagnes", "Communication", "Créativité"],
    "Plombier": ["Installation sanitaire", "Réparation de fuites", "Lecture de plans", "Soudure", "Maintenance", "Normes de sécurité", "Service client"],
    "Mécanicien": ["Réparation de véhicules", "Diagnostic mécanique", "Entretien", "Utilisation d'outils", "Connaissance des moteurs", "Normes de sécurité", "Service client"],
    "Coiffeur": ["Coupe de cheveux", "Coloration", "Coiffure", "Conseil client", "Hygiène", "Gestion du salon", "Créativité"],
    "Tailleur": ["Couture", "Prise de mesures", "Conception de vêtements", "Réparation", "Conseil client", "Gestion des tissus", "Précision"],
    "Boulanger": ["Pétrissage", "Cuisson", "Gestion des ingrédients", "Hygiène alimentaire", "Créativité", "Service client", "Gestion du temps"],
    "Pâtissier": ["Pâtisserie", "Décoration", "Gestion des ingrédients", "Hygiène alimentaire", "Créativité", "Précision", "Service client"],
    "Serveur": ["Service client", "Prise de commandes", "Gestion du temps", "Communication", "Hygiène", "Travail d'équipe", "Résolution de problèmes"],
    "Barman": ["Mixologie", "Service client", "Gestion des stocks", "Hygiène", "Communication", "Créativité", "Travail sous pression"],
    "Agent immobilier": ["Négociation", "Évaluation immobilière", "Vente", "Conseil client", "Connaissance du marché", "Rédaction de contrats", "Communication"],
    "Agent de sécurité": ["Surveillance", "Gestion des conflits", "Premiers secours", "Connaissance des lois", "Communication", "Vigilance", "Rapport"],
    "Policier": ["Application de la loi", "Investigation", "Sécurité publique", "Communication", "Premiers secours", "Gestion des conflits", "Éthique"],
    "Pompier": ["Extinction d'incendies", "Sauvetage", "Premiers secours", "Maintenance d'équipements", "Travail d'équipe", "Gestion du stress"],
    "Militaire": ["Stratégie", "Combat", "Discipline", "Premiers secours", "Communication", "Physique", "Maintenance d'équipements"],
    "Technicien de maintenance": ["Dépannage", "Maintenance préventive", "Lecture de schémas", "Utilisation d'outils", "Normes de sécurité", "Rapport"],
    "Analyste financier": ["Analyse de données", "Modélisation financière", "Évaluation des risques", "Excel avancé", "Rapport", "Connaissance des marchés"],
    "Consultant": ["Analyse de problèmes", "Conseil stratégique", "Communication client", "Gestion de projets", "Recherche", "Présentation"],
    "Graphiste": ["Conception graphique", "Photoshop", "Illustrator", "Créativité", "Communication client", "Gestion de projets"],
    "Photographe": ["Photographie", "Retouche d'images", "Éclairage", "Créativité", "Communication client", "Gestion d'équipements"],
    "Vidéaste": ["Tournage", "Montage vidéo", "Éclairage", "Son", "Créativité", "Logiciels de montage"],
    "Monteur vidéo": ["Montage", "Effets spéciaux", "Synchronisation audio", "Logiciels (Premiere, Final Cut)", "Créativité"],
    "Rédacteur": ["Rédaction", "Recherche", "SEO", "Correction", "Communication", "Créativité"],
    "Traducteur": ["Traduction", "Connaissance linguistique", "Recherche terminologique", "Précision", "Gestion du temps"],
    "Interprète": ["Interprétation simultanée", "Connaissance linguistique", "Communication", "Écoute active", "Gestion du stress"],
    "Bibliothécaire": ["Gestion de collections", "Recherche documentaire", "Service client", "Informatique", "Organisation"],
    "Archiviste": ["Gestion d'archives", "Numérisation", "Recherche", "Organisation", "Connaissance historique"],
    "Conservateur de musée": ["Gestion de collections", "Conservation", "Recherche", "Organisation d'expositions", "Communication"],
    "Guide touristique": ["Connaissance culturelle", "Communication", "Organisation", "Multilinguisme", "Service client"],
    "Agent de voyage": ["Planification de voyages", "Réservations", "Conseil client", "Connaissance des destinations", "Communication"],
    "Pilote": ["Pilotage", "Navigation", "Sécurité aérienne", "Communication", "Gestion du stress", "Maintenance"],
    "Hôtesse de l'air": ["Service client", "Sécurité aérienne", "Premiers secours", "Communication", "Multilinguisme"],
    "Contrôleur aérien": ["Gestion du trafic aérien", "Communication", "Prise de décision", "Gestion du stress", "Connaissance des protocoles"],
    "Marin": ["Navigation", "Maintenance de navires", "Sécurité maritime", "Communication", "Travail d'équipe"],
    "Capitaine de navire": ["Commandement", "Navigation", "Sécurité maritime", "Gestion d'équipe", "Maintenance"],
    "Paysagiste": ["Conception de jardins", "Entretien paysager", "Connaissance des plantes", "CAO", "Communication client"],
    "Jardinier": ["Entretien des plantes", "Taille", "Irrigation", "Connaissance des sols", "Utilisation d'outils"],
    "Fleuriste": ["Composition florale", "Connaissance des fleurs", "Service client", "Créativité", "Gestion des stocks"],
    "Écologiste": ["Recherche environnementale", "Analyse de données", "Conservation", "Communication", "Sensibilisation"],
    "Biologiste": ["Recherche scientifique", "Analyse de données", "Expérimentation", "Rédaction scientifique", "Connaissance biologique"],
    "Chimiste": ["Analyse chimique", "Synthèse", "Expérimentation", "Sécurité en laboratoire", "Rédaction scientifique"],
    "Physicien": ["Recherche scientifique", "Modélisation", "Expérimentation", "Analyse de données", "Mathématiques"],
    "Mathématicien": ["Modélisation", "Analyse", "Résolution de problèmes", "Programmation", "Enseignement"],
    "Statisticien": ["Analyse de données", "Modélisation statistique", "Logiciels (R, SPSS)", "Rapport", "Interprétation"],
    "Data scientist": ["Machine learning", "Analyse de données", "Programmation (Python, R)", "Visualisation", "Statistiques"],
    "Data analyst": ["Analyse de données", "Visualisation", "SQL", "Excel", "Rapport"],
    "Ingénieur civil": ["Conception de structures", "Gestion de projets", "CAO", "Normes de construction", "Budgétisation"],
    "Ingénieur mécanique": ["Conception mécanique", "CAO", "Tests", "Maintenance", "Gestion de projets"],
    "Ingénieur électrique": ["Conception de circuits", "Maintenance", "Normes de sécurité", "CAO", "Gestion de projets"],
    "Urbaniste": ["Planification urbaine", "Analyse spatiale", "Consultation publique", "SIG", "Réglementation"],
    "Géologue": ["Analyse des sols", "Cartographie", "Recherche", "Évaluation des risques", "Rapport"],
    "Météorologue": ["Prévision météo", "Analyse de données", "Modélisation", "Communication", "Instruments météo"],
    "Océanographe": ["Recherche marine", "Analyse de données", "Échantillonnage", "Modélisation", "Conservation"],
    "Astronome": ["Observation", "Analyse de données", "Modélisation", "Recherche", "Programmation"],
    "Psychologue": ["Écoute active", "Diagnostic", "Conseil", "Recherche", "Communication"],
    "Psychiatre": ["Diagnostic", "Prescription", "Thérapie", "Communication patient", "Éthique"],
    "Travailleur social": ["Accompagnement", "Évaluation des besoins", "Médiation", "Communication", "Empathie"],
    "Conseiller d'orientation": ["Évaluation", "Conseil", "Connaissance du marché", "Communication", "Planification"],
    "Coach": ["Motivation", "Planification", "Écoute", "Fixation d'objectifs", "Communication"],
    "Formateur": ["Pédagogie", "Conception de cours", "Animation", "Évaluation", "Communication"],
    "Animateur": ["Animation", "Organisation", "Communication", "Créativité", "Travail d'équipe"],
    "Éducateur spécialisé": ["Accompagnement", "Pédagogie", "Évaluation", "Communication", "Empathie"],
    "Orthophoniste": ["Diagnostic", "Thérapie", "Communication", "Évaluation", "Pédagogie"],
    "Kinésithérapeute": ["Rééducation", "Massage", "Évaluation", "Communication patient", "Anatomie"],
    "Ergothérapeute": ["Réadaptation", "Évaluation", "Planification", "Communication", "Empathie"],
    "Opticien": ["Évaluation visuelle", "Fabrication de lunettes", "Conseil client", "Précision", "Service client"],
    "Audioprothésiste": ["Évaluation auditive", "Ajustement d'appareils", "Conseil client", "Communication", "Technologie"],
    "Sage-femme": ["Accouchement", "Suivi prénatal", "Conseil", "Communication", "Premiers secours"],
    "Aide-soignant": ["Soins de base", "Hygiène", "Communication patient", "Empathie", "Travail d'équipe"],
    "Ambulancier": ["Transport médical", "Premiers secours", "Conduite sécuritaire", "Communication", "Gestion du stress"],
    "Laborantin": ["Analyse", "Prélèvements", "Sécurité en laboratoire", "Précision", "Rapport"],
    "Chercheur": ["Recherche", "Analyse de données", "Rédaction scientifique", "Expérimentation", "Collaboration"],
    "Professeur d'université": ["Enseignement", "Recherche", "Publication", "Mentorat", "Conception de cours"],
    "Assistant de recherche": ["Collecte de données", "Analyse", "Rédaction", "Collaboration", "Organisation"],
    "Économiste": ["Analyse économique", "Modélisation", "Prévision", "Rapport", "Connaissance des marchés"],
    "Sociologue": ["Recherche", "Analyse qualitative", "Analyse quantitative", "Rédaction", "Observation"],
    "Anthropologue": ["Recherche culturelle", "Observation", "Analyse", "Rédaction", "Terrain"],
    "Historien": ["Recherche historique", "Analyse de sources", "Rédaction", "Enseignement", "Archivage"],
    "Géographe": ["Analyse spatiale", "Cartographie", "SIG", "Recherche", "Rédaction"],
    "Politicien": ["Prise de décision", "Communication", "Négociation", "Stratégie", "Connaissance des lois"],
    "Diplomate": ["Négociation", "Communication", "Connaissance internationale", "Multilinguisme", "Protocole"],
    "Agent des douanes": ["Contrôle", "Réglementation", "Communication", "Vigilance", "Rapport"],
    "Inspecteur fiscal": ["Audit fiscal", "Analyse", "Connaissance des lois", "Rapport", "Communication"],
    "Auditeur": ["Audit", "Analyse financière", "Rapport", "Conformité", "Communication"],
    "Actuaire": ["Analyse des risques", "Modélisation", "Statistiques", "Rapport", "Logiciels actuariels"],
    "Assureur": ["Évaluation des risques", "Vente", "Conseil client", "Rédaction de polices", "Communication"],
    "Courtier": ["Négociation", "Conseil", "Connaissance des marchés", "Communication client", "Analyse"],
    "Notaire": ["Rédaction d'actes", "Conseil juridique", "Connaissance des lois", "Communication", "Éthique"]
    # Removed skills for jobs not in the top 100
}
job_skills = {job: skills for job, skills in job_skills.items() if job in jobs}


# Descriptions spécifiques par métier
job_descriptions = {
    "Enseignant": [
        "Enseignant avec {years} ans d’expérience, expert en {skill1}, j’ai conçu des cours engageants et utilisé {skill2} pour optimiser l’apprentissage.",
        "Spécialisé en {skill1}, j’ai géré des classes diversifiées pendant {years} ans, maîtrisant {skill2} pour motiver les élèves."
    ],
    "Médecin": [
        "Médecin avec {years} ans d’expérience, j’ai effectué des diagnostics précis en {skill1} et géré des urgences avec {skill2}.",
        "Spécialisé en {skill1}, j’ai travaillé {years} ans en milieu hospitalier, excelling en {skill2} et en soins patients."
    ]
    # Descriptions for other jobs will be generated by the loop below
}
# Ensure all selected jobs have descriptions
temp_job_descriptions = {
    "Enseignant": job_descriptions.get("Enseignant"),
    "Médecin": job_descriptions.get("Médecin")
}
for job in jobs:
    if job not in temp_job_descriptions or temp_job_descriptions[job] is None: # Check if job is already in or if it was None
        temp_job_descriptions[job] = [
            f"Professionnel(le) avec {{years}} ans d’expérience en {{skill1}}, compétent(e) en {{skill2}} et motivé(e) à relever des défis.",
            f"Expert(e) en {{skill1}} avec {{years}} ans d’expérience, je maîtrise {{skill2}} pour des résultats optimaux."
        ]
job_descriptions = temp_job_descriptions

# Étape 4 : Générer 14 400 CV uniques (72 CV par métier)
cvs = []
# Define base output directory and create it
base_output_dir = "generated_cvs_output"
os.makedirs(base_output_dir, exist_ok=True)
os.makedirs(os.path.join(base_output_dir, 'cvs_pdf'), exist_ok=True)
os.makedirs(os.path.join(base_output_dir, 'cvs_docx'), exist_ok=True)

# Répartition des profils
profile_types = ["junior", "intermediate", "experienced", "senior"]
cv_per_job = 1  # Generate 1 CV per job to reach 100 CVs for 100 jobs
total_cvs = 0
max_cvs = 100 # Generate only 100 files

# Générer les CVs
with ThreadPoolExecutor(max_workers=8) as executor:
    args = []
    for job in jobs:
        cv_count = 0
        attempts = 0
        max_attempts = 100  # Prevent infinite loops
        while cv_count < cv_per_job and attempts < max_attempts:
            is_djiboutian = random.random() < 0.85
            profile_type = random.choice(profile_types)
            cv = generate_cv(job, profile_type, is_djiboutian, cv_index=total_cvs)
            if is_unique_cv(cv):
                args.append((cv, total_cvs))
                cv_count += 1
                total_cvs += 1
            attempts += 1
            if total_cvs >= max_cvs:
                break
        if total_cvs >= max_cvs:
            break
    
    results = list(executor.map(generate_and_save_cv, args))
    cvs = [result["cv"] for result in results if result]

# Étape 5 : Exporter les métadonnées
cv_metadata = pd.DataFrame(cvs)
metadata_path = os.path.join(base_output_dir, "cv_metadata.csv")
cv_metadata.to_csv(metadata_path, index=False)
print(f"Métadonnées exportées dans {metadata_path}")

# Étape 6 : Créer une archive ZIP
zip_filename = os.path.join(base_output_dir, f'{max_cvs}_cvs.zip') # Dynamic zip filename
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    pdf_dir_to_zip = os.path.join(base_output_dir, 'cvs_pdf')
    for root, _, files in os.walk(pdf_dir_to_zip):
        for file in files:
            if file.endswith('.pdf'):
                full_path = os.path.join(root, file)
                # Add file to zip with relative path inside 'cvs_pdf' folder in zip
                zipf.write(full_path, os.path.join('cvs_pdf', os.path.relpath(full_path, pdf_dir_to_zip)))

    docx_dir_to_zip = os.path.join(base_output_dir, 'cvs_docx')
    for root, _, files in os.walk(docx_dir_to_zip):
        for file in files:
            if file.endswith('.docx'):
                full_path = os.path.join(root, file)
                # Add file to zip with relative path inside 'cvs_docx' folder in zip
                zipf.write(full_path, os.path.join('cvs_docx', os.path.relpath(full_path, docx_dir_to_zip)))
    
    zipf.write(metadata_path, os.path.basename(metadata_path))

print(f"Archive ZIP créée : {zip_filename}")

# Étape 7 : Télécharger l'archive
from google.colab import files
files.download(zip_filename)
print(f"L'archive ZIP est disponible localement à : {os.path.abspath(zip_filename)}")