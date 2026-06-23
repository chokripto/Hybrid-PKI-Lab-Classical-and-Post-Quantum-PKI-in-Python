from benchmarks.benchmark_handshake import classical_x25519_handshake


def test_classical_x25519_handshake():
    secret = classical_x25519_handshake()

    assert isinstance(secret, bytes)
    assert len(secret) > 0
