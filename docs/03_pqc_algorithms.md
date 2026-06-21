# 03 — Algorithmes PQC

## Introduction

La **cryptographie post-quantique**, PQC, désigne des algorithmes conçus pour résister aux ordinateurs classiques et quantiques.

Les algorithmes classiques menacés sont :

```text
RSA
DSA
ECDSA
ECDH
DH
X25519
```

## KEM

Un **Key Encapsulation Mechanism**, KEM, permet à deux parties d’obtenir un secret partagé.

Fonctions :

```text
KeyGen()      → public_key, secret_key
Encaps(pk)    → ciphertext, shared_secret
Decaps(sk, c) → shared_secret
```

Formules :

$$
(pk, sk) = KeyGen()
$$

$$
(c, ss_A) = Encaps(pk)
$$

$$
ss_B = Decaps(sk, c)
$$

$$
ss_A = ss_B
$$

## ML-KEM

**ML-KEM** est un mécanisme d’encapsulation de clé basé sur les réseaux modulaires.

Il sert à :

- établir un secret partagé
- construire un handshake hybride
- compléter ou remplacer ECDH/X25519

ML-KEM ne sert pas à signer.

Variantes :

| Variante | Usage |
|---|---|
| ML-KEM-512 | léger |
| ML-KEM-768 | recommandé |
| ML-KEM-1024 | sécurité élevée |

Dans ce projet :

```text
ML-KEM-768
```

## ML-DSA

**ML-DSA** est un algorithme de signature numérique post-quantique.

Fonctions :

```text
KeyGen()       → public_key, secret_key
Sign(sk, msg)  → signature
Verify(pk, msg, signature) → true/false
```

ML-DSA sert à signer des certificats hybrides.

Variantes :

| Variante | Usage |
|---|---|
| ML-DSA-44 | léger |
| ML-DSA-65 | recommandé |
| ML-DSA-87 | sécurité élevée |

Dans ce projet :

```text
ML-DSA-65
```

## SLH-DSA

**SLH-DSA** est une famille de signatures post-quantiques basée sur les fonctions de hachage.

Avantages : hypothèses conservatrices.

Inconvénients : signatures plus grandes et performances parfois moins favorables.

## Différence importante

```text
ML-KEM = échange/encapsulation de clé
ML-DSA = signature numérique
SLH-DSA = signature hash-based
```

Erreur à éviter :

```text
ML-KEM ne signe pas.
ML-DSA ne chiffre pas.
SLH-DSA ne fait pas d'échange de clés.
```

## Utilisation dans Hybrid-PKI-Lab

- ML-KEM : handshake hybride
- ML-DSA : certificats hybrides
- SLH-DSA : extension avancée

Secret hybride :

$$
Secret_{hybrid} = HKDF(Secret_{X25519} \parallel Secret_{ML-KEM})
$$

Signature hybride :

$$
Valid_{hybrid} = Verify_{Classic} \land Verify_{ML-DSA}
$$
