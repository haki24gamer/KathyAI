import random
import datetime
import json

# --- Constants from the problem description ---
TOTAL_CV = 14400
PERCENT_DJIBOUTIAN = 0.87
PERCENT_FOREIGN = 0.13
NUM_DJIBOUTIAN_CV = int(TOTAL_CV * PERCENT_DJIBOUTIAN) # 12528
NUM_FOREIGN_CV = TOTAL_CV - NUM_DJIBOUTIAN_CV # 1872

NUM_JOBS = 200
CV_PER_JOB = TOTAL_CV // NUM_JOBS # 72

# --- Data Provided by User (Ensure full lists are used) ---
djiboutian_first_names = [
    # Masculins
    "Ahmed", "Hassan", "Mahad", "Ismail", "Abdourahman", "Ali", "Ibrahim", "Abdi", "Youssouf", "Souleiman",
    "Jamal", "Zakaria", "Mohamed", "Farhan", "Idriss", "Faysal", "Yassin", "Bilal", "Omar", "Abdallah",
    "Barkhad", "Anwar", "Saïd", "Nour", "Dini", "Mahamoud", "Khaled", "Awaleh", "Bileh", "Muse",
    "Saad", "Salah", "Warsame", "Guedi", "Walid", "Abdirahman", "Haroun", "Moustapha", "Abshir",
    "Suleyman", "Dawoud", "Houssein", "Abokor", "Aweis", "Hersi", "Aaden", "Ayub", "Farah", "Ayman",
    "Rachid", "Madar", "Nuradin", "Hassanali", "Kalif", "Deria", "Saidou", "Samatar", "Tahlil",
    "Wais", "Darar", "Robleh", "Barre", "Aliyow", "Djamal", "Sharmarke", "Kamil", "Mahdi", "Gedi", # Corrected from "Gedi" in OCR
    "Duale", "Barkat",
    # Féminins
    "Fadumo", "Ayan", "Hibo", "Ifrah", "Nimo", "Hawa", "Sagal", "Asha", "Safia", "Hodan",
    "Zamzam", "Amal", "Faiza", "Rahma", "Amina", "Khadija", "Naima", "Yasmin", "Salma", "Ikram",
    "Roda", "Halima", "Saida", "Habiba", "Mariam", "Fatouma", "Asli", "Souad", "Batula", "Anisa",
    "Hani", "Deeqa", "Shaafi", "Sahra", "Rihana", "Munira", "Bilan", "Layla", "Nadra", "Muna",
    "Mako", "Sucaad", "Faisa", "Anab", "Haniyo", "Sulekha", "Fawzia", "Farhia", "Ifra", "Sudi", # Corrected from "Ifra"
    "Lubna", "Bashira", "Nura", "Zamzama", "Zaynab", "Deka", "Ikran", "Saynab", "Jawahir",
    "Farhiyo", "Ubah", "Shukri", "Ismahan", "Barwaqo", "Rukia", "Misra", "Nasteexo", "Samia",
    "Asma", "Rahimo"
] # Should be 120

djiboutian_last_names_provided = [
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
] # Provided list has 79 items, 78 unique. Spec needs 105.

# Pad Djiboutian last names if not enough unique ones are provided to meet the 105 requirement
unique_djiboutian_last_names = sorted(list(set(djiboutian_last_names_provided)))
djiboutian_last_names_final = unique_djiboutian_last_names[:]
if len(djiboutian_last_names_final) < 105:
    print(f"Warning: Provided Djiboutian last names list has {len(djiboutian_last_names_final)} unique names, less than the required 105.")
    needed_more = 105 - len(djiboutian_last_names_final)
    for i in range(needed_more):
        djiboutian_last_names_final.append(f"NomSupplémentaire{i+1}")
    print(f"Padded with {needed_more} placeholder last names to meet the 105 requirement for combinations.")
djiboutian_last_names_final = djiboutian_last_names_final[:105] # Ensure exactly 105

