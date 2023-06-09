import typer
from src.controller.scrapper import Scrapper
from config import settings

app = typer.Typer()


@app.command()
def scrap(scrap_date: str = typer.Option(..., prompt="Date to scrap")):
    scrapper = Scrapper(scrap_date, settings.scrap.url)
    avisos = scrapper.get_grouped_avisos()

    for aviso in avisos:
        scrapper.save_aviso(aviso)


if __name__ == "__main__":
    app()



