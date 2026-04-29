import unicodedata
from urllib.parse import quote

from behave import given, then, when
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _wait(context, seconds=15):
    return WebDriverWait(context.driver, seconds)


def _normalize(value):
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(
        char for char in normalized if not unicodedata.combining(char)
    ).lower()


def _dismiss_google_dialogs(context):
    driver = context.driver
    candidates = [
        (By.ID, "L2AGLb"),
        (By.XPATH, "//button[.//div[text()='Aceptar todo'] or text()='Aceptar todo']"),
        (By.XPATH, "//button[.//div[text()='Accept all'] or text()='Accept all']"),
        (By.XPATH, "//button[.//div[text()='Reject all'] or text()='Reject all']"),
    ]

    for by, value in candidates:
        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((by, value))
            )
            button.click()
            return
        except TimeoutException:
            continue


def _visible_text(context):
    return _normalize(context.driver.find_element(By.TAG_NAME, "body").text)


def _ensure_iteso_search_open(context):
    driver = context.driver
    if driver.find_elements(By.CSS_SELECTOR, "#search-element.buscador-show"):
        return

    icons = driver.find_elements(By.ID, "icon-search")
    for icon in icons:
        if icon.is_displayed():
            driver.execute_script("arguments[0].click();", icon)
            _wait(context).until(
                EC.visibility_of_element_located((By.ID, "ipt-search"))
            )
            return

    raise AssertionError("No se pudo abrir el buscador de ITESO")


def _search_iteso(context, query):
    _ensure_iteso_search_open(context)
    search_input = _wait(context).until(
        EC.element_to_be_clickable((By.ID, "ipt-search"))
    )
    search_input.clear()
    search_input.send_keys(query)

    try:
        _wait(context, 8).until(
            lambda driver: "suggest_text_show"
            in driver.find_element(By.ID, "suggest_text").get_attribute("class")
            or query.lower() in driver.find_element(By.TAG_NAME, "body").text.lower()
        )
    except TimeoutException:
        search_input.send_keys(Keys.RETURN)
        _wait(context).until(EC.url_contains("/web/iteso/search"))


def _search_tec(context, query):
    driver = context.driver
    try:
        button = _wait(context, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    ".menu-buscador .menu-search-, .zone-search .menu-search-",
                )
            )
        )
        driver.execute_script("arguments[0].click();", button)
        search_input = _wait(context, 5).until(
            EC.element_to_be_clickable((By.ID, "edit-search--4"))
        )
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)
        _wait(context).until(EC.url_contains("/es/busqueda"))
        return
    except TimeoutException:
        driver.get(f"https://tec.mx/es/busqueda?search={quote(query)}")
        _wait(context).until(EC.url_contains("/es/busqueda"))


def _search_udg(context, query):
    driver = context.driver
    try:
        button = _wait(context, 5).until(
            EC.element_to_be_clickable((By.ID, "buscar_front"))
        )
        driver.execute_script("arguments[0].click();", button)
        search_input = _wait(context, 5).until(
            EC.element_to_be_clickable((By.ID, "edit-keys"))
        )
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)
    except TimeoutException:
        driver.get(f"https://www.udg.mx/es/search/node?keys={quote(query)}")

    encoded = quote(query)
    _wait(context).until(
        lambda current: encoded in current.current_url
        or "/search/node" in current.current_url
    )


def _search_in_current_site(context, query):
    url = context.driver.current_url.lower()
    if "iteso.mx" in url:
        _search_iteso(context, query)
        return
    if "tec.mx" in url:
        _search_tec(context, query)
        return
    if "udg.mx" in url:
        _search_udg(context, query)
        return
    raise AssertionError(f"Sitio no soportado para busqueda interna: {url}")


@given("I open Google")
def step_open_google(context):
    context.driver.get("https://www.google.com/ncr")
    _dismiss_google_dialogs(context)
    _wait(context).until(EC.presence_of_element_located((By.NAME, "q")))


@when('I search in Google for "{query}"')
def step_search_google(context, query):
    search_box = _wait(context).until(EC.element_to_be_clickable((By.NAME, "q")))
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    _wait(context).until(EC.presence_of_element_located((By.ID, "search")))


@when('I open the first Google result matching "{expected_domain}"')
def step_open_matching_result(context, expected_domain):
    _wait(context).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#search a[href]"))
    )
    links = context.driver.find_elements(By.CSS_SELECTOR, "#search a[href]")

    for link in links:
        href = (link.get_attribute("href") or "").lower()
        if expected_domain.lower() not in href:
            continue
        if not link.is_displayed():
            continue
        context.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", link
        )
        context.driver.execute_script("arguments[0].click();", link)
        return

    raise AssertionError(
        f"No se encontro un resultado de Google para el dominio {expected_domain}"
    )


@then('I should be on a page from "{expected_domain}"')
def step_verify_domain(context, expected_domain):
    _wait(context).until(
        lambda driver: expected_domain.lower() in driver.current_url.lower()
    )
    assert expected_domain.lower() in context.driver.current_url.lower()


@when('I search within the university site for "{query}"')
def step_search_site(context, query):
    _search_in_current_site(context, query)


@then('I should find content related to "{expected_terms}"')
def step_verify_related_content(context, expected_terms):
    expected_values = [
        _normalize(term.strip()) for term in expected_terms.split(",") if term.strip()
    ]
    page_text = _visible_text(context)
    current_url = _normalize(context.driver.current_url)
    links = " ".join(
        _normalize(element.get_attribute("href") or "")
        for element in context.driver.find_elements(By.CSS_SELECTOR, "a[href]")
    )
    combined = f"{page_text} {current_url} {links}"

    matches = [term for term in expected_values if term in combined]
    assert (
        matches
    ), f"No se encontraron terminos esperados. Esperados: {expected_values}"
