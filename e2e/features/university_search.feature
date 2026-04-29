Feature: University search journeys
  As a prospective student
  I want to find universities in Google and search terms on their websites
  So that I can confirm relevant academic information is available

  Scenario Outline: Search a university in Google and validate internal site results
    Given I open Google
    When I search in Google for "<google_query>"
    And I open the first Google result matching "<expected_domain>"
    Then I should be on a page from "<expected_domain>"
    When I search within the university site for "<site_query>"
    Then I should find content related to "<expected_terms>"

    Examples:
      | google_query                | expected_domain | site_query         | expected_terms                                                         |
      | iteso                       | iteso.mx        | carreras           | Carreras, carreras.iteso.mx, Programas academicos, Academic Programs   |
      | tec de monterrey            | tec.mx          | oferta educativa   | Oferta educativa, Profesional, PrepaTec, Admisiones y Oferta educativa |
      | universidad de guadalajara  | udg.mx          | oferta academica   | Oferta academica, oferta-academica, Aspirantes, programas educativos   |
