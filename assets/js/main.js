const menu = document.querySelector(".menu"),
  links = document.querySelector(".nav-links");
if (menu && links) {
  menu.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
  });
  links
    .querySelectorAll("a")
    .forEach((a) =>
      a.addEventListener("click", () => {
        links.classList.remove("open");
        menu.setAttribute("aria-expanded", "false");
      }),
    );
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && links.classList.contains("open")) {
      links.classList.remove("open");
      menu.setAttribute("aria-expanded", "false");
      menu.focus();
    }
  });
}

if (links) {
  const normalizePath = (value) => {
    const path = value.replace(/\/index\.html$/, "/");
    return path.length > 1 ? path.replace(/\/$/, "") : path;
  };
  const updateActiveLink = () => {
    const currentPath = normalizePath(window.location.pathname);
    links.querySelectorAll("a").forEach((link) => {
      const url = new URL(link.href, window.location.href);
      const linkPath = normalizePath(url.pathname);
      const isLocation = url.hash === "#ubicacion";
      const isSection =
        linkPath !== "/" && currentPath.startsWith(`${linkPath}/`);
      const atLocation = currentPath === "/" && window.location.hash === "#ubicacion";
      const selected = isLocation
        ? atLocation
        : !atLocation && (linkPath === currentPath || isSection);
      link.classList.toggle("active", selected);
      if (selected) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  };
  updateActiveLink();
  window.addEventListener("hashchange", updateActiveLink);
  links.querySelectorAll("a").forEach((link) =>
    link.addEventListener("click", () => {
      links.querySelectorAll("a").forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
    }),
  );
}
document
  .querySelectorAll("[data-year]")
  .forEach((el) => (el.textContent = new Date().getFullYear()));

const whatsappForm = document.querySelector("[data-whatsapp-form]");
if (whatsappForm) {
  whatsappForm.hidden = false;
  whatsappForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!whatsappForm.reportValidity()) return;

    const data = new FormData(whatsappForm);
    const value = (name) => String(data.get(name) || "").trim();
    const lines = [
      "Hola Toyo Services. Quiero solicitar atención para mi Toyota.",
      "",
      ...(value("nombre") ? [`Nombre: ${value("nombre")}`] : []),
      `Modelo: ${value("modelo")}`,
      `Año: ${value("anio") || "No indicado"}`,
      `Servicio: ${value("servicio")}`,
      `Detalle: ${value("mensaje")}`,
      "",
      "Enviado desde toyoservicescartagena.com",
    ];
    const url = `https://wa.me/573018638164?text=${encodeURIComponent(lines.join("\n"))}`;
    window.location.assign(url);
  });
}

// Progressive enhancement: every guide remains crawlable without JavaScript.
const guideSearch = document.querySelector("[data-guide-search]");
if (guideSearch) {
  const input = guideSearch.querySelector("input");
  const status = guideSearch.querySelector("[data-guide-count]");
  const sections = [...document.querySelectorAll(".guide-topic")];
  const normalize = (text) => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const filterGuides = () => {
    const terms = normalize(input.value.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    for (const section of sections) {
      let visible = 0;
      for (const item of section.querySelectorAll("li")) {
        item.hidden = !terms.every((term) => normalize(item.textContent).includes(term));
        if (!item.hidden) visible++;
      }
      section.hidden = visible === 0;
      count += visible;
    }
    status.textContent = count ? `${count} ${count === 1 ? "guía disponible" : "guías disponibles"}` : "No encontramos esa búsqueda. Prueba con el modelo o con otro síntoma.";
  };
  input.addEventListener("input", filterGuides);
  document.querySelectorAll(".topic-links a").forEach((link) => link.addEventListener("click", () => {
    input.value = "";
    filterGuides();
  }));
  guideSearch.hidden = false;
  filterGuides();
}
