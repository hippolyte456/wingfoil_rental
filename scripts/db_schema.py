import graphviz

# Création du graphe
db_schema = graphviz.Digraph(format='png', graph_attr={"rankdir": "LR"})

# Bases de données
db_schema.node("Clients", "📂 Clients\n- Nom, Email\n- Historique réservations\n- Paiements", shape="folder", style="filled", fillcolor="lightblue")
db_schema.node("Réservations", "📂 Réservations\n- ID Réservation\n- Client\n- Équipement\n- Date", shape="folder", style="filled", fillcolor="lightgreen")
db_schema.node("Équipements", "📂 Équipements\n- ID Matériel\n- Type (Wing, Board)\n- État", shape="folder", style="filled", fillcolor="lightyellow")
db_schema.node("Paiements", "📂 Paiements\n- ID Paiement\n- Client\n- Montant\n- Statut", shape="folder", style="filled", fillcolor="lightcoral")
db_schema.node("Marketing", "📂 Marketing\n- Emails envoyés\n- Statistiques\n- Leads", shape="folder", style="filled", fillcolor="lightgray")

# Inputs
db_schema.node("Formulaires Web", "🌐 Formulaires Web\n- Demande de réservation", shape="note", style="filled", fillcolor="white")
db_schema.node("Paiement en ligne", "💳 Paiement en ligne\n- Stripe, PayPal", shape="note", style="filled", fillcolor="white")
db_schema.node("Check-in", "🏝️ Check-in\n- Confirmation matériel", shape="note", style="filled", fillcolor="white")
db_schema.node("Email Marketing", "📧 Email Marketing\n- Campagnes", shape="note", style="filled", fillcolor="white")

# Outputs
db_schema.node("Tableau de bord", "📊 Tableau de bord\n- Statistiques ventes\n- Matériel disponible", shape="note", style="filled", fillcolor="white")
db_schema.node("Emails Clients", "📩 Emails Clients\n- Confirmation\n- Relances", shape="note", style="filled", fillcolor="white")

# Relations entre bases
db_schema.edge("Clients", "Réservations", label="Fait une réservation")
db_schema.edge("Réservations", "Équipements", label="Assigne matériel")
db_schema.edge("Réservations", "Paiements", label="Génère facture")
db_schema.edge("Clients", "Paiements", label="Effectue un paiement")
db_schema.edge("Clients", "Marketing", label="Ciblage publicitaire")
db_schema.edge("Marketing", "Emails Clients", label="Envoi promo")

# Relations avec Inputs et Outputs
db_schema.edge("Formulaires Web", "Réservations", label="Création")
db_schema.edge("Paiement en ligne", "Paiements", label="Validation")
db_schema.edge("Check-in", "Équipements", label="Vérification état")
db_schema.edge("Email Marketing", "Marketing", label="Campagne ciblée")
db_schema.edge("Paiements", "Tableau de bord", label="Suivi financier")
db_schema.edge("Réservations", "Tableau de bord", label="Statistiques")
db_schema.edge("Emails Clients", "Clients", label="Notification")

# Génération du fichier
db_schema_path = "/home/hippolytedreyfus/Documents/wingfoil_rental/scripts/db_schema"
db_schema.render(db_schema_path)
db_schema_path + ".png"
