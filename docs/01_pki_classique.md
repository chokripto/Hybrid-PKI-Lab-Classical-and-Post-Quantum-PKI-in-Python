# 01 — PKI Classique

## Introduction

Une **PKI**, ou **Public Key Infrastructure**, est une infrastructure permettant de gérer des clés cryptographiques, des certificats numériques et des relations de confiance.

Elle est utilisée dans HTTPS/TLS, VPN, mTLS, signature de code, signature documentaire, messagerie sécurisée, Wi-Fi entreprise et identité numérique.

## Cryptographie asymétrique

Chaque entité possède une paire de clés :

```text
Private Key  ← secrète
Public Key   ← publique
```

La clé privée sert à signer ou prouver une identité. La clé publique sert à vérifier une signature ou établir une relation cryptographique.

## Certificat numérique

Un certificat lie une identité à une clé publique.

Exemple simplifié :

```text
Subject: CN=example.com
Issuer: CN=Intermediate CA
Public Key: RSA/ECDSA/Ed25519 public key
Validity: notBefore → notAfter
Signature: signature de la CA
```

## Autorité de certification

Une **Certificate Authority**, CA, signe des certificats. Elle garantit qu’une identité possède une certaine clé publique.

Architecture classique :

```text
Root CA
   ↓
Intermediate CA
   ↓
Server / Client Certificate
```

## Root CA

La Root CA est la racine de confiance. Son certificat est généralement autosigné :

```text
Subject = Issuer
```

Formule conceptuelle :

$$
Cert_{Root} = Sign_{RootPrivateKey}(RootPublicKey, RootIdentity)
$$

La clé privée Root doit être fortement protégée, idéalement hors ligne.

## Intermediate CA

L’Intermediate CA est signée par la Root CA et signe les certificats finaux.

Avantage :

```text
La Root CA reste protégée.
L'Intermediate CA effectue les opérations quotidiennes.
```

## Certificat final

Un certificat final n’est pas une CA. Il peut être utilisé pour un serveur, un client, une application ou un équipement.

Extensions typiques :

```text
BasicConstraints: CA:FALSE
KeyUsage: digitalSignature, keyEncipherment
ExtendedKeyUsage: serverAuth ou clientAuth
SubjectAlternativeName: DNS/IP autorisés
```

## Chaîne de confiance

Validation d’une chaîne :

```text
Server Certificate
       ↓ signed by
Intermediate CA Certificate
       ↓ signed by
Root CA Certificate
       ↓ trusted by system/browser
Trust Anchor
```

Règles :

$$
Verify(Cert_{server}, PubKey_{intermediate}) = True
$$

$$
Verify(Cert_{intermediate}, PubKey_{root}) = True
$$

$$
Root \in TrustStore
$$

## CSR

Un **CSR**, Certificate Signing Request, contient l’identité demandée, la clé publique et une signature prouvant la possession de la clé privée.

Workflow :

```text
1. Générer une paire de clés.
2. Créer un CSR.
3. Envoyer le CSR à la CA.
4. Vérifier l’identité.
5. Signer le certificat.
```

## Validation d’un certificat

Un validateur doit vérifier :

1. signature
2. chaîne de confiance
3. période de validité
4. hostname ou IP
5. Key Usage
6. Extended Key Usage
7. révocation
8. Root CA de confiance

Pseudo-code :

```text
validate_certificate(cert, chain, trust_store):
    verify_time(cert)
    verify_hostname(cert)
    verify_key_usage(cert)
    verify_signature_chain(cert, chain)
    verify_revocation_status(cert)
    verify_root_in_trust_store(chain.root, trust_store)
    return trusted
```

## Révocation

Un certificat peut être révoqué avant expiration.

Mécanismes :

```text
CRL  — Certificate Revocation List
OCSP — Online Certificate Status Protocol
```

Règle CRL :

```text
if cert.serial_number in crl:
    reject certificate
```

## PKI et TLS

Dans HTTPS, la PKI authentifie le serveur. Le navigateur vérifie le certificat, la chaîne, le nom DNS, la validité et la révocation.

## Algorithmes classiques

- RSA-3072 ou RSA-4096
- ECDSA P-256/P-384
- Ed25519
- X25519 pour l’échange de clés
- SHA-256/SHA-384 pour le hachage

## Limites face au quantique

Les algorithmes suivants sont menacés par un futur ordinateur quantique puissant :

```text
RSA
DSA
ECDSA
ECDH
DH
X25519
```

Une migration vers une PKI hybride ou post-quantique devient donc nécessaire.
