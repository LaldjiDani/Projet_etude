from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from db import connect
from werkzeug.security import check_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'ma_cle_secrete_projet_l2'

from werkzeug.security import generate_password_hash


# --- ACCUEIL ---
@app.route('/')
def index():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT nomVille FROM ville ORDER BY nomVille")
    villes_dispo = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT descripMotcle FROM motcle ORDER BY descripMotcle")
    mots_cles_dispo = [row[0] for row in cursor.fetchall()]

    search_query = request.args.get('q')
    filter_ville = request.args.get('ville')
    filter_mot = request.args.get('mot')

    sql = """
        SELECT 
            r.nomResto, 
            r.ouverture, 
            r.fermeture, 
            r.etat, 
            v.nomVille, 
            STRING_AGG(m.descripMotcle, ', ') as mots_cles
        FROM restaurant r
        JOIN se_situe s ON r.nomResto = s.nomResto
        JOIN ville v ON s.idVille = v.idVille
        LEFT JOIN decrit_par dp ON r.nomResto = dp.nomResto
        LEFT JOIN motcle m ON dp.idMot = m.idMot
        WHERE 1=1 
    """
    params = []
    if search_query:
        sql += " AND r.nomResto ILIKE %s"
        params.append(f"%{search_query}%")

    if filter_ville:
        sql += " AND v.nomVille = %s"
        params.append(filter_ville)
        
    if filter_mot:
        sql += " AND m.descripMotcle = %s"
        params.append(filter_mot)
        
    # on utilise ORDER BY... pour que les restaurant ouvert soit en première ligne
    sql += """ 
    GROUP BY r.nomResto, r.ouverture, r.fermeture, r.etat, v.nomVille 
    ORDER BY 
        (CASE WHEN r.ouverture <= r.fermeture THEN 
                (CURRENT_TIME BETWEEN r.ouverture AND r.fermeture)
            ELSE 
                (CURRENT_TIME >= r.ouverture OR CURRENT_TIME <= r.fermeture)
        END) DESC,
        r.nomResto ASC;
    """
    cursor.execute(sql, tuple(params))
    restaurants = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # On renvoie tout au template : les restos trouve, et les listes pour reafficher le formulaire
    return render_template('index.html', 
                           restaurants=restaurants, 
                           villes=villes_dispo, 
                           mots_cles=mots_cles_dispo)

# --- INSCRIPTION CLIENT ---
@app.route('/register_client')
def page_register_client():
    conn = connect()
    cursor = conn.cursor()
    # On récupère les villes pour que le client puisse choisir
    cursor.execute("SELECT idVille, nomVille FROM ville ORDER BY nomVille")
    villes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('register_client.html', villes=villes)

# --- Route POST ---
@app.route('/action_register_client', methods=['POST'])
def action_register_client():
    # Infos Personnelles
    prenom = request.form.get('prenom')
    nom = request.form.get('nom')
    email = request.form.get('email')
    tel = request.form.get('tel')
    cb = request.form.get('cb')
    mdp = request.form.get('mdp')
    
    # Infos Adresse (Nouveaux champs)
    rue = request.form.get('rue')
    id_ville = request.form.get('id_ville')

    # Vérification
    if not prenom or not nom or not email or not mdp or not rue or not id_ville:
        flash("Veuillez remplir tous les champs obligatoires.", "error")
        return redirect(url_for('page_register_client'))

    conn = connect()
    cursor = conn.cursor()

    try:
        # 1. Hachage du mot de passe
        mdp_hache = generate_password_hash(mdp) 

        # 2. Création du CLIENT
        sql_client = """
            INSERT INTO client (email, prenomCl, nomCl, numtelCl, cb, fidelite, motdepasse)
            VALUES (%s, %s, %s, %s, %s, 0, %s);
        """
        cursor.execute(sql_client, (email, prenom, nom, tel, cb, mdp_hache))

        # 3. Création de l'ADRESSE
        # On calcule le prochain ID disponible (MAX + 1) car ce n'est pas un SERIAL automatique
        cursor.execute("SELECT COALESCE(MAX(idadresse), 0) + 1 FROM adresse")
        new_id_adresse = cursor.fetchone()[0]

        sql_adresse = "INSERT INTO adresse (idadresse, idVille, rue) VALUES (%s, %s, %s)"
        cursor.execute(sql_adresse, (new_id_adresse, id_ville, rue))

        # 4. Liaison dans HABITE
        sql_habite = "INSERT INTO habite (email, idadresse) VALUES (%s, %s)"
        cursor.execute(sql_habite, (email, new_id_adresse))

        # Si tout s'est bien passé, on valide la transaction
        conn.commit()
        
        flash("Compte créé avec succès ! Connectez-vous.", "success")
        return redirect(url_for('page_login_client')) 

    except Exception as e:
        conn.rollback() # Annule TOUT si une étape plante
        flash(f"Erreur lors de l'inscription : {e}", "error")
        return redirect(url_for('page_register_client'))
    
    finally:
        cursor.close()
        conn.close()

