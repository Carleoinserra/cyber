import mechanize
import webbrowser
import mechanize
import webbrowser
import ssl
import certifi

# Imposta il percorso dei certificati di autorità di certificazione
ssl._create_default_https_context = ssl._create_unverified_context
ssl._create_default_https_context().load_verify_locations(certifi.where())

# Crea una nuova istanza di Browser
browser = mechanize.Browser()

# Imposta alcune opzioni di navigazione
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')]

# URL di ricerca di Bing
search_url = 'https://www.bing.com/search?cc=it&q=cyber'

# Effettua la ricerca su Bing
response = browser.open(search_url)

# Apri la pagina di risultati di ricerca nel browser
webbrowser.open(response.geturl())

# Chiudi il browser
browser.close()