foreign_first_names_data = {
    "French": ["Lucas", "Hugo", "Enzo", "Arthur", "Léo", "Nathan", "Raphaël", "Jules", "Tom", "Clément", "Louis", "Adam", "Noé", "Théo", "Maxime"],
    "English": ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles", "Joseph", "Thomas", "Daniel", "Matthew", "Andrew", "Kevin", "Brian"],
    "Russian": ["Ivan", "Dimitri", "Alexei", "Nikolai", "Mikhail", "Vladimir", "Yuri", "Andrei", "Sergei", "Pavel"],
    "Italian": ["Luca", "Matteo", "Marco", "Andrea", "Alessandro", "Gabriele", "Giovanni", "Antonio", "Stefano", "Francesco"],
    "Ethiopian": ["Bekele", "Tadesse", "Tesfaye", "Abebe", "Dawit", "Getachew", "Hailu", "Kassahun", "Solomon", "Yosef"],
    "Other": ["Ali", "Omar", "Amir", "Malik", "Ibrahim", "Hamza", "Sami", "Elias", "Youssef", "Karim"]
}
foreign_last_names_flat = [
    "Dubois", "Lefèvre", "Bernard", "Girard", "Morel",
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Petrov", "Sokolov", "Kuznetsov", "Ivanov", "Makarov",
    "Rossi", "Bianchi", "Romano", "Conti", "Gallo",
    "Teshome", "Gebre", "Mekonnen", "Alemu", "Desta",
    "El Fassi", "Ben Omar", "Diouf", "Bamba", "Haddad"
]

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
    "Agent des douanes", "Inspecteur fiscal", "Auditeur", "Actuaire", "Assureur", "Courtier", "Notaire",
    "Huissier", "Juge", "Procureur", "Greffier", "Planificateur", "Gestionnaire de projet", "Scrum master",
    "Product owner", "UX designer", "UI designer", "Développeur mobile", "Développeur backend", "Développeur frontend",
    "Administrateur système", "Administrateur réseau", "Spécialiste cybersécurité", "Testeur QA", "Technicien support",
    "Community manager", "Responsable communication", "Publicitaire", "Organisateur d'événements", "Organisateur de mariage",
    "DJ", "Musicien", "Chanteur", "Acteur", "Réalisateur", "Scénariste", "Producteur", "Costumier", "Maquilleur",
    "Décorateur", "Éclairagiste", "Technicien son", "Technicien lumière", "Styliste", "Modéliste", "Couturier",
    "Bijoutier", "Horloger", "Ébéniste", "Menuisier", "Charpentier", "Maçon", "Peintre en bâtiment", "Carreleur",
    "Couvreur", "Vitrier", "Serrurier", "Forgeron", "Soudeur", "Métallurgiste", "Conducteur d'engins", "Grutier",
    "Chauffeur poids lourd", "Livreur", "Magasinier", "Employé de banque", "Caissier", "Vendeur", "Manager de magasin",
    "Merchandiser", "Sommelier", "Œnologue", "Viticulteur", "Brasseur", "Distillateur", "Apiculteur", "Éleveur",
    "Vacher", "Berger", "Maraîcher", "Arboriculteur", "Pépiniériste", "Semencier", "Paysan", "Technicien agricole",
    "Vulcanologue", "Sismologue", "Hydrologue", "Glaciologue", "Cartographe", "Topographe", "Géomaticien",
    "Épidémiologiste", "Généticien", "Biochimiste", "Microbiologiste", "Pharmacologue", "Toxicologue",
    "Nutritionniste", "Diététicien", "Préparateur physique", "Entraîneur", "Arbitre", "Agent sportif",
    "Journaliste sportif", "Commentateur", "Éditeur", "Libraire", "Imprimeur", "Relieur"
] # len(jobs) == 200

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
    "Notaire": ["Rédaction d'actes", "Conseil juridique", "Connaissance des lois", "Communication", "Éthique"],
    "Huissier": ["Exécution des décisions", "Rédaction", "Connaissance juridique", "Communication", "Organisation"],
    "Juge": ["Interprétation des lois", "Prise de décision", "Éthique", "Communication", "Analyse"],
    "Procureur": ["Poursuite", "Analyse juridique", "Plaidoyer", "Éthique", "Communication"],
    "Greffier": ["Gestion des dossiers", "Rédaction", "Organisation", "Connaissance juridique", "Communication"],
    "Planificateur": ["Planification", "Analyse", "Coordination", "Communication", "Gestion de projets"],
    "Gestionnaire de projet": ["Planification", "Coordination", "Budgétisation", "Communication", "Résolution de problèmes"],
    "Scrum master": ["Facilitation", "Agilité", "Coordination", "Communication", "Résolution de conflits"],
    "Product owner": ["Définition de produit", "Priorisation", "Communication", "Agilité", "Analyse des besoins"],
    "UX designer": ["Recherche utilisateur", "Prototypage", "Tests d'utilisabilité", "Design d'interface", "Communication"],
    "UI designer": ["Design d'interface", "Prototypage", "Graphisme", "Outils (Figma)", "Créativité"],
    "Développeur mobile": ["Programmation (Swift, Kotlin)", "Tests", "Conception d'applications", "Git", "API"],
    "Développeur backend": ["Programmation (Python, Java)", "Bases de données", "API", "Sécurité", "Git"],
    "Développeur frontend": ["HTML/CSS", "JavaScript", "Frameworks (React)", "Responsive design", "Git"],
    "Administrateur système": ["Gestion de serveurs", "Sécurité", "Réseaux", "Scripting", "Maintenance"],
    "Administrateur réseau": ["Configuration réseau", "Sécurité", "Dépannage", "Monitoring", "Protocoles"],
    "Spécialiste cybersécurité": ["Analyse des menaces", "Pentesting", "Sécurité réseau", "Cryptographie", "Rapport"],
    "Testeur QA": ["Tests fonctionnels", "Tests automatisés", "Rédaction de cas de test", "Bug tracking", "Communication"],
    "Technicien support": ["Dépannage", "Support utilisateur", "Connaissance IT", "Communication", "Documentation"],
    "Community manager": ["Gestion des réseaux sociaux", "Création de contenu", "Engagement", "Analyse", "Communication"],
    "Responsable communication": ["Stratégie de communication", "Rédaction", "Gestion de crise", "Relations publiques", "Coordination"],
    "Publicitaire": ["Conception de campagnes", "Analyse de marché", "Créativité", "Communication", "Gestion de projets"],
    "Organisateur d'événements": ["Planification", "Coordination", "Budgétisation", "Communication", "Négociation"],
    "Organisateur de mariage": ["Planification", "Coordination", "Créativité", "Communication client", "Budgétisation"],
    "DJ": ["Mixage", "Connaissance musicale", "Animation", "Équipements audio", "Créativité"],
    "Musicien": ["Interprétation", "Composition", "Connaissance musicale", "Pratique d'instruments", "Créativité"],
    "Chanteur": ["Chant", "Interprétation", "Scène", "Connaissance musicale", "Créativité"],
    "Acteur": ["Interprétation", "Improvisation", "Mémorisation", "Expression", "Travail d'équipe"],
    "Réalisateur": ["Mise en scène", "Direction d'acteurs", "Montage", "Scénario", "Créativité"],
    "Scénariste": ["Écriture", "Développement de personnages", "Structure narrative", "Créativité", "Recherche"],
    "Producteur": ["Gestion de projets", "Financement", "Coordination", "Négociation", "Communication"],
    "Costumier": ["Conception de costumes", "Couture", "Recherche historique", "Créativité", "Communication"],
    "Maquilleur": ["Maquillage", "Effets spéciaux", "Connaissance des produits", "Créativité", "Précision"],
    "Décorateur": ["Conception de décors", "Aménagement", "Créativité", "Budgétisation", "Communication"],
    "Éclairagiste": ["Conception d'éclairage", "Installation", "Programmation", "Créativité", "Technologie"],
    "Technicien son": ["Gestion du son", "Mixage", "Installation", "Dépannage", "Technologie"],
    "Technicien lumière": ["Installation lumière", "Programmation", "Dépannage", "Connaissance des équipements", "Créativité"],
    "Styliste": ["Conception de mode", "Tendances", "Croquis", "Créativité", "Communication"],
    "Modéliste": ["Patronage", "Couture", "Conception", "Précision", "Connaissance des tissus"],
    "Couturier": ["Couture", "Confection", "Précision", "Connaissance des tissus", "Service client"],
    "Bijoutier": ["Conception de bijoux", "Travail des métaux", "Sertissage", "Créativité", "Précision"],
    "Horloger": ["Réparation de montres", "Assemblage", "Précision", "Connaissance mécanique", "Service client"],
    "Ébéniste": ["Travail du bois", "Conception de meubles", "Finition", "Précision", "Créativité"],
    "Menuisier": ["Travail du bois", "Assemblage", "Lecture de plans", "Utilisation d'outils", "Précision"],
    "Charpentier": ["Construction de structures", "Lecture de plans", "Travail du bois", "Normes de sécurité", "Précision"],
    "Maçon": ["Construction", "Lecture de plans", "Maçonnerie", "Normes de sécurité", "Travail d'équipe"],
    "Peintre en bâtiment": ["Peinture", "Préparation de surfaces", "Connaissance des matériaux", "Précision", "Service client"],
    "Carreleur": ["Pose de carrelage", "Coupe", "Préparation de surfaces", "Précision", "Normes de qualité"],
    "Couvreur": ["Pose de toitures", "Réparation", "Normes de sécurité", "Connaissance des matériaux", "Travail en hauteur"],
    "Vitrier": ["Pose de vitres", "Coupe", "Réparation", "Précision", "Service client"],
    "Serrurier": ["Fabrication de serrures", "Installation", "Dépannage", "Connaissance des mécanismes", "Service client"],
    "Forgeron": ["Forge", "Travail des métaux", "Conception", "Précision", "Créativité"],
    "Soudeur": ["Soudure", "Connaissance des métaux", "Normes de sécurité", "Précision", "Utilisation d'équipements"],
    "Métallurgiste": ["Analyse des métaux", "Production", "Connaissance des alliages", "Sécurité", "Rapport"],
    "Conducteur d'engins": ["Conduite", "Maintenance", "Normes de sécurité", "Coordination", "Précision"],
    "Grutier": ["Opération de grues", "Normes de sécurité", "Coordination", "Communication", "Précision"],
    "Chauffeur poids lourd": ["Conduite", "Navigation", "Entretien", "Respect des horaires", "Normes de sécurité"],
    "Livreur": ["Livraison", "Navigation", "Service client", "Gestion du temps", "Conduite sécuritaire"],
    "Magasinier": ["Gestion des stocks", "Organisation", "Réception", "Expédition", "Informatique"],
    "Employé de banque": ["Service client", "Gestion de transactions", "Connaissance bancaire", "Communication", "Précision"],
    "Caissier": ["Gestion de caisse", "Service client", "Comptabilité de base", "Communication", "Travail sous pression"],
    "Vendeur": ["Vente", "Service client", "Négociation", "Connaissance des produits", "Communication"],
    "Manager de magasin": ["Gestion d'équipe", "Vente", "Gestion des stocks", "Budgétisation", "Communication"],
    "Merchandiser": ["Présentation visuelle", "Analyse des ventes", "Gestion des stocks", "Créativité", "Communication"],
    "Sommelier": ["Connaissance des vins", "Dégustation", "Conseil client", "Gestion de cave", "Communication"],
    "Œnologue": ["Vinification", "Analyse chimique", "Dégustation", "Recherche", "Gestion de production"],
    "Viticulteur": ["Culture de la vigne", "Récolte", "Entretien", "Connaissance des sols", "Gestion"],
    "Brasseur": ["Brassage", "Connaissance des ingrédients", "Contrôle qualité", "Hygiène", "Créativité"],
    "Distillateur": ["Distillation", "Connaissance des alcools", "Contrôle qualité", "Hygiène", "Précision"],
    "Apiculteur": ["Gestion des ruches", "Récolte de miel", "Connaissance des abeilles", "Entretien", "Commercialisation"],
    "Éleveur": ["Soins aux animaux", "Gestion d'élevage", "Connaissance animale", "Commercialisation", "Maintenance"],
    "Vacher": ["Traite", "Soins aux vaches", "Entretien", "Connaissance animale", "Hygiène"],
    "Berger": ["Gestion du troupeau", "Soins aux animaux", "Navigation", "Connaissance animale", "Entretien"],
    "Maraîcher": ["Culture maraîchère", "Récolte", "Irrigation", "Connaissance des sols", "Commercialisation"],
    "Arboriculteur": ["Culture d'arbres fruitiers", "Taille", "Récolte", "Connaissance des sols", "Entretien"],
    "Pépiniériste": ["Culture de plantes", "Greffage", "Entretien", "Connaissance botanique", "Commercialisation"],
    "Semencier": ["Production de semences", "Contrôle qualité", "Recherche", "Connaissance botanique", "Commercialisation"],
    "Paysan": ["Agriculture", "Élevage", "Gestion de ferme", "Connaissance des sols", "Commercialisation"],
    "Technicien agricole": ["Analyse des sols", "Gestion des cultures", "Utilisation de machines", "Rapport", "Conseil"],
    "Vulcanologue": ["Analyse volcanique", "Recherche", "Cartographie", "Évaluation des risques", "Rapport"],
    "Sismologue": ["Analyse sismique", "Modélisation", "Recherche", "Évaluation des risques", "Rapport"],
    "Hydrologue": ["Analyse de l'eau", "Modélisation", "Recherche", "Gestion des ressources", "Rapport"],
    "Glaciologue": ["Analyse des glaciers", "Recherche", "Échantillonnage", "Modélisation", "Rapport"],
    "Cartographe": ["Cartographie", "SIG", "Analyse spatiale", "Précision", "Logiciels"],
    "Topographe": ["Mesures topographiques", "Cartographie", "Utilisation d'équipements", "Précision", "Rapport"],
    "Géomaticien": ["SIG", "Analyse spatiale", "Cartographie", "Programmation", "Recherche"],
    "Épidémiologiste": ["Analyse des données", "Recherche", "Prévention", "Rapport", "Statistiques"],
    "Généticien": ["Analyse génétique", "Recherche", "Expérimentation", "Rédaction scientifique", "Bioinformatique"],
    "Biochimiste": ["Analyse biochimique", "Expérimentation", "Recherche", "Rédaction scientifique", "Sécurité"],
    "Microbiologiste": ["Analyse microbiologique", "Expérimentation", "Recherche", "Sécurité", "Rapport"],
    "Pharmacologue": ["Recherche pharmacologique", "Expérimentation", "Analyse", "Sécurité", "Rédaction"],
    "Toxicologue": ["Analyse toxicologique", "Recherche", "Évaluation des risques", "Rapport", "Sécurité"],
    "Nutritionniste": ["Conseil alimentaire", "Évaluation", "Planification", "Communication", "Recherche"],
    "Diététicien": ["Planification alimentaire", "Conseil", "Évaluation", "Communication", "Suivi"],
    "Préparateur physique": ["Entraînement", "Évaluation physique", "Planification", "Motivation", "Communication"],
    "Entraîneur": ["Coaching", "Planification", "Motivation", "Évaluation", "Communication"],
    "Arbitre": ["Connaissance des règles", "Prise de décision", "Communication", "Impartialité", "Gestion du stress"],
    "Agent sportif": ["Négociation", "Gestion de carrière", "Connaissance du sport", "Communication", "Réseautage"],
    "Journaliste sportif": ["Rédaction", "Interview", "Connaissance sportive", "Montage", "Communication"],
    "Commentateur": ["Commentaire en direct", "Connaissance sportive", "Communication", "Improvisation", "Charisme"],
    "Éditeur": ["Révision", "Planification éditoriale", "Coordination", "Connaissance du marché", "Communication"],
    "Libraire": ["Vente", "Conseil client", "Gestion des stocks", "Connaissance littéraire", "Communication"],
    "Imprimeur": ["Impression", "Gestion des machines", "Contrôle qualité", "Organisation", "Précision"],
    "Relieur": ["Reliure", "Restauration", "Précision", "Connaissance des matériaux", "Créativité"]
}
generic_job_skills = ["Communication", "Travail d'équipe", "Résolution de problèmes", "Organisation", "Adaptabilité", "Gestion du temps", "Esprit critique", "Créativité", "Leadership", "Souci du détail", "Analyse", "Initiative", "Apprentissage continu"]
for job_item in jobs: # Ensure all jobs have some skills
    if job_item not in job_skills:
        job_skills[job_item] = random.sample(generic_job_skills, k=random.randint(5, min(10, len(generic_job_skills))))