# --- CONNEXION CLIENT ---
@app.route('/login_client')
def page_login_client():
    return render_template('login_client.html')

# --- CLIENT ---
@app.route('/action_login_client', methods=['POST'])
def action_login_client():
    email = request.form.get('email')
    mdp = request.form.get('mdp')

    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM client WHERE email = %s", (email,))
        client = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if client and check_password_hash(client.motdepasse, mdp):
            session['user'] = client.email
            session['prenom'] = client.prenomcl
            session['type_compte'] = 'client'
            session['fidelite'] = client.fidelite 
            flash(f"Bonjour {client.prenomcl}, vous êtes connecté !", "success")
            return redirect(url_for('index'))
        else:
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for('page_login_client'))
    except Exception as e:
        flash(f"Erreur technique : {e}", "error")
        return redirect(url_for('page_login_client'))

# --- RESTAURANT ---
@app.route('/restaurant/<nom_resto>')
def restaurant_detail(nom_resto):
    conn = connect()
    cursor = conn.cursor()
    sql_resto = """
        SELECT r.*, v.nomVille 
        FROM restaurant r
        JOIN se_situe s ON r.nomResto = s.nomResto
        JOIN ville v ON s.idVille = v.idVille
        WHERE r.nomResto = %s
    """
    cursor.execute(sql_resto, (nom_resto,))
    resto = cursor.fetchone()

    # Liste des plats
    sql_plats = """
        SELECT p.* FROM plat p
        JOIN composee c ON p.nomPlat = c.nomPlat
        JOIN restaurant r ON r.nomCarte = c.nomCarte
        WHERE r.nomResto = %s
    """
    cursor.execute(sql_plats, (nom_resto,))
    plats = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('restaurant_detail.html', resto=resto, plats=plats)

# --- VALIDER LA COMMANDE ---
@app.route('/checkout')
def checkout():
    # Faut être connecté
    if 'user' not in session:
        flash("Veuillez vous connecter pour commander.", "error")
        return redirect(url_for('page_login_client'))

    # Faut un panier
    if 'panier' not in session or not session['panier']:
        flash("Votre panier est vide.", "error")
        return redirect(url_for('index'))

    panier = session['panier']
    user_email = session['user']
    
    # On récupère le nom du resto 
    nom_resto = panier[0]['resto'] 

    conn = connect()
    cursor = conn.cursor()

    try:
        sql_cmd = "INSERT INTO commande (heureCommande, statut) VALUES (NOW(), 'en_attente') RETURNING idCommande;"
        cursor.execute(sql_cmd)
        id_commande = cursor.fetchone()[0]

        cursor.execute("INSERT INTO a_commande (email, idCommande) VALUES (%s, %s)", (user_email, id_commande))

        cursor.execute("INSERT INTO prepare (nomResto, idCommande) VALUES (%s, %s)", (nom_resto, id_commande))

        comptage = {}
        for item in panier:
            plat = item['nom']
            comptage[plat] = comptage.get(plat, 0) + 1

        for nom_plat, quantite in comptage.items():
            sql_contient = "INSERT INTO contient (idCommande, nomPlat, quantite) VALUES (%s, %s, %s)"
            cursor.execute(sql_contient, (id_commande, nom_plat, quantite))
        
        # point de fidelité 10 points par commande
        cursor.execute("UPDATE client SET fidelite = fidelite + 10 WHERE email = %s", (user_email,))
        session['fidelite'] += 10

        session.pop('panier', None)
        flash("Commande validée avec succès ! Le restaurant la prépare.", "success")
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('profil_client'))

    except Exception as e:
        conn.rollback()
        flash(f"Erreur lors de la commande : {e}", "error")
        return redirect(url_for('panier'))

