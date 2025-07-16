from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import webview

app = Flask(__name__)


def extract_dialog(html_code):
    """Извлекает диалог из HTML-кода."""
    soup = BeautifulSoup(html_code, 'html.parser')
    dialog_elements = soup.find_all('p', class_='group/block')
    dialog = []
    for element in dialog_elements:
        speaker_tag = element.find('span', attrs={'data-speaker': 'true'})
        if speaker_tag:
            speaker = speaker_tag.text.strip()
            text_spans = element.find_all('span', attrs={'data-speaker': 'false'})
            text = ' '.join([span.text.strip() for span in text_spans])
            dialog.append(f"{speaker}: {text}")
    return "\n\n".join(dialog)


@app.route("/", methods=["GET", "POST"])
def index():
    # Если метод POST (файл отправлен)
    if request.method == "POST":
        file = request.files.get('html_file')
        if file and file.filename != '':
            html_code = file.read().decode('utf-8')
            extracted_dialog = extract_dialog(html_code)
            # Снова отображаем index.html, но на этот раз с результатом
            return render_template("index.html", extracted_dialog=extracted_dialog)

    # Если метод GET (первый запуск) или файл не был отправлен,
    # просто показываем index.html без результата.
    return render_template("index.html")


if __name__ == '__main__':
    webview.create_window('Анализатор диалогов', app)
    webview.start()