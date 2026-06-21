# 05 — Modèle de Sécurité

## Objectifs

Hybrid-PKI-Lab cherche à garantir :

| Objectif | Description |
|---|---|
| Authentification | vérifier une identité |
| Intégrité | détecter toute modification |
| Non-répudiation | relier une signature à une clé privée |
| Confidentialité | protéger les secrets du handshake |
| Résistance quantique | réduire le risque futur |
| Anti-downgrade | empêcher le retour à un mode faible |
| Traçabilité | journaliser les opérations importantes |

## Actifs critiques

```text
Root CA private key
Intermediate CA private key
PQC CA secret key
Server private keys
Client private keys
Hybrid certificate payloads
CRL signing keys
Configuration policies
Audit logs
```

Le plus critique :

```text
Root CA private key
```

## Racine de confiance

PKI classique :

```text
Trust Anchor = Root CA Certificate
```

PKI hybride :

```text
Trust Anchor = Classical Root Public Key + PQC Root Public Key
```

## Hypothèses

Le projet suppose que :

- la Root CA initiale est authentique
- les clés privées CA ne sont pas compromises
- le générateur aléatoire est sûr
- les politiques de validation ne sont pas modifiées
- le trust store est correct

## Modèle d’attaquant

L’attaquant peut intercepter, modifier et rejouer des messages. Il peut présenter de faux certificats, remplacer des clés publiques, tenter un downgrade et collecter du trafic pour le futur.

Il ne doit pas pouvoir accéder aux clés privées CA ou forger des signatures valides.

## Politique classique

Un certificat classique est accepté si :

$$
Accept_{classic} = ValidChain \land ValidTime \land NotRevoked \land ValidName \land ValidUsage \land TrustedRoot
$$

## Politique hybride

Mode strict :

$$
Accept_{hybrid} = Valid_{classic} \land Valid_{PQC} \land ValidTime \land NotRevoked \land TrustedIssuer
$$

Politique recommandée :

```text
hybrid-strict
```

## Menaces principales

### Clé privée compromise

Mitigations : chiffrement, permissions, rotation, révocation, HSM et journaux d’audit.

### Fausse CA

Mitigation : vérifier que la Root CA appartient au trust store.

### Certificat expiré

$$
now > notAfter \Rightarrow Reject
$$

### Certificat révoqué

$$
serial \in CRL \Rightarrow Reject
$$

### Downgrade

$$
RequiredPolicy = hybridStrict \land UsedPolicy \neq hybridStrict \Rightarrow Reject
$$

### Harvest Now, Decrypt Later

Mitigation :

```text
X25519 + ML-KEM-768
```

$$
Secret_{hybrid} = HKDF(Secret_{X25519} \parallel Secret_{ML-KEM})
$$

## Gestion des clés

Bonnes pratiques :

```text
chmod 600 private_key.pem
encrypt private keys
never commit keys to Git
rotate keys regularly
backup keys securely
separate test and production keys
```

## Sécurité API

Endpoints sensibles à protéger :

```text
POST /ca/classical/init
POST /ca/hybrid/init
POST /certificates/classical/issue
POST /certificates/hybrid/issue
POST /certificates/revoke
```

Mesures : authentification admin, HTTPS, limitation de débit, validation stricte, logs et RBAC.

## Limites

Hybrid-PKI-Lab est pédagogique. Il ne remplace pas un HSM, une CA de production, un audit WebTrust/eIDAS ou un OCSP complet.