# --- CONNEXION LIVREUR ---
@app.route('/login_livreur')
def page_login_livreur():
    return render_template('login_livreur.html')

@app.route('/action_login_livreur', methods=['POST'])
def action_login_livreur():
    matricule = request.form.get('matricule')
    mdp = request.form.get('mdp')

    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livreur WHERE numLi = %s", (matricule,))
        livreur = cursor.fetchone()
        cursor.close()
        conn.close()
        # Vérification
        if livreur and check_password_hash(livreur.motdepasse, mdp):
            session['user'] = livreur.numli
            session['prenom'] = livreur.prenomli
            session['type_compte'] = 'livreur'
            flash(f"Bon courage {livreur.prenomli} !", "success")
            return redirect(url_for('dashboard_livreur'))
        else:
            flash("Matricule ou mot de passe incorrect.", "error")
            return redirect(url_for('page_login_livreur'))

    except Exception as e:
        flash(f"Erreur : {e}", "error")
        return redirect(url_for('page_login_livreur'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- DASHBOARD LIVREUR ---
@app.route('/dashboard_livreur')
def dashboard_livreur():
    # Vérification du compte
    if session.get('type_compte') != 'livreur':
        return redirect(url_for('page_login_livreur'))

    matricule = session['user']
    conn = connect()
    cursor = conn.cursor()

    # 1. Récupération ville du livreur
    cursor.execute("SELECT localisation FROM livreur WHERE numLi = %s", (matricule,))
    res = cursor.fetchone()
    
    if res:
        try:
            ma_ville = res.localisation 
        except AttributeError:
            ma_ville = res[0]
    else:
        ma_ville = 'Inconnue'

    # 2. Commandes DISPONIBLES (Dans la zone du livreur)
    sql_dispo = """
        SELECT c.idCommande, c.heureCommande, r.nomResto, r.adresse_rue, v.nomVille
        FROM commande c
        JOIN prepare p ON c.idCommande = p.idCommande
        JOIN restaurant r ON p.nomResto = r.nomResto
        JOIN se_situe s ON r.nomResto = s.nomResto
        JOIN ville v ON s.idVille = v.idVille
        WHERE c.statut = 'en_attente' 
        AND v.nomVille = %s 
        ORDER BY c.heureCommande ASC;
    """
    cursor.execute(sql_dispo, (ma_ville,))
    commandes_dispo = cursor.fetchall()

    # 3. Mes livraisons EN COURS 
    sql_encours = """
        SELECT 
            c.idCommande, 
            c.heureCommande, 
            r.nomResto, 
            r.adresse_rue, 
            client.prenomCl, 
            client.numtelCl, 
            COALESCE(a.rue, 'Pas d''adresse renseignée') as rue_client
        FROM commande c
        JOIN livre l ON c.idCommande = l.idCommande
        JOIN prepare p ON c.idCommande = p.idCommande
        JOIN restaurant r ON p.nomResto = r.nomResto
        JOIN a_commande ac ON c.idCommande = ac.idCommande
        JOIN client ON ac.email = client.email
        -- LEFT JOIN ici pour éviter le bug des "commandes invisibles"
        LEFT JOIN habite h ON client.email = h.email
        LEFT JOIN adresse a ON h.idadresse = a.idadresse
        WHERE l.numLi = %s AND c.statut = 'en_livraison';
    """
    cursor.execute(sql_encours, (matricule,))
    mes_livraisons = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard_livreur.html', 
                           ville=ma_ville, 
                           dispo=commandes_dispo, 
                           encours=mes_livraisons)

# --- PRENDRE UNE COMMANDE ---
@app.route('/prendre_commande/<int:id_cmd>')
def prendre_commande(id_cmd):
    if session.get('type_compte') != 'livreur': 
        return redirect(url_for('index'))
    
    matricule = session['user']
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE commande SET statut = 'en_livraison' WHERE idCommande = %s", (id_cmd,))
        cursor.execute("INSERT INTO livre (numLi, idCommande) VALUES (%s, %s)", (matricule, id_cmd))
        flash("Commande acceptée ! En route !", "success")
    except Exception as e:
        flash(f"Erreur : {e}", "error")
        conn.rollback()

    cursor.close()
    conn.close()
    return redirect(url_for('dashboard_livreur'))


# --- TERMINER UNE LIVRAISON ---
@app.route('/terminer_commande/<int:id_cmd>')
def terminer_commande(id_cmd):
    if session.get('type_compte') != 'livreur': 
        return redirect(url_for('index'))
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE commande SET statut = 'livree' WHERE idCommande = %s", (id_cmd,))
    flash("Bravo ! Livraison terminée.", "success")
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard_livreur'))

# --- PROFIL CLIENT ---
@app.route('/profil_client')
def profil_client():
    if 'user' not in session:
        return redirect(url_for('page_login_client'))

    conn = connect()
    cursor = conn.cursor()
    sql = """
        SELECT 
            c.idCommande, 
            c.heureCommande, 
            c.statut, 
            p.nomResto,
            SUM(pl.prix * co.quantite) as total_prix
        FROM commande c
        JOIN a_commande ac ON c.idCommande = ac.idCommande
        JOIN prepare p ON c.idCommande = p.idCommande
        JOIN contient co ON c.idCommande = co.idCommande
        JOIN plat pl ON co.nomPlat = pl.nomPlat
        WHERE ac.email = %s
        GROUP BY c.idCommande, c.heureCommande, c.statut, p.nomResto
        ORDER BY c.idCommande DESC;
    """
    cursor.execute(sql, (session['user'],))
    mes_commandes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('profil_client.html', commandes=mes_commandes)

# --- AJOUTER AU PANIER ---
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    nom_plat = request.form.get('nom_plat')
    prix = float(request.form.get('prix'))
    nom_resto = request.form.get('nom_resto')
    
    if 'panier' not in session:
        session['panier'] = []
    
    session['panier'].append({
        'nom': nom_plat, 
        'prix': prix,
        'resto': nom_resto
    })
    
    session.modified = True
    flash(f"{nom_plat} ajouté au panier.", "success")
    return redirect(request.referrer)


# --- VOIR LE PANIER ---
@app.route('/panier')
def panier():
    if 'panier' not in session or not session['panier']:
        return render_template('panier.html', items=[], total=0)
    
    # Calcul du total
    total = sum(item['prix'] for item in session['panier'])
    
    return render_template('panier.html', items=session['panier'], total=total)


# --- VIDER LE PANIER ---
@app.route('/clear_cart')
def clear_cart():
    session.pop('panier', None)
    flash("Panier vidé.", "info")
    return redirect(url_for('panier'))

# --- ANNULER COMMANDE ---
@app.route('/annuler_commande/<int:id_cmd>', methods=['POST'])
def annuler_commande(id_cmd):
    # on vérifie que le client est connecté
    if 'user' not in session:
        return redirect(url_for('page_login_client'))
    
    conn = connect()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE commande 
            SET statut = 'annulee' 
            FROM a_commande 
            WHERE commande.idCommande = a_commande.idCommande 
            AND a_commande.email = %s 
            AND commande.idCommande = %s 
            AND commande.statut = 'en_attente'
        """, (session['user'], id_cmd))
        
        # rowcount nous dit combien de ligne ont ete modifiee
        if cursor.rowcount > 0:
            flash("commande annulee avec succes.", "success")
        else:
            flash("impossible d'annuler cette commande (deja prise en charge ?).", "error")
            
        conn.commit() # On valide la modification
        
    except Exception as e:
        flash(f"Erreur lors de l'annulation : {e}", "error")
        
    cursor.close()
    conn.close()
    
    return redirect(url_for('profil_client'))

# --- CONSULTER LES DONNEES DE LA VUE ---
@app.route('/transparence')
def transparence():
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM vue_popularite_specialites")
    stats = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('transparence.html', stats=stats)

# --- FONCTION VÉRIFIER L'HEURE ---
@app.context_processor
def utility_processor():
    def est_ouvert(ouverture, fermeture):
        """
        Renvoie True si le resto est ouvert maintenant, False sinon.
        Gère le cas des restos qui ferment après minuit.
        """
        if not ouverture or not fermeture:
            return False
            
        now = datetime.now().time()
        
        if ouverture <= fermeture:
            return ouverture <= now <= fermeture
        else:
            return now >= ouverture or now <= fermeture
            
    return dict(est_ouvert=est_ouvert)

if __name__ == '__main__':
    app.run()