djiboutian_addresses = ["Rue de Balbala, Djibouti", "Quartier Ambouli, Djibouti", "Avenue Gabode, Djibouti", "Cité Arhiba, Djibouti", "Boulevard de la République, Djibouti"]
djiboutian_institutions = ["Université de Djibouti", "Lycée d’État de Djibouti", "Institut de Formation Professionnelle", "Centre de Formation Technique de Balbala", "École Nationale de Commerce"]
djiboutian_companies = ["Port de Djibouti", "Ministère de l’Éducation", "Djibouti Telecom", "Hôpital Général Peltier", "Banque de Djibouti", "Électricité de Djibouti", "Aéroport International de Djibouti", "Entreprise de Construction Locale", "Agence de Voyage Djiboutienne", "Société de Services Informatiques"]

# --- Added/Derived Data Structures ---
foreign_universities = {
    "French": ["Sorbonne Université", "Université PSL", "École Polytechnique", "Sciences Po Paris", "HEC Paris"],
    "English": ["University of Oxford", "University of Cambridge", "Imperial College London", "UCL", "King's College London"],
    "Russian": ["Lomonosov Moscow State University", "Saint Petersburg State University", "Bauman Moscow State Technical University"],
    "Italian": ["University of Bologna", "Sapienza University of Rome", "Polytechnic University of Milan"],
    "Ethiopian": ["Addis Ababa University", "Mekelle University", "Jimma University", "Bahir Dar University"],
    "Other": ["Harvard University", "Stanford University", "MIT", "University of Toronto", "National University of Singapore", "ETH Zurich"]
}
foreign_addresses = {
    "French": ["10 Rue de Rivoli, 75001 Paris", "25 Avenue des Champs-Élysées, 75008 Paris", "1 Place de la Bourse, 69002 Lyon"],
    "English": ["1 Baker Street, London, W1U 8ED", "10 Oxford Street, London, W1D 1BS", "22 King's Parade, Cambridge, CB2 1SP"],
    "Russian": ["Tverskaya Street 1, Moscow, 125009", "Nevsky Prospekt 10, St. Petersburg, 191186", "Arbat Street 5, Moscow, 119002"],
    "Italian": ["Via del Corso 100, 00186 Rome", "Piazza San Marco 1, 30124 Venice", "Via Montenapoleone 8, 20121 Milan"],
    "Ethiopian": ["Bole Sub-City, Kebele 03/05, Addis Ababa", "Kirkos Sub-City, Woreda 01, Addis Ababa", "Meskel Flower Area, Addis Ababa"],
    "Other": ["123 Main Street, Anytown, NY 10001, USA", "456 Oak Avenue, Toronto, ON M5H 2N2, Canada", "789 Pine Road, 10115 Berlin, Germany"]
}
foreign_companies = {
    "French": ["TotalEnergies", "LVMH", "BNP Paribas", "AXA", "Sanofi", "Renault"],
    "English": ["HSBC", "Unilever", "BP", "GlaxoSmithKline", "Vodafone", "Shell"],
    "Russian": ["Gazprom", "Rosneft", "Sberbank", "Lukoil", "Yandex", "Kaspersky Lab"],
    "Italian": ["Eni", "Generali", "Intesa Sanpaolo", "Ferrari", "Gucci", "Fiat"],
    "Ethiopian": ["Ethiopian Airlines", "Commercial Bank of Ethiopia", "Ethio Telecom", "Awash Bank", "Dashen Bank"],
    "Other": ["Google", "Microsoft", "Apple", "Amazon", "Tata Consultancy Services", "Samsung", "Toyota"]
}

