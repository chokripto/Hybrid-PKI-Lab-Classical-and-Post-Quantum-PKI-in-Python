# 04 — Cycle de Vie d’un Certificat

## Vue générale

Un certificat passe par plusieurs étapes :

```text
Key Generation
      ↓
CSR Generation
      ↓
Identity Validation
      ↓
Certificate Issuance
      ↓
Certificate Deployment
      ↓
Certificate Monitoring
      ↓
Renewal / Revocation / Expiration
```

## Génération des clés

PKI classique :

```text
Private Key + Public Key
```

PKI hybride :

```text
Classical Private Key + Classical Public Key
PQC Private Key       + PQC Public Key
```

La clé privée ne doit jamais être envoyée à la CA.

## CSR

Un CSR contient l’identité, la clé publique, les extensions demandées et une signature prouvant la possession de la clé privée.

Formule :

$$
CSR = Sign_{SubjectPrivateKey}(SubjectInfo \parallel SubjectPublicKey)
$$

## Validation de l’identité

La CA vérifie que le demandeur contrôle l’identité demandée : domaine, utilisateur, service, équipement ou organisation.

## Émission

Processus :

```text
1. Lire le CSR.
2. Vérifier la signature du CSR.
3. Vérifier l'identité.
4. Créer le certificat.
5. Ajouter les extensions.
6. Signer avec la clé privée CA.
```

Formule :

$$
Certificate = Sign_{CAPrivateKey}(SubjectInfo \parallel SubjectPublicKey \parallel Extensions)
$$

## Émission hybride

```text
Payload
  ↓
Signature classique
  ↓
Signature PQC
  ↓
Certificat hybride
```

$$
Sig_{classic} = Sign_{ClassicCAKey}(Payload)
$$

$$
Sig_{PQC} = Sign_{PQCCAKey}(Payload)
$$

## Déploiement

Fichiers typiques :

```text
server.key
server.crt
chain.crt
fullchain.crt
```

Pour le mode hybride expérimental :

```text
server_classical.crt
server_hybrid.json
server_pqc_public.key
server_pqc_private.key
```

## Surveillance

À surveiller :

- expiration
- révocation
- faiblesse d’algorithme
- exposition de clé privée
- mauvaise configuration TLS

## Renouvellement

Le renouvellement peut réutiliser la clé ou générer une nouvelle clé. Pour les certificats sensibles, une nouvelle clé est recommandée.

## Révocation

Un certificat révoqué doit être rejeté même si sa signature et sa date sont valides.

$$
Revoked(Certificate) = True \Rightarrow Reject
$$

## Expiration

Condition de validité temporelle :

$$
notBefore \leq now \leq notAfter
$$

Sinon, rejet.

## Journalisation

Événements à journaliser :

```text
key generation
CSR reception
identity validation
certificate issuance
certificate renewal
certificate revocation
CRL generation
OCSP response
policy change
admin access
```

Ne jamais journaliser les clés privées ou secrets partagés.

## Résumé

Une PKI fiable dépend autant de la cryptographie que de la gestion opérationnelle du cycle de vie.
