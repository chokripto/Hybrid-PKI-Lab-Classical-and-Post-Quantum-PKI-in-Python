# 02 — PKI Hybride

## Introduction

Une **PKI hybride** combine une PKI classique avec des mécanismes post-quantiques. Elle permet de conserver la compatibilité actuelle tout en préparant une résistance aux futures attaques quantiques.

## Pourquoi une PKI hybride ?

Les systèmes classiques reposent souvent sur RSA, ECDSA, ECDH ou X25519. Ces algorithmes sont efficaces contre les ordinateurs classiques, mais vulnérables à un ordinateur quantique suffisamment puissant.

Une migration directe vers le tout-PQC est difficile, car les nouveaux algorithmes ont des tailles plus grandes, des bibliothèques plus récentes et un support protocolaire encore en évolution.

## Principe de sécurité

Pour une signature hybride :

$$
Valid_{hybrid} = Valid_{classical} \land Valid_{PQC}
$$

Pour un échange de clé hybride :

$$
Secret_{hybrid} = KDF(Secret_{classical} \parallel Secret_{PQC})
$$

L’attaquant doit casser les deux mondes pour réussir dans le mode strict.

## Architecture

```text
Hybrid Root CA
    ├── Classical CA Key
    ├── PQC CA Key
    └── Hybrid CA Policy

Hybrid Intermediate CA
    ├── Classical Signing Key
    ├── PQC Signing Key
    └── Hybrid Certificate Issuer

Hybrid End-Entity Certificate
    ├── Classical Public Key
    ├── PQC Public Key
    ├── Classical Signature
    └── PQC Signature
```

## Certificat hybride

Exemple pédagogique :

```json
{
  "subject": "CN=hybrid.example.com",
  "issuer": "CN=Hybrid Root CA",
  "classical_algorithm": "ECDSA-P256",
  "classical_public_key": "...",
  "pqc_signature_algorithm": "ML-DSA-65",
  "pqc_public_key": "...",
  "classical_signature": "...",
  "pqc_signature": "..."
}
```

Ce format est expérimental et destiné au laboratoire.

## Signature hybride

La CA hybride signe le même payload avec deux clés :

$$
Sig_{classic} = Sign_{classic}(Payload)
$$

$$
Sig_{PQC} = Sign_{PQC}(Payload)
$$

Le certificat final contient :

```text
Payload
Classical Signature
PQC Signature
```

## Politiques de validation

| Politique | Règle |
|---|---|
| classical-only | accepter si la signature classique est valide |
| pqc-only | accepter si la signature PQC est valide |
| hybrid-strict | accepter si les deux signatures sont valides |
| hybrid-fallback | accepter si au moins une signature est valide |

Politique recommandée :

```text
hybrid-strict
```

## Handshake hybride

Dans ce projet :

```text
Classical part: X25519
PQC part: ML-KEM-768
KDF: HKDF-SHA256
```

Processus :

```text
1. Le serveur génère une clé X25519.
2. Le serveur génère une paire ML-KEM.
3. Le client effectue un échange X25519.
4. Le client encapsule un secret ML-KEM.
5. Le serveur décapsule le secret ML-KEM.
6. Les deux côtés dérivent un secret hybride.
```

Formule :

$$
Secret_{hybrid} = HKDF(Secret_{X25519} \parallel Secret_{ML-KEM})
$$

## Protection contre le downgrade

Une attaque de downgrade force un mode plus faible :

```text
Expected: hybrid-strict
Forced: classical-only
```

Mitigation : imposer localement `hybrid-strict` et refuser les politiques plus faibles.

## Migration

Étapes recommandées :

1. inventaire des algorithmes classiques
2. double émission classique + hybride
3. activation progressive de la validation hybride
4. passage en `hybrid-strict`
5. réduction progressive de la dépendance classique

## Résumé

Une PKI hybride est une stratégie de transition vers le post-quantique. Elle combine la maturité des mécanismes classiques avec la résistance future des algorithmes PQC.