_fln_keys = list(foreign_first_names_data.keys())
foreign_last_names_by_nationality = {}
for i, key in enumerate(_fln_keys):
    start_index = i * 5
    end_index = start_index + 5
    foreign_last_names_by_nationality[key] = foreign_last_names_flat[start_index:end_index] if end_index <= len(foreign_last_names_flat) else foreign_last_names_flat[start_index:]
for nat in _fln_keys: # Fallback for any missing nationalities
    if not foreign_last_names_by_nationality.get(nat):
        foreign_last_names_by_nationality[nat] = ["LastNameGeneric1", "LastNameGeneric2", "LastNameGeneric3", "LastNameGeneric4", "LastNameGeneric5"]


generic_majors = [
    "Administration des Affaires", "Marketing", "Finance", "Ressources Humaines", "Informatique", "Génie Logiciel", "Génie Civil", 
    "Génie Mécanique", "Génie Électrique", "Sciences Politiques", "Relations Internationales", "Journalisme", "Communication",
    "Lettres", "Langues Étrangères", "Histoire", "Géographie", "Sociologie", "Psychologie", "Biologie", "Chimie", "Physique", 
    "Mathématiques", "Statistiques", "Médecine", "Pharmacie", "Soins Infirmiers", "Santé Publique", "Droit", "Économie",
    "Arts Visuels", "Musique", "Design Graphique", "Architecture", "Urbanisme"
]
degree_types = ["Licence", "Master", "Doctorat", "Diplôme d'Ingénieur", "BTS", "DUT", "MBA", "PhD", "Bachelor", "Master of Science"]
current_year = datetime.datetime.now().year

