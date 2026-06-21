from pathlib import Path
import matplotlib.pyplot as plt

OUTPUT_DIR = Path("docs/diagrams")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def box(ax, text, x, y):
    ax.text(x, y, text, ha="center", va="center", bbox=dict(boxstyle="round", linewidth=1.5), fontsize=10)

def save_pki_chain():
    fig, ax = plt.subplots(figsize=(8, 6)); ax.axis("off")
    box(ax, "Root CA\nSelf-Signed\nTrust Anchor", 0.5, 0.8)
    box(ax, "Intermediate CA\nSigned by Root CA", 0.5, 0.55)
    box(ax, "Server Certificate\nSigned by Intermediate CA", 0.5, 0.3)
    box(ax, "Client / Browser\nTrust Store", 0.15, 0.55)
    for s, e in [((0.5, .73), (.5, .62)), ((.5, .48), (.5, .37)), ((.23, .57), (.42, .78)), ((.23, .53), (.42, .32))]:
        ax.annotate("", xy=e, xytext=s, arrowprops=dict(arrowstyle="->"))
    ax.set_title("Classical PKI Chain of Trust")
    plt.savefig(OUTPUT_DIR / "pki_chain.png", bbox_inches="tight", dpi=200); plt.close()

def save_hybrid_certificate():
    fig, ax = plt.subplots(figsize=(10, 7)); ax.axis("off")
    box(ax, "Hybrid Certificate", .5, .9)
    items = [("Unsigned Payload\nSubject, Issuer, Validity", .25, .7), ("Classical Public Key\nRSA / ECDSA / Ed25519", .75, .7), ("PQC Public Key\nML-DSA", .25, .5), ("Classical Signature\nCA Classical Key", .75, .5), ("PQC Signature\nCA PQC Key", .25, .3), ("Policy\nhybrid-strict", .75, .3), ("Validator\nAccept = classical AND PQC", .5, .1)]
    for t, x, y in items:
        box(ax, t, x, y)
        if y > .1:
            ax.annotate("", xy=(x, y+.07), xytext=(.5, .85), arrowprops=dict(arrowstyle="->"))
    ax.set_title("Hybrid Certificate Structure")
    plt.savefig(OUTPUT_DIR / "hybrid_certificate.png", bbox_inches="tight", dpi=200); plt.close()

def save_hybrid_handshake():
    fig, ax = plt.subplots(figsize=(11, 7)); ax.axis("off")
    steps = ["1. Server generates X25519 key pair", "2. Server generates ML-KEM key pair", "3. Server sends public keys and hybrid certificate", "4. Client validates hybrid certificate", "5. Client computes X25519 shared secret", "6. Client encapsulates ML-KEM secret", "7. Client sends X25519 public key and ML-KEM ciphertext", "8. Server computes X25519 shared secret", "9. Server decapsulates ML-KEM ciphertext", "10. Both derive HKDF(secret_x25519 || secret_mlkem)"]
    y = .9
    for step in steps:
        box(ax, step, .5, y)
        if y > .14:
            ax.annotate("", xy=(.5, y-.055), xytext=(.5, y-.02), arrowprops=dict(arrowstyle="->"))
        y -= .085
    ax.set_title("Hybrid Handshake: X25519 + ML-KEM")
    plt.savefig(OUTPUT_DIR / "hybrid_handshake.png", bbox_inches="tight", dpi=200); plt.close()

if __name__ == "__main__":
    save_pki_chain(); save_hybrid_certificate(); save_hybrid_handshake()
    print("Diagrams generated in docs/diagrams/")
