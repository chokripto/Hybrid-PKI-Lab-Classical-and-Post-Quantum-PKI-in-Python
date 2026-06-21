import typer

app = typer.Typer(help="Hybrid PKI Lab CLI")

@app.command()
def init_classical_pki():
    typer.echo("Initializing classical PKI...")

@app.command()
def init_hybrid_pki():
    typer.echo("Initializing hybrid PKI...")

@app.command()
def issue_classical_cert(common_name: str):
    typer.echo(f"Issuing classical certificate for {common_name}")

@app.command()
def issue_hybrid_cert(common_name: str):
    typer.echo(f"Issuing hybrid certificate for {common_name}")

@app.command()
def verify_cert(path: str, policy: str = "hybrid-strict"):
    typer.echo(f"Verifying {path} with policy {policy}")

@app.command()
def benchmark():
    typer.echo("Running benchmarks...")

if __name__ == "__main__":
    app()