# --- Helper Functions ---
def generate_djiboutian_names(first_names, last_names_list, num_required):
    all_combinations = list(set([f"{fname} {lname}" for fname in first_names for lname in last_names_list]))
    if len(all_combinations) < num_required:
        print(f"Critical Warning: Not enough unique Djiboutian name combinations ({len(all_combinations)}) for {num_required} CVs. Max possible with provided data. This may lead to fewer Djiboutian CVs than targeted or duplicates if forced.")
        # This should not happen if first_names=120 and last_names_list=105 (12600 combos)
        return random.sample(all_combinations, len(all_combinations)) # Return all available
    return random.sample(all_combinations, num_required)

def generate_foreign_name(nationality):
    first_name_list = foreign_first_names_data.get(nationality, foreign_first_names_data["Other"])
    last_name_list = foreign_last_names_by_nationality.get(nationality, foreign_last_names_by_nationality["Other"])
    return f"{random.choice(first_name_list)} {random.choice(last_name_list)}"

generated_emails = set()
def generate_email(full_name):
    name_part = "".join(c for c in full_name if c.isalnum() or c == ' ').replace(" ", ".").lower()
    domain = random.choice(["gmail.com", "yahoo.fr", "outlook.com", "hotmail.dj", "protonmail.com"])
    email = f"{name_part}@{domain}"
    counter = 1
    original_email_base = email 
    while email in generated_emails:
        name_part_with_counter = "".join(c for c in full_name if c.isalnum() or c == ' ').replace(" ", ".").lower() + str(counter)
        email = f"{name_part_with_counter}@{domain}"
        counter += 1
    generated_emails.add(email)
    return email

