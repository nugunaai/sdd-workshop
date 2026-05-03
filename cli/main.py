# cli/main.py: Typer 기반 CLI entrypoint (scaffold)
import typer

app = typer.Typer()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
