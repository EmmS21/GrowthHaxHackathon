from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/scrape")
def scrape():
    web_html = requests.get("https://docs.dagger.io/").text
    soup = BeautifulSoup(web_html, "html.parser")

    web_text = ' '.join([item.text for item in soup.find_all('p')])

    return {"text": web_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)