def generate_phone_number(nationality):
    if nationality == "Djiboutian": return f"+253 77 {random.randint(10,99):02d} {random.randint(10,99):02d} {random.randint(10,99):02d}"
    if nationality == "French": return f"+33 {random.choice(['6','7'])} {random.randint(10,99):02d} {random.randint(10,99):02d} {random.randint(10,99):02d} {random.randint(10,99):02d}"
    if nationality == "Russian": return f"+7 {random.randint(900,999)} {random.randint(100,999):03d} {random.randint(10,99):02d} {random.randint(10,99):02d}"
    if nationality == "Ethiopian": return f"+251 91 {random.randint(100,999):03d} {random.randint(1000,9999):04d}"
    return f"+{random.randint(1,99)} {random.randint(100,999)} {random.randint(100000,999999)}" # Generic

def generate_address(nationality):
    if nationality == "Djiboutian": return random.choice(djiboutian_addresses)
    return random.choice(foreign_addresses.get(nationality, foreign_addresses["Other"]))

def generate_education(nationality, age, job_title):
    major = random.choice(generic_majors) # Default major
    # Simple relevance logic
    if any(s in job_title.lower() for s in ["ingénieur", "développeur", "informatique", "data", "technicien"]): major = random.choice([m for m in generic_majors if any(t in m.lower() for t in ["informatique", "génie", "math", "physique", "systèmes", "électrique", "mécanique"])] or [major])
    elif any(s in job_title.lower() for s in ["médecin", "infirmier", "pharmacien", "santé", "biologiste"]): major = random.choice([m for m in generic_majors if any(t in m.lower() for t in ["médecine", "soins", "pharmacie", "santé", "biologie"])] or [major])
    elif any(s in job_title.lower() for s in ["comptable", "financier", "banquier", "marketing", "commerce"]): major = random.choice([m for m in generic_majors if any(t in m.lower() for t in ["finance", "comptabilité", "économie", "gestion", "marketing", "commerce"])] or [major])

    grad_year_offset = random.randint(0,3) 
    default_grad_age = 22 + grad_year_offset
    grad_year = current_year - (age - default_grad_age)
    if grad_year >= current_year: grad_year = current_year - random.randint(1,2) # Must be in the past
    if grad_year < (current_year - age + 18) : grad_year = current_year - age + 18 # Min grad age 18

    institution = random.choice(djiboutian_institutions) if nationality == "Djiboutian" else random.choice(foreign_universities.get(nationality, foreign_universities["Other"]))
    return {"degree": random.choice(degree_types), "major": major, "institution": institution, "graduation_year": grad_year}

