# -*- coding: utf-8 -*-
from config.ca_configs import *

# WWW HOST
WWW_HOST = "fr.simplyhired.ca"
WWW_SCHEME_AND_HOST = "http://" + WWW_HOST

### fr-ca Mini Browse ###
BROWSE_URLS = (
    [
        [{'link_url': 'q-Administration', 'link_text': 'Administration'}],
        [{'link_url': 'q-Architecture', 'link_text': 'Architecture'}],
        [{'link_url': 'q-Art', 'link_text': 'Art'}],
        [{'link_url': 'q-Arts graphiques', 'link_text': 'Arts graphiques'}],
        [{'link_url': 'q-Assurance qualité', 'link_text': 'Assurance qualité'}],
        [{'link_url': 'q-Cadre', 'link_text': 'Cadre'}],
        [{'link_url': 'q-Comptabilité', 'link_text': 'Comptabilité'}],
        [{'link_url': 'q-Développement commercial', 'link_text': 'Développement commercial'}],
        [{'link_url': 'q-Enseignement', 'link_text': 'Enseignement'}],
        [{'link_url': 'q-Été', 'link_text': 'Été'}],
        [{'link_url': 'q-Finance', 'link_text': 'Finance'}],
        [{'link_url': 'q-Gestion', 'link_text': 'Gestion'}],
        [{'link_url': 'q-Hôtel', 'link_text': 'Hôtel'}],
        [{'link_url': 'q-Indépendant', 'link_text': 'Indépendant'}],
        [{'link_url': 'q-Ingénierie', 'link_text': 'Ingénierie'}],
        [{'link_url': 'q-Internet', 'link_text': 'Internet'}],
        [{'link_url': 'q-IT', 'link_text': 'IT'}],
        [{'link_url': 'q-Logiciel', 'link_text': 'Logiciel'}],
        [{'link_url': 'q-Logistique', 'link_text': 'Logistique'}],
        [{'link_url': 'q-Marketing', 'link_text': 'Marketing'}]
        ],
    [
        [{'link_url': 'q-Média', 'link_text': 'Média'}],
        [{'link_url': 'q-Mise en réseau', 'link_text': 'Mise en réseau'}],
        [{'link_url': 'q-Publicité', 'link_text': 'Publicité'}],
        [{'link_url': 'q-Ressources humaines', 'link_text': 'Ressources humaines'}],
        [{'link_url': 'q-Restaurant', 'link_text': 'Restaurant'}],
        [{'link_url': 'q-RP', 'link_text': 'RP'}],
        [{'link_url': 'q-Saisonnier', 'link_text': 'Saisonnier'}],
        [{'link_url': 'q-Santé', 'link_text': 'Santé'}],
        [{'link_url': 'q-Sciences', 'link_text': 'Sciences'}],
        [{'link_url': 'q-Service clientèle', 'link_text': 'Service clientèle'}],
        [{'link_url': 'q-Service juridique', 'link_text': 'Service juridique'}],
        [{'link_url': 'q-Soins infirmiers', 'link_text': 'Soins infirmiers'}],
        [{'link_url': 'q-Stages', 'link_text': 'Stages'}],
        [{'link_url': 'q-Systèmes', 'link_text': 'Systèmes'}],
        [{'link_url': 'q-Technologie', 'link_text': 'Technologie'}],
        [{'link_url': 'q-Temporaire', 'link_text': 'Temporaire'}],
        [{'link_url': 'q-Temps partiel', 'link_text': 'Temps partiel'}],
        [{'link_url': 'q-Transport', 'link_text': 'Transport'}],
        [{'link_url': 'q-Travail administratif', 'link_text': 'Travail administratif'}],
        [{'link_url': 'q-Ventes', 'link_text': 'Ventes'}]
        ]
)

### FOR DEV UNIT TESTING ###
DEV_TEST_CONFIG = 'FR-CA'
