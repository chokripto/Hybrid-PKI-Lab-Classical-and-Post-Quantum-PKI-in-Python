# 06 — Scénarios d’Attaque

## Introduction

Ce document présente des attaques contre une PKI classique et une PKI hybride.

Chaque scénario décrit la menace, l’impact, la détection et le comportement attendu.

## 1. Certificat expiré

Exemple :

```text
notAfter = 2025-01-01
now      = 2026-06-20
```

Règle :

$$
now > notAfter \Rightarrow Reject
$$

Résultat attendu :

```text
rejected: certificate expired
```

## 2. Certificat pas encore valide

Règle :

$$
now < notBefore \Rightarrow Reject
$$

Résultat attendu :

```text
rejected: certificate not yet valid
```

## 3. Mauvaise chaîne de confiance

Un certificat est signé par une CA non approuvée.

Règle :

$$
Root \notin TrustStore \Rightarrow Reject
$$

Résultat attendu :

```text
rejected: untrusted root
```

## 4. Signature invalide

Un attaquant modifie le contenu d’un certificat après signature.

Règle :

$$
Verify(Payload, Signature, PublicKey_{issuer}) = False \Rightarrow Reject
$$

Résultat attendu :

```text
rejected: invalid signature
```

## 5. Certificat révoqué

Règle :

$$
serial \in CRL \Rightarrow Reject
$$

Résultat attendu :

```text
rejected: certificate revoked
```

## 6. Mauvais hostname

Exemple :

```text
Certificate SAN: example.com
Requested host: attacker.com
```

Règle :

$$
hostname \notin SAN \Rightarrow Reject
$$

## 7. Mauvais usage de clé

Exemple :

```text
Certificate usage: clientAuth
Used for: serverAuth
```

Règle :

$$
RequiredUsage \notin CertificateUsage \Rightarrow Reject
$$

## 8. Substitution de clé publique

Un attaquant remplace la clé publique du certificat. La signature doit échouer.

Règle :

$$
ModifiedPayload \Rightarrow InvalidSignature
$$

## 9. Substitution de clé PQC

Dans un certificat hybride, l’attaquant remplace la clé publique PQC.

En `hybrid-strict`, le certificat doit être rejeté.

```text
rejected: PQC signature invalid
```

## 10. Downgrade attack

L’attaquant force un mode plus faible :

```text
Expected policy: hybrid-strict
Forced policy: classical-only
```

Règle :

$$
RequiredPolicy = hybridStrict \land UsedPolicy \neq hybridStrict \Rightarrow Reject
$$

## 11. Harvest Now, Decrypt Later

L’attaquant collecte aujourd’hui du trafic chiffré pour le déchiffrer plus tard avec un ordinateur quantique.

Mitigation :

```text
X25519 + ML-KEM-768
```

$$
Secret_{hybrid} = HKDF(Secret_{X25519} \parallel Secret_{ML-KEM})
$$

## 12. Compromission de clé serveur

Réponse :

```text
1. Révoquer le certificat.
2. Générer une nouvelle clé.
3. Émettre un nouveau certificat.
4. Auditer les logs.
```

## 13. Compromission d’Intermediate CA

Réponse :

```text
revoke intermediate CA
create new intermediate CA
reissue affected certificates
publish CRL
audit issued certificates
```

## 14. Compromission de Root CA

Impact catastrophique. Il faut reconstruire la PKI et mettre à jour les trust stores.

## 15. SHA-1 ou MD5

Algorithmes interdits :

```text
MD5
SHA-1
```

Résultat attendu :

```text
rejected: weak signature algorithm
```

## 16. Self-signed non approuvé

Règle :

$$
SelfSigned \land Cert \notin TrustStore \Rightarrow Reject
$$

## Résumé

| Scénario | Résultat attendu |
|---|---|
| Certificat expiré | rejet |
| Pas encore valide | rejet |
| Mauvaise chaîne | rejet |
| Signature invalide | rejet |
| Révoqué | rejet |
| Mauvais hostname | rejet |
| Mauvais usage | rejet |
| Substitution de clé | rejet |
| Substitution PQC | rejet |
| Downgrade | rejet |
| HNDL | recommander hybride |
| Clé serveur compromise | révocation |
| Intermediate CA compromise | révocation de la CA |
| Root CA compromise | reconstruction PKI |
| SHA-1/MD5 | rejet |
| Self-signed non approuvé | rejet |