def generate_experience(age, education_grad_year, target_job_title, nationality):
    experiences = []
    max_possible_exp_years = max(0, age - education_grad_year - random.randint(0,1)) # Allow for gap year
    if max_possible_exp_years <= 0: return experiences

    total_years_of_exp_to_distribute = random.randint(0, max_possible_exp_years) # Person might not have worked all possible years
    if total_years_of_exp_to_distribute == 0: return experiences

    num_jobs = random.randint(1, min(4, total_years_of_exp_to_distribute // 2 + 1)) # 1 to 4 jobs
    
    exp_end_year_for_current_job = current_year 

    for i in range(num_jobs):
        if total_years_of_exp_to_distribute <= 0: break
        
        avg_duration_per_job = max(1, total_years_of_exp_to_distribute // (num_jobs - i))
        exp_duration = random.randint(1, max(1, avg_duration_per_job + 1)) # Vary duration a bit
        exp_duration = min(exp_duration, total_years_of_exp_to_distribute)

        is_current_job = (i == 0 and random.random() < 0.75) # 75% chance most recent job is current
        
        actual_end_year = exp_end_year_for_current_job if not is_current_job else current_year
        actual_start_year = actual_end_year - exp_duration

        if actual_start_year < education_grad_year: # Adjust if starts before graduation
            actual_start_year = education_grad_year
            exp_duration = actual_end_year - actual_start_year
            if exp_duration <= 0: continue # Skip if this makes duration invalid

        job_title_past = random.choice(jobs)
        if i == 0 and random.random() < 0.8: job_title_past = target_job_title # Most recent often target job
        
        company = random.choice(djiboutian_companies) if nationality == "Djiboutian" else random.choice(foreign_companies.get(nationality, foreign_companies["Other"]))
        
        desc_bullets = [f"Responsable de {random.choice(['la gestion', 'l\'optimisation', 'le développement'])} de {random.choice(['projets X', 'processus Y', 'solutions Z'])}.",
                        f"Collaboration avec {random.choice(['les équipes internes', 'les clients', 'les partenaires externes'])} pour {random.choice(['atteindre les objectifs', 'améliorer les performances', 'assurer la satisfaction'])}.",
                        f"Utilisation de {random.choice(['compétences analytiques', 'logiciels spécifiques', 'méthodologies agiles'])} pour {random.choice(['résoudre des problèmes complexes', 'livrer des résultats de qualité', 'innover'])}."]

        experiences.append({
            "job_title": job_title_past, "company": company,
            "start_date": f"{random.randint(1,12):02d}/{actual_start_year}",
            "end_date": "Présent" if is_current_job else f"{random.randint(1,12):02d}/{actual_end_year}",
            "description": "- " + "\n- ".join(random.sample(desc_bullets, k=random.randint(2,3)))
        })
        
        total_years_of_exp_to_distribute -= exp_duration
        exp_end_year_for_current_job = actual_start_year - random.randint(0,1) # End of previous job is start of this one minus gap
        
    return experiences[::-1] # Chronological

def generate_professional_summary(job_title, years_experience, skills_list):
    adj = random.choice(["dévoué(e)", "expérimenté(e)", "dynamique", "polyvalent(e)", "rigoureux(se)"])
    s1 = random.choice(skills_list) if skills_list else "la résolution de problèmes"
    s2 = random.choice(skills_list) if len(skills_list) > 1 else "le travail d'équipe"
    if years_experience == 0: return f"Jeune diplômé(e) en {job_title.lower()}, motivé(e) et prêt(e) à mettre en pratique mes compétences en {s1} et {s2}. Recherche une première opportunité pour contribuer et apprendre."
    if years_experience <= 3: return f"{job_title} {adj} avec {years_experience} ans d'expérience. Fortes compétences en {s1} et {s2}. Enthousiaste à l'idée de relever de nouveaux défis."
    s3 = random.choice(skills_list) if len(skills_list) > 2 else 'la gestion de projet'
    return f"{job_title} {adj} avec {years_experience} ans d'expérience. Expertise avérée en {s1}, {s2} et {s3}. Orienté(e) résultats et capable de diriger des initiatives."

# --- Main Generation Logic ---
print("Starting CV data generation...")
all_candidates_base = []

# 1. Djiboutian candidates
djiboutian_unique_full_names = generate_djiboutian_names(djiboutian_first_names, djiboutian_last_names_final, NUM_DJIBOUTIAN_CV)
for name in djiboutian_unique_full_names:
    all_candidates_base.append({"full_name": name, "nationality": "Djiboutian"})

# 2. Foreign candidates
foreign_nationalities_list = list(foreign_first_names_data.keys())
for _ in range(NUM_FOREIGN_CV):
    nat = random.choice(foreign_nationalities_list)
    all_candidates_base.append({"full_name": generate_foreign_name(nat), "nationality": nat})

random.shuffle(all_candidates_base)
print(f"Generated {len(all_candidates_base)} base candidate profiles.")

all_cv_data = []
candidate_idx = 0
pdf_count = 0
word_count = 0
total_target_cv_formats = TOTAL_CV // 2

for job_idx, current_job_title in enumerate(jobs):
    # print(f"Processing job {job_idx+1}/{NUM_JOBS}: {current_job_title}") # Verbose
    for _ in range(CV_PER_JOB):
        if candidate_idx >= len(all_candidates_base): break
        
        base_profile = all_candidates_base[candidate_idx]
        candidate_idx += 1
        
        full_name, nationality = base_profile["full_name"], base_profile["nationality"]
        age = random.randint(22, 55)
        
        education_info = generate_education(nationality, age, current_job_title)
        years_exp_val = max(0, age - education_info["graduation_year"] - random.randint(0,1)) # Years of experience value

        # Skills (5-15)
        min_s, max_s = 5, 15
        num_s_target = random.randint(min_s, max_s)
        job_specific_skills = job_skills.get(current_job_title, [])
        
        selected_skills = []
        if len(job_specific_skills) >= num_s_target:
            selected_skills = random.sample(job_specific_skills, num_s_target)
        else:
            selected_skills = job_specific_skills[:] # Take all specific
            if len(selected_skills) < min_s: # Pad if less than min_skills
                needed_generic = min_s - len(selected_skills)
                generic_padding = [s for s in generic_job_skills if s not in selected_skills]
                if len(generic_padding) >= needed_generic:
                    selected_skills.extend(random.sample(generic_padding, needed_generic))
                else:
                    selected_skills.extend(generic_padding)
        selected_skills = selected_skills[:max_s] # Ensure not over max due to padding

        # CV Format
        # Determine CV format to ensure a 50/50 split between PDF and Word
        # total_target_cv_formats is already defined as TOTAL_CV // 2 (e.g., 7200 for 14400 CVs)

        can_assign_pdf = pdf_count < total_target_cv_formats
        # For an even TOTAL_CV, the target for Word is also total_target_cv_formats
        can_assign_word = word_count < total_target_cv_formats

        if can_assign_pdf and can_assign_word:
            # Both formats can be assigned; alternate to maintain balance.
            # Assign to PDF if its count is less than or equal to Word's count,
            # otherwise assign to Word. This creates an alternating pattern.
            if pdf_count <= word_count:
                cv_format = "PDF"
            else:
                cv_format = "Word"
        elif can_assign_pdf:
            # Only PDF can be assigned (Word quota likely met).
            cv_format = "PDF"
        elif can_assign_word:
            # Only Word can be assigned (PDF quota likely met).
            cv_format = "Word"
        else:
            # Both quotas are met. This state implies that the number of CVs
            # processed should be at or near TOTAL_CV.
            # This assigns a fallback format if the loop were to continue unexpectedly.
            cv_format = "PDF" # Fallback assignment

        if cv_format == "PDF": pdf_count += 1
        else: word_count += 1

        all_cv_data.append({
            "id": len(all_cv_data) + 1, "full_name": full_name, "email": generate_email(full_name), 
            "phone": generate_phone_number(nationality), "address": generate_address(nationality),
            "date_of_birth": f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/{current_year - age}", "age": age,
            "nationality": nationality, "target_job_title": current_job_title,
            "professional_summary": generate_professional_summary(current_job_title, years_exp_val, selected_skills),
            "skills": selected_skills, "education": [education_info],
            "experience": generate_experience(age, education_info["graduation_year"], current_job_title, nationality),
            "cv_format": cv_format,
            "languages": ["Français (Courant)", random.choice(["Anglais (Bon niveau)", "Arabe (Notions)", "Somali (Langue maternelle)"] if nationality == "Djiboutian" else ["Anglais (Courant)", "Langue locale (Courant)"])]
        })
    if (job_idx + 1) % 20 == 0: print(f"Processed {job_idx+1}/{NUM_JOBS} jobs...")


print(f"\nGenerated {len(all_cv_data)} CV data entries.")
print(f"PDFs: {pdf_count}, Word Docs: {word_count}")

# --- Verification (Optional) ---
djib_cv_count = sum(1 for cv in all_cv_data if cv['nationality'] == 'Djiboutian')
foreign_cv_count = len(all_cv_data) - djib_cv_count
print(f"Actual Djiboutian CVs: {djib_cv_count} (Target: {NUM_DJIBOUTIAN_CV})")
print(f"Actual Foreign CVs: {foreign_cv_count} (Target: {NUM_FOREIGN_CV})")

djib_names_set = set()
djib_duplicates = 0
for cv_item in all_cv_data:
    if cv_item['nationality'] == 'Djiboutian':
        if cv_item['full_name'] in djib_names_set: djib_duplicates += 1
        djib_names_set.add(cv_item['full_name'])
print(f"Unique Djiboutian names generated: {len(djib_names_set)}")
if djib_duplicates > 0: print(f"WARNING: {djib_duplicates} duplicate Djiboutian names found!")
else: print("Djiboutian names are unique.")

# Save to JSON file
output_filename = "cv_data_generation.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(all_cv_data, f, indent=2, ensure_ascii=False)
print(f"\nCV data saved to {output_filename}")

# Example of one CV
if all_cv_data:
    print("\n--- Example CV Data (First Entry from file) ---")
    with open(output_filename, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    print(json.dumps(loaded_data[0], indent=2, ensure_ascii=